from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from Test.models import *
import pandas as pd
from scipy import stats
import random
import datetime
from django.contrib import messages
from django.contrib.auth.hashers import make_password,check_password
from django.core.paginator import Paginator
# from django.contrib.messages.storage.session.SessionStorage

#-----------------------------------------------------------------------------------------------------------
#This view used for showing welcome page to new  user  by rendering 'welcome.html'
def welcome(request):
    logoutStatus = 1
    template = loader.get_template('welcome.html')  #load the html file
    return render(request , 'welcome.html',{'logoutStatus':logoutStatus})


#-----------------------------------------------------------------------------------------------------------
#This view used for show SignUp form to new  user  by rendering 'registration_form.html'
def candidateRegistrationForm(request):
    res = render(request , 'registration_form.html')
    return res

#-----------------------------------------------------------------------------------------------------------
#This view used for SignUp new  user  by rendering 'registration.html'
def candidateRegistration(request):
    if request.method =='POST':
        username = request.POST['username']
        #check if the user already exists
        if len(Candidate.objects.filter(username=username)) :
            userStatus = 1
            messages.info(request,"Sorry,Username Already exists , please try different Username")
            return HttpResponseRedirect('registrationform')
        else:
            candidate =  Candidate()
            candidate.username = username
            candidate.password = make_password(request.POST['password'])
            candidate.name =request.POST['name']
            candidate.save()
            userStatus = 2
            messages.info(request,"Account Created Successfully,Please Login Yourself")
            return render(request,'login.html')
    else:
        userStatus = 3 #request dose not have method post

    context = {'userStatus' : userStatus}
    res = render(request ,'registration_form.html',context)
    return res

#-----------------------------------------------------------------------------------------------------------
#This view used for login user and by rendering 'login.html'
def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password =request.POST['password']
        candidates = Candidate.objects.filter(username = username)
        for candidate in candidates:
            if check_password(password,candidate.password):
                loginSuccess ="Login Successful,"
                messages.info(request,loginSuccess)
                request.session['username'] = candidate.username
                request.session['name'] = candidate.name
                return  HttpResponseRedirect('home')
        else:
            loginError = "Invalid username or password"
            storage = messages.get_messages(request)
            storage.used = False
            messages.info(request,loginError)
            return render(request,'login.html')
           
    else:
        res = render(request,'login.html')
    return res

#-----------------------------------------------------------------------------------------------------------
#This view used for user to reach on Home page by rendering 'home.html'
def candidateHome(request):
    if 'name' not in request.session.keys():
        res = HttpResponseRedirect('login')
    else:
        res = render(request,'home.html')
    return res

#-----------------------------------------------------------------------------------------------------------
#This view used for logout user and redirects on welcome page
def logoutView(request):
    logoutStatus = 1 #user not logout
    username =''
    if 'name'  in request.session.keys():
        username = request.session['username']
        del request.session['username']
        del request.session['name']
        logoutStatus = 2  #user logout successfully
    context = {'logoutStatus':logoutStatus , 'username':username}
    return render(request , 'welcome.html',context)

#-----------------------------------------------------------------------------------------------------------
#This view used for creating N Questions test paper question in IMAGE format by rendering 'test_paper.html' file
def testPaper(request):
    #check whether user is login or not
    if 'name' not in request.session.keys():
        res = HttpResponseRedirect('login')
    
    #fetch question from db
    n = int(request.GET['n'])
    question_pool =list(QuestionImages.objects.all())
    question_list = None
    if len(question_pool)!=0:
        random.shuffle(question_pool)
        question_list = question_pool[:n]
        examStatus = 1
    else:
        examStatus = 2  #if no question found

    hr = n//60 
    min = n%60
    sec = 0
    context = {'questions' : question_list , 
               'examStatus':examStatus,
               'totalQuestion':n,
               'topicName':"All",
               'time':n ,
               'hr':hr , 
               'min':min,
               'sec':sec}
    res  = render(request , 'test_paper.html',context)
    return res 

