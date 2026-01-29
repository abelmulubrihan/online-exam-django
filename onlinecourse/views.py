from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Lesson, Submission, Choice

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    lesson = course.lesson_set.first()  # Adjust if multiple lessons
    if request.method == 'POST':
        learner = request.user.learner
        submission = Submission.objects.create(enrollment=learner)
        selected_choices = request.POST.getlist('choices')
        for choice_id in selected_choices:
            submission.choices.add(Choice.objects.get(id=choice_id))
        return redirect('show_exam_result', course_id=course.id, submission_id=submission.id)

    context = {'course': course, 'lesson': lesson}
    return render(request, 'onlinecourse/exam_bootstrap.html', context)

def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)

    total_score = 0
    possible_score = 0
    selected_ids = []

    for lesson in course.lesson_set.all():
        for question in lesson.question_set.all():
            possible_score += 1
            choices = submission.choices.filter(question=question)
            selected_ids.extend([c.id for c in choices])
            if question.is_get_score([c.id for c in choices]):
                total_score += 1

    grade = f"{total_score}/{possible_score}"

    context = {
        "course": course,
        "selected_ids": selected_ids,
        "grade": grade,
        "possible": possible_score
    }
    return render(request, "onlinecourse/exam_result_bootstrap.html", context)
