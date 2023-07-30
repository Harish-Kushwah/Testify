from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Candidate(models.Model):
    username = models.CharField(primary_key=True , max_length=20)
    password = models.TextField(null=False)
    name = models.CharField(null=False,max_length=30)
    test_attempted = models.IntegerField(default=0)
    points = models.FloatField(default=0)
    email = models.EmailField(max_length=254,null=True)
    profileImage = models.ImageField(upload_to="profile_images/" , max_length=250,null=True,default=None ,blank=True)
    about = models.TextField(null=True,default=None ,blank=True)
    contact_no = models.TextField(max_length=10,null=True,default=None ,blank=True)
    
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
    wrong_attempted_ques = ArrayField(models.TextField(),null=True)
    not_attempted_ques = ArrayField(models.TextField(),null=True)
    right_attempted_ques = ArrayField(models.TextField(),null=True)

    # def __str__(self):
    #     return self.username

class QuestionImages(models.Model):
    question_id = models.BigAutoField(primary_key=True , auto_created=True)
    question_title = models.CharField(max_length=100)
    question_in_exam = models.CharField(max_length=100,default="OTHER")
    question_image = models.FileField(upload_to="question/" , max_length=250,null=True,default=None)
    ans = models.CharField(max_length=2)

class QuestionRating(models.Model):
    question_rating_id = models.BigAutoField(primary_key=True , auto_created=True)
    question_id = models.ForeignKey(QuestionImages,on_delete=models.CASCADE)
    total_times_not_attempted = models.IntegerField(default=0)
    total_times_wrong = models.IntegerField(default=0)
    total_times_right = models.IntegerField(default=0)
    difficulty  = models.FloatField(default=0.0)

    
class PiChartData(models.Model):
    piChart_id = models.BigAutoField(primary_key=True , auto_created=True)
    username  = models.ForeignKey(Candidate,on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    current_exam_pi_image = models.ImageField(upload_to="piChart/" , max_length=250,null=True,default=None , blank=True)
    all_exam_pi_image = models.ImageField(upload_to="piChart/" , max_length=250,null=True,default=None ,blank=True)