#-----------------------------------------------------------------------------------------------------------
#This view used for creating custome test paper question in IMAGE format by rendering 'test_paper.html' file
def customsTestPaper(request):
    if 'name' not in request.session.keys():
        res = HttpResponseRedirect('login')
    
    topic_name = str(request.POST['topic_name']).strip().upper()
    if len(topic_name)==0:
        topic_name = "All"
    total_ques = int(request.POST['total_que'])
    question_pool = list(QuestionImages.objects.filter(question_title =topic_name))
    question_list = None
    if len(question_pool)!=0:
        random.shuffle(question_pool)
        question_list = question_pool[:total_ques]
        examStatus = 1
    else:
        examStatus = 2  #if no question found

    hr = total_ques//60 
    min = total_ques%60
    sec = 0
    #1 question 1 min
    timeAllot = total_ques
   
    context = {'questions' : question_list , 
               'examStatus':examStatus ,
               'totalQuestion':total_ques,
               'topicName':topic_name,
               'time':timeAllot ,
               'hr':hr ,
                'min':min,
                'sec':sec,
                }
    res  = render(request , 'test_paper.html',context)
    return res 

#-----------------------------------------------------------------------------------------------------------
#This view used for showing question in text format by rendering 'test_paper.html' file
def textTestPaper(request):
    #check whether user is login or not
    if 'name' not in request.session.keys():
        res = HttpResponseRedirect('login')
    
    #fetch question from db
    n = int(request.GET['n'])
    question_pool =list(Question.objects.all())
    random.shuffle(question_pool) #to get random element
    question_list = question_pool[:n]
    
    context = {'questions' : question_list }

    res  = render(request , 'test_paper.html',context)
    return res 


#-----------------------------------------------------------------------------------------------------------
#This view used for calculating test and string into Database of each test  and redirect to  'result' url
def calculateTestResult(request):
    if 'name' not in request.session.keys():
        res = HttpResponseRedirect('login')
    
    total_attempt = 0
    total_right = 0
    total_wrong = 0
    wrong_attempted_ques =[]
    right_attempted_ques =[]
    not_attempted_ques =[]
    qid_list = [] #all questions of the test
    for k in request.POST:
        if k.startswith('qno'):
            qid_list.append(int(request.POST[k]))
    
    for n in qid_list:
        question_img = QuestionImages.objects.get(question_id = n)
        try:
              
            if question_img.ans == request.POST['op' + str(n)]:
                total_right +=1
                right_attempted_ques.append(question_img.question_id)
            else:
                total_wrong +=1
                wrong_attempted_ques.append(question_img.question_id)
            total_attempt+=1
            
        except:
            pass
    if total_attempt!=0:
        points = (total_right - total_wrong) /  total_attempt *10
    else:
        points = 0

    # finds the set of not_attempted question of the test
    right_and_wrong_que = set(right_attempted_ques).union(set(wrong_attempted_ques))
    qid_list =  set(qid_list)
    setA  = right_and_wrong_que - qid_list
    setB  = qid_list - right_and_wrong_que
    not_attempted_ques = list(setA.union(setB))
   
    username = Candidate.objects.get(username = request.session['username'])
    result = Result()
    result.username = username
    result.attempt = total_attempt
    result.right = total_right
    result.wrong = total_wrong
    result.points = points
    result.not_attempted_ques = not_attempted_ques
    result.wrong_attempted_ques = wrong_attempted_ques
    result.right_attempted_ques = right_attempted_ques
    result.save()

    #update candidate table
    candidate = username
    candidate.test_attempted +=1
    candidate.points = ( candidate.points * (candidate.test_attempted -1) + points )/candidate.test_attempted
    candidate.save()
    return HttpResponseRedirect('result') 

