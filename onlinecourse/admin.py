from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline, StackedInline
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission

# Inline for Choice
class ChoiceInline(TabularInline):
    model = Choice
    extra = 3

# Inline for Question
class QuestionInline(StackedInline):
    model = Question
    extra = 1

# Admin for Question
class QuestionAdmin(ModelAdmin):
    inlines = [ChoiceInline]

# Admin for Lesson
class LessonAdmin(ModelAdmin):
    inlines = [QuestionInline]

# Register models
admin.site.register(Course)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
