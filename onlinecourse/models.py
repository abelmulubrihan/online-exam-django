from django.db import models
from django.contrib.auth.models import User

# =========================
# Courses and Lessons
# =========================

class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title

# =========================
# Users: Instructor & Learner
# =========================

class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_time = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

class Learner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    occupation = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

# =========================
# Exam Models: Question, Choice, Submission
# =========================

class Question(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    question_text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def is_get_score(self, selected_ids):
        """
        Check if selected choices are exactly the correct ones
        """
        correct_choices = self.choice_set.filter(is_correct=True).values_list('id', flat=True)
        return set(correct_choices) == set(selected_ids)

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text

class Submission(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)

    def __str__(self):
        return f"Submission by {self.learner.user.username}"
