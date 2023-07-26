from django.db import models

# Create your models here.
class Candidate(models.Model):
    username = models.CharField(primary_key=True , max_length=20)
    password = models.CharField(null=False, max_length=20)
    name = models.CharField(null=False,max_length=30)
    test_attempted = models.IntegerField(default=0)
    points = models.FloatField(default=0)
    # def __str__(self):
    #     return self

class Question(models.Model):
    question_id = models.BigAutoField(primary_key=True , auto_created=True)
    question_statement = models.TextField()
    opt_a = models.CharField(max_length=255)
    opt_b = models.CharField(max_length=255)
    opt_c = models.CharField(max_length=255)
    opt_d = models.CharField(max_length=255)
    ans = models.CharField(max_length=2)
    # def __str__(self):
    #     return self

class Result(models.Model):
    result_id = models.BigAutoField(primary_key=True,auto_created=True)
    username  = models.ForeignKey(Candidate,on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    attempt = models.IntegerField()
    right = models.IntegerField()
    wrong = models.IntegerField()
    points = models.FloatField()

    # def __str__(self):
    #     return self

class QuestionImages(models.Model):
    question_id = models.BigAutoField(primary_key=True , auto_created=True)
    question_title = models.CharField(max_length=100)
    question_image = models.FileField(upload_to="question/" , max_length=250,null=True,default=None)
    ans = models.CharField(max_length=2)
    
class PiChartData(models.Model):
    piChart_id = models.BigAutoField(primary_key=True , auto_created=True)
    username  = models.ForeignKey(Candidate,on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    current_exam_pi_image = models.ImageField(upload_to="piChart/" , max_length=250,null=True,default=None , blank=True)
    all_exam_pi_image = models.ImageField(upload_to="piChart/" , max_length=250,null=True,default=None ,blank=True)