#NOTE: pagination 
def calculateTestResult1(request):
    if 'name' not in request.session.keys():
        res = HttpResponseRedirect('login')
    
    total_attempt = 0
    total_right = 0
    total_wrong = 0
    wrong_attempted_ques =[]
    right_attempted_ques =[]
    not_attempted_ques =[]
    qid_list = [] #all questions of the test
    for k in request.POST:
        if k.startswith('qno'):
            qid_list.append(int(request.POST[k]))
    
    for n in qid_list:
        question_img = QuestionImages.objects.get(question_id = n)
        try:
              
            if question_img.ans == request.POST['op' + str(n)]:
                total_right +=1
                right_attempted_ques.append(question_img.question_id)
            else:
                total_wrong +=1
                wrong_attempted_ques.append(question_img.question_id)
            total_attempt+=1
            
        except:
            pass
    if total_attempt!=0:
        points = (total_right - total_wrong) /  total_attempt *10
    else:
        points = 0

    # finds the set of not_attempted question of the test
    right_and_wrong_que = set(right_attempted_ques).union(set(wrong_attempted_ques))
    qid_list =  set(qid_list)
    setA  = right_and_wrong_que - qid_list
    setB  = qid_list - right_and_wrong_que
    not_attempted_ques = list(setA.union(setB))
   
    username = Candidate.objects.get(username = request.session['username'])
    result = Result()
    result.username = username
    result.attempt = total_attempt
    result.right = total_right
    result.wrong = total_wrong
    result.points = points
    result.not_attempted_ques = not_attempted_ques
    result.wrong_attempted_ques = wrong_attempted_ques
    result.right_attempted_ques = right_attempted_ques
    result.save()

    #update candidate table
    candidate = username
    candidate.test_attempted +=1
    candidate.points = ( candidate.points * (candidate.test_attempted -1) + points )/candidate.test_attempted
    candidate.save()
    return HttpResponseRedirect('result') 


#-----------------------------------------------------------------------------------------------------------
#This view used for Showing test result of each test  by rendering "show_result.html" file
# NOTE:When result will be displayed at that time rating will be updated each question 
# BUG:integrity error arise during result storing difficulty each question
def get_difficulty_of_question(questionRating):
    right = questionRating.total_times_right
    wrong = questionRating.total_times_wrong
    total_attempted = right + wrong
    if total_attempted !=0:
        difficulty = (right/total_attempted)*100
        return difficulty
    return 0


def showTestResult(request):
    if 'name' not in request.session.keys():
        res = HttpResponseRedirect('login')
    
    #fetch latest result
    results  = Result.objects.filter(result_id = Result.objects.latest('result_id').result_id , username_id = request.session['username'])
    context = {'results' : results}
    for res in results:
        not_attempted_ques = res.not_attempted_ques
        right_attempted_ques = res.right_attempted_ques
        wrong_attempted_ques = res.wrong_attempted_ques

        for question in not_attempted_ques:
            questionRating  = QuestionRating.objects.get(question_id = question)
            if questionRating!=None:
                questionRating.total_times_not_attempted+=1
                questionRating.difficulty=get_difficulty_of_question(questionRating)
                questionRating.save()

        for question in right_attempted_ques:
            questionRating  = QuestionRating.objects.get(question_id = question)
            if questionRating !=None:
                questionRating.total_times_right+=1
                questionRating.difficulty=get_difficulty_of_question(questionRating)
                questionRating.save()

        for question in wrong_attempted_ques:
            questionRating  = QuestionRating.objects.get(question_id = question)
            if questionRating !=None:
                questionRating.total_times_wrong+=1
                questionRating.difficulty=get_difficulty_of_question(questionRating)
                questionRating.save()
        
    res = render(request,'show_result.html' , context)
    return res


#-----------------------------------------------------------------------------------------------------------
#This view used for Uploading Question  by rendering "upload_question.html" file
# NOTE:When new question will uploaded at that time question row added in QuestionRating table 

def uploadQuestion(request):
    if 'name' not in request.session.keys():
        return HttpResponseRedirect('login')
    if request.method == 'POST':
        questionImg = QuestionImages()
        questionRating = QuestionRating()
        questionImg.question_title = str(request.POST['title']).strip().upper()
        questionImg.ans = request.POST['ans']
        questionImg.question_in_exam =str(request.POST['exam']).strip().upper()
        
        if len(request.FILES)!=0:
            questionImg.question_image = request.FILES['img']
            questionRating.question_id = questionImg
        else :
          res = HttpResponseRedirect('home')
        questionImg.save()
        questionRating.save()
        messages.success(request,"Question added successfully")
    res = render(request, 'upload_question.html' )
    return res




