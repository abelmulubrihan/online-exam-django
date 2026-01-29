from django.shortcuts import render, get_object_or_404, redirect
from .models import Lesson, Submission, Choice
from django.contrib import messages


def submit(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    if request.method == 'POST':
        selected_choices = request.POST.getlist('choices')
        choices = Choice.objects.filter(id__in=selected_choices)
        submission = Submission.objects.create(lesson=lesson)
        submission.choices.set(choices)
        return redirect('show_exam_result', lesson_id=lesson_id)
    return render(request, 'onlinecourse/course_details_bootstrap.html', {'lesson': lesson})


def show_exam_result(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    submission = Submission.objects.filter(lesson=lesson).last()
    if not submission:
        messages.error(request, 'No submission found.')
        return redirect('submit', lesson_id=lesson_id)
    score = 0
    total_questions = lesson.question_set.count()
    for question in lesson.question_set.all():
        question_score = question.get_score(submission.choices.all())
        score += question_score
    score_percentage = (score / total_questions) * 100 if total_questions > 0 else 0
    return render(request, 'onlinecourse/exam_result.html', {
        'lesson': lesson,
        'score': score_percentage,
        'total_questions': total_questions
    })
