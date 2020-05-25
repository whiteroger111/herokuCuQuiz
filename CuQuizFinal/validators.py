import functools
import gzip
import re
from difflib import SequenceMatcher
from pathlib import Path

from django.conf import settings
from django.core.exceptions import (
    FieldDoesNotExist, ImproperlyConfigured, ValidationError,
)
from django.utils.functional import lazy
from django.utils.html import format_html, format_html_join
from django.utils.module_loading import import_string
from django.utils.translation import gettext as _, ngettext


@functools.lru_cache(maxsize=None)
def get_default_password_validators():
    return get_password_validators(settings.AUTH_PASSWORD_VALIDATORS)


def get_password_validators(validator_config):
    validators = []
    for validator in validator_config:
        try:
            klass = import_string(validator['NAME'])
        except ImportError:
            msg = "The module in NAME could not be imported: %s. Check your AUTH_PASSWORD_VALIDATORS setting."
            raise ImproperlyConfigured(msg % validator['NAME'])
        validators.append(klass(**validator.get('OPTIONS', {})))

    return validators


def validate_password(password, user=None, password_validators=None):
    errors = []
    if password_validators is None:
        password_validators = get_default_password_validators()
    for validator in password_validators:
        try:
            validator.validate(password, user)
        except ValidationError as error:
            errors.append(error)
    if errors:
        raise ValidationError(errors)


def password_changed(password, user=None, password_validators=None):
    if password_validators is None:
        password_validators = get_default_password_validators()
    for validator in password_validators:
        password_changed = getattr(validator, 'password_changed', lambda *a: None)
        password_changed(password, user)


def password_validators_help_texts(password_validators=None):
    help_texts = []
    if password_validators is None:
        password_validators = get_default_password_validators()
    for validator in password_validators:
        help_texts.append(validator.get_help_text())
    return help_texts


def _password_validators_help_text_html(password_validators=None):
    help_texts = password_validators_help_texts(password_validators)
    help_items = format_html_join('', '<li>{}</li>', ((help_text,) for help_text in help_texts))
    return format_html('<ul>{}</ul>', help_items) if help_items else ''


password_validators_help_text_html = lazy(_password_validators_help_text_html, str)


class MinimumLengthValidator:
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ngettext(
                    "თქვენი პაროლი მინიმუმ უნდა შეიცავდეს %(min_length)d სიმბოლოს.",
                    "თქვენი პაროლი მინიმუმ უნდა შეიცავდეს %(min_length)d სიმბოლოს.",
                    self.min_length
                ),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return ngettext(
            "თქვენი პაროლი მინიმუმ უნდა შეიცავდეს %(min_length)d სიმბოლოს.",
            "თქვენი პაროლი მინიმუმ უნდა შეიცავდეს %(min_length)d სიმბოლოს.",
            self.min_length
        ) % {'min_length': self.min_length}


class UserAttributeSimilarityValidator:
    DEFAULT_USER_ATTRIBUTES = 'username'

    def __init__(self, user_attributes=DEFAULT_USER_ATTRIBUTES, max_similarity=0.7):
        self.user_attributes = user_attributes
        self.max_similarity = max_similarity

    def validate(self, password, user=None):
        if not user:
            return

        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if not value or not isinstance(value, str):
                continue
            value_parts = re.split(r'\W+', value) + [value]
            for value_part in value_parts:
                if SequenceMatcher(a=password.lower(), b=value_part.lower()).quick_ratio() >= self.max_similarity:
                    try:
                        verbose_name = str(user._meta.get_field(attribute_name).verbose_name)
                    except FieldDoesNotExist:
                        verbose_name = attribute_name
                    raise ValidationError(
                        _("პაროლი არ შეიძლება იყოს მსგავსი %(verbose_name)-ის."),
                        code='password_too_similar',
                        params={'verbose_name': verbose_name},
                    )

    def get_help_text(self):
        return _('პაროლი არ შეიძლება იყოს მომხმარებლლის სახელის მსგავსი.')


class CommonPasswordValidator:
    DEFAULT_PASSWORD_LIST_PATH = Path(__file__).resolve().parent / 'common-passwords.txt.gz'

    def __init__(self, password_list_path=DEFAULT_PASSWORD_LIST_PATH):
        try:
            with gzip.open(password_list_path, 'rt', encoding='utf-8') as f:
                self.passwords = {x.strip() for x in f}
        except OSError:
            with open(password_list_path) as f:
                self.passwords = {x.strip() for x in f}

    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise ValidationError(
                _("პაროლი ძალიან მარტივია."),
                code='password_too_common',
            )

    def get_help_text(self):
        return _('პაროლი ძალიან მარტივია.')


class NumericPasswordValidator:
    """
    Validate whether the password is alphanumeric.
    """
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                _("პაროლი შეიცავს მხოლოდ ციფრებს."),
                code='password_entirely_numeric',
            )

    def get_help_text(self):
        return _('პაროლი შეიცავს მხოლოდ ციფრებს.')
