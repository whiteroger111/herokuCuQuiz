from django.contrib import admin

# Register your models here.
from django.contrib import admin
import nested_admin

# Register your models here.
from .models import User, Subject, Quiz, Question, Answer, Student, TakenQuiz, StudentAnswer, Post


class AnswerInline(nested_admin.NestedTabularInline):
    model = Answer
    extra = 4
    max_num = 4


class QuestionInline(nested_admin.NestedTabularInline):
    model = Question
    inlines = [AnswerInline, ]
    extra = 5


class QuizAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInline, ]


class UsersAnswerInline(admin.TabularInline):
    model = StudentAnswer


class QuizTakerAdmin(admin.ModelAdmin):
    inlines = [UsersAnswerInline, ]


admin.site.register(User)
admin.site.register(Subject)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Student, QuizTakerAdmin)
admin.site.register(TakenQuiz)
admin.site.register(StudentAnswer)
admin.site.register(Post)
