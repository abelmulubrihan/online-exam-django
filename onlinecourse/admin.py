from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline, StackedInline
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission

# =========================
# Inline models for admin
# =========================

class ChoiceInline(TabularInline):
    model = Choice
    extra = 3

class QuestionInline(StackedInline):
    model = Question
    extra = 1

# =========================
# Admin classes
# =========================

class CourseAdmin(ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    list_filter = ('name',)
    inlines = []

class LessonAdmin(ModelAdmin):
    list_display = ('title', 'course')
    search_fields = ('title', 'course__name')
    inlines = [QuestionInline]

class QuestionAdmin(ModelAdmin):
    list_display = ('question_text', 'lesson', 'pub_date')
    inlines = [ChoiceInline]

# =========================
# Register models
# =========================

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
    