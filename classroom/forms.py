from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from classroom.models import (Answer, Question, Student, StudentAnswer, Subject, User)
from django.contrib.auth.forms import UsernameField, AuthenticationForm
from django.contrib.auth.password_validation import *


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label='მომხმარებლის სახელი',
        widget=forms.TextInput(attrs={'autofocus': True}),
        error_messages={
            'required': "ეს ველი სავალდებულოა",
        }
    )
    password = forms.CharField(
        label="პაროლი",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
        error_messages={
            'required': "ეს ველი სავალდებულოა",
        }
    )

    error_messages = {
        'invalid_login': "გთხოვთ შეიყვანოთ სწორი მომხმარებლის სახელი და პაროლი",
        'required': "ეს ველი სავალდებულოა",
    }


class TeacherSignUpForm(UserCreationForm):
    username = UsernameField(
        label='მომხმარებლის სახელი',
        widget=forms.TextInput(attrs={'autofocus': True}),
        error_messages={
            'required': "ეს ველი სავალდებულოა",
        }
    )
    password1 = forms.CharField(
        label="პაროლი",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
        error_messages={
            'required': "ეს ველი სავალდებულოა",
        }
    )
    password2 = forms.CharField(
        label="გაიმეორეთ პაროლი",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
        error_messages={
            'required': "ეს ველი სავალდებულოა",
        }
    )

    error_messages = {
        'password_mismatch': 'პაროლები არაა იდენტური.',
    }

    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user


class StudentSignUpForm(UserCreationForm):
    username = UsernameField(
        label='მომხმარებლის სახელი',
        widget=forms.TextInput(attrs={'autofocus': True}),
        error_messages={
            'required': "ეს ველი სავალდებულოა",
        }
    )
    password1 = forms.CharField(
        label="პაროლი",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
        error_messages={
            'required': "ეს ველი სავალდებულოა",
        }
    )
    password2 = forms.CharField(
        label="გაიმეორეთ პაროლი",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
        error_messages={
            'required': "ეს ველი სავალდებულოა",
        }
    )

    error_messages = {
        'password_mismatch': 'პაროლები არაა იდენტური.',
    }

    interests = forms.ModelMultipleChoiceField(
        label='ინტერესი',
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User

    def __init__(self, *args, **kwargs):
        super(StudentSignUpForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required': ' ველის შევსება აუცილებელია'.format(
                fieldname=field.label)}

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        student.interests.add(*self.cleaned_data.get('interests'))
        return user


class StudentInterestsForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('interests',)
        widgets = {
            'interests': forms.CheckboxSelectMultiple
        }
        labels = {
            "interests": "ინტერესი"
        }

    """"
    interests = forms.ModelMultipleChoiceField(
        label='საგანი',
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    """

    def __init__(self, *args, **kwargs):
        super(StudentInterestsForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required': ' ველის შევსება აუცილებელია'.format(
                fieldname=field.label)}


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text',)
        labels = {
            "text": "შეკითხვა"
        }

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required': ' ველის შევსება აუცილებელია'.format(
                fieldname=field.label)}


class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise ValidationError('პასუხი არაა მონიშნული.', code='no_correct_answer')


class TakeQuizForm(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset=Answer.objects.none(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None)

    class Meta:
        model = StudentAnswer
        fields = ('answer',)

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['answer'].queryset = question.answers.order_by('text')

        for field in self.fields.values():
            field.error_messages = {'required': ' ველის შევსება აუცილებელია'.format(
                fieldname=field.label)}
        self.fields['answer'].label = "პასუხი"