#-----------------------------------------------------------------------------------------------------------
#This view used for Showing test result history by rendering "candidate_history.html" file
from Test.graphs import *
def testResultHistory(request):
    if 'name' not in request.session.keys():
        res = HttpResponseRedirect('login')

    candidate = Candidate.objects.filter(username = request.session['username'])
    results = Result.objects.filter(username_id =request.session['username'])
    test_attempted = 2
    chart = None
    bar  = None
    if len(results)!=0:
        chart = plotPi(results)
        bar = plotBar(results)
        test_attempted = 1 
        # status =getTrendResult(results)
        li = plotTrend(results)
        trend = li[0]
        status =li[1]
        points =format(candidate[0].points, ".2f")
        context = {'candidate' : candidate[0] ,
                'results':results,
                'chart':chart,
                'testAttempted':test_attempted ,
                    'bar':bar,
                    'Status':status,
                    'points':points,
                    'trend':trend
                    }
        
        res = render(request, 'candidate_history.html' , context)
    else:
        messages.info(request , "No test given")
        res = HttpResponseRedirect('home')
    return res

#-----------------------------------------------------------------------------------------------------------
#This view used for Showing test result history by rendering "candidate_history.html" file
def account(request):
    if 'name' not in request.session.keys():
        res = HttpResponseRedirect('login')
    candidate = Candidate.objects.filter(username = request.session['username'])
    results = Result.objects.filter(username = request.session['username'])
    points =format(candidate[0].points, ".2f")
    
    context = {'candidate':candidate[0],'points':points ,'results':results }

    res = render(request, 'user_account.html',context)
    return res


#-----------------------------------------------------------------------------------------------------------
#This view used for edit profile data 
def edit_profile_info(request):
    if 'name' not in request.session.keys():
        res = HttpResponseRedirect('login')
    
    candidate = Candidate.objects.get(username = request.session['username'])
    
    edited = False

    if request.method == 'POST':
        if 'img' in request.FILES:
            candidate.profileImage  = request.FILES['img']
            edited = True
            candidate.save()

        if len(request.POST['name'])!=0:
            candidate.name = request.POST['name']
            edited = True

        if len(request.POST['email'])!=0:
            candidate.email = request.POST['email']
            edited = True

        if len(request.POST['contact'])!=0:
            candidate.contact_no = request.POST['contact']
            edited = True

        if len(request.POST['about'])!=0:
            candidate.about = request.POST['about']
            edited = True

    if edited :
        candidate.save()
        messages.success(request,"Successfully Profile updated")
    else:
        messages.info(request,"Unable to changed info")

    res = HttpResponseRedirect('account')

    return res

#-----------------------------------------------------------------------------------------------------------












#-----------------------------------------------------------------------------------------------------------
#This view is not using because it used TEXT question database to calculate result
'''
def calculateTestResult1(request):
    if 'name' not in request.session.keys():
        res = HttpResponseRedirect('login')
    
    total_attempt = 0
    total_right = 0
    total_wrong = 0
    qid_list = []
    for k in request.POST:
        if k.startswith('qno'):
            qid_list.append(int(request.POST[k]))
    
    for n in qid_list:
        question = Question.objects.get(question_id = n)
        try:
            if question.ans == request.POST['q' + str(n)]:
                total_right +=1
            else:
                total_wrong +=1
            total_attempt+=1
        except:
            pass

    points = (total_right - total_wrong) / len(qid_list) *10

    #store it into result table
    result = Result()
    result.username = Candidate.objects.get(username = request.session['username'])
    result.attempt = total_attempt
    result.right = total_right
    result.wrong = total_wrong
    result.points = points
    result.save()

    #update candidate table
    candidate = Candidate.objects.get(username = request.session['username'])
    candidate.test_attempted +=1
    candidate.points = ( candidate.points * (candidate.test_attempted -1) + points )/candidate.test_attempted
    candidate.save()
    return HttpResponseRedirect('result') 
'''
