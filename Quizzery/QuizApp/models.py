from ipaddress import ip_address
from django.db import models
from django.db.models.deletion import CASCADE
# Create your models here.


class UserTable(models.Model):
    name = models.CharField(max_length=30)
    user_id = models.BigIntegerField(primary_key=True)
    email = models.EmailField()
    password = models.CharField(max_length=20)


class QuizTable(models.Model):
    user_id = models.ForeignKey(to=UserTable, db_column='user_id', on_delete=CASCADE)
    quizname = models.CharField(max_length=50)
    quiz_id = models.BigIntegerField(primary_key=True)
    quiz_desc = models.TextField()
    quiz_time = models.IntegerField()
    start_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    end_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    public = models.BooleanField(default=True)


class QuestionsTable(models.Model):
    quiz_id = models.ForeignKey(to=QuizTable, db_column='quiz_id', on_delete=CASCADE)
    question_no = models.IntegerField()
    question = models.TextField()
    option_1 = models.CharField(max_length=200)
    option_2 = models.CharField(max_length=200)
    option_3 = models.CharField(max_length=200)
    option_4 = models.CharField(max_length=200)
    answer = models.CharField(max_length=8)


class QuizExamTable(models.Model):
    quiz_id = models.ForeignKey(to=QuizTable, db_column='quiz_id', on_delete=CASCADE)
    quiz_username = models.CharField(max_length=30)
    ipaddress = models.CharField(max_length=15)
    time_of_joining = models.DateTimeField()
    score = models.IntegerField()


class QuestionAnswerTable(models.Model):
    quiz_id = models.ForeignKey(to=QuizTable, db_column='quiz_id', on_delete=CASCADE)
    quiz_username = models.CharField(max_length=30)
    question = models.TextField(default=None)
    answer = models.CharField(max_length=8)
    score = models.IntegerField()


class Statistics(models.Model):
    quiz_id = models.ForeignKey(to=QuizTable, db_column='quiz_id', on_delete=CASCADE)
    most_correctly_answered_question = models.IntegerField()
    most_incorrectly_answered_question = models.IntegerField()
