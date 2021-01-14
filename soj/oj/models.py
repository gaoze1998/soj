from django.db import models


class User(models.Model):
    user_name = models.CharField(max_length=16)
    password = models.CharField(max_length=16)
    email = models.CharField(max_length=256)


class Problem(models.Model):
    problem_name = models.CharField(max_length=16)
    problem_content = models.CharField(max_length=1024)
    problem_memory_limit = models.IntegerField()
    problem_time_limit = models.IntegerField()
    sample_location = models.CharField(max_length=256)


class Contest(models.Model):
    contest_name = models.CharField(max_length=16)
    contest_start_time = models.DateTimeField()
    contest_end_time = models.DateTimeField()
    problem_list = models.ManyToManyField(Problem)


class Code(models.Model):
    id = models.AutoField(primary_key=True)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    code_location = models.CharField(max_length=256)


class Grade(models.Model):
    id = models.AutoField(primary_key=True)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    grade = models.IntegerField()
    memo = models.CharField(max_length=16)
