from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    title = models.TextField()  # default null=True, blank=True
    status = models.CharField(default="inactive", max_length=10)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # auto_now reference https://stackoverflow.com/questions/51389042/difference-between-auto-now-and-auto-now-add
    # auto_now - updates the value of field to current time and date every time the Model.save() is called.
    # auto_now_add - updates the value with the time and date of creation of record.
    # if a filed in model contains both the auto_now and auto_now_add set to True?
    # auto_now takes precedence (obviously, because it updates field each time, while auto_now_add updates on creation only).

    def __str__(self):
        return self.title

    @property
    def choices(self):
        # pylint: disable=E1101
        return self.choice_set.all()


class Choice(models.Model):
    question = models.ForeignKey('poll.Question', on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    @property
    def votes(self):
        # pylint: disable=E1101
        return self.answer_set.count()


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # pylint: disable=E1101
        return self.user.username + '-' + self.choice.text
