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
import time
from datetime import date
from datetime import datetime ,time , date
import datetime as dt
# from dateutil.relativedelta import relativedelta
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
def home(request):
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
    n = 0
    if request.method == 'GET':
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
#This view used for creating test paper question in IMAGE format by rendering 'set_test_paper.html' file
def createTestPaper(request):
    if 'name' not in request.session.keys():
        res  = HttpResponseRedirect('login')
    question_pool =list(QuestionImages.objects.all())
    context = {'questions' :question_pool}
    
    res  = render(request , 'set_test_paper.html' , context)
    return res


#-----------------------------------------------------------------------------------------------------------
#This view used for set questions into test paper  IMAGE format into database
import string
import random 
def generate_unique_code():
    length = 6
    while True:
        code= ''.join(random.choices(string.ascii_uppercase,k=length))
        if TestPaperSet.objects.filter(code=code).count()==0:
            break
    return code


def setQuestionSet(request):
    if 'name' not in request.session.keys():
        res  = HttpResponseRedirect('login')

    if request.method == 'POST':
        test_paper_name = str(request.POST['test_paper_name']).strip().upper()
        total_question =  request.POST['total_question']
        start_date = request.POST['start_date']
        start_time =  request.POST['start_time']
        # meridian =  request.POST['meridian'] 
      
        #convert time duration into exam end_time
        start_time_list = [int(i) for i in start_time.split(':')]
        start_date_list = [int(i) for i in start_date.split('-')]
        print(start_date)
        #    end_hr duration + start_time_hour
        hr = int(request.POST['hr']) + start_time_list[0]
        min = int(request.POST['min']) + start_time_list[1]
        sec = int(request.POST['sec']) + 0
 
        end_year = start_date_list[0]
        end_month = start_date_list[1]
        end_day = start_date_list[2]
        
        #NOTE:here we are only took care of day this is bruit force need to optimize logic
        if hr>=24 or start_time_list[0] == 0:
            end_day+= hr//24
            hr = hr%24
        if sec>60:
            min+=sec//60
            sec = sec%60
        if min>60:
            hr+=min//60
            min = min%60

        # delta = relativedelta(year=+)
        # end_date = start_data + (start_time+ duration_of_test)

        end_date = dt.datetime(end_year, end_month , end_day ,hour=hr , minute=min , second=sec)
        # start_date = dt.datetime(start_year, start_month , start_day)
        # future_date =relativedelta(hour=+hr , minute=+min , second=+sec)

        end_time = dt.time(hour=hr , minute=min , second=sec)
        qid_list =[]
        for k in request.POST:
            if k.startswith('qno'):
                qid_list.append(int(request.POST[k]))
        
        # insert data into testpaper set
        new_test_paper = TestPaperSet()
        new_test_paper.test_paper_name = test_paper_name
        new_test_paper.code = generate_unique_code()
        new_test_paper.start_date = start_date
        new_test_paper.start_time = start_time
        new_test_paper.end_time= end_time
        new_test_paper.end_date= end_date
        new_test_paper.total_question = total_question
        new_test_paper.created_by = request.session['username']
        new_test_paper.save()
        
        #add all the questions of testpaper set
        for id in qid_list:
            question_set  = QuestionSet()
            question_set.test_paper_id = new_test_paper
            question_set.question_id  = id
            question_set.save()

    messages.info(request,"Test paper added successfully:")
    res =  HttpResponseRedirect('home')
    return res

#-----------------------------------------------------------------------------------------------------------
#This view used for starting the test paper on the basis of Test Paper code
def startTestPaper(request):
    if 'name' not in request.session.keys():
        res =  HttpResponseRedirect('login')
    
    #NOTE:we are taking  code which is 6 upper case character
    if request.GET:
        code = str(request.GET['code']).strip()
    elif request.POST:
        code = str(request.POST['code']).strip()

    if code.isalpha():
        test_paper_set =TestPaperSet.objects.filter(code=code)
        if len(test_paper_set)!=0:
            for test_paper in test_paper_set:
                question_pool = []
                question_set = QuestionSet.objects.filter(test_paper_id=test_paper)
                for question in question_set:
                    question_pool.append(QuestionImages.objects.get(question_id =question.question_id))   
            
                # Exam set date and time
                start_date = test_paper.start_date
                start_time = test_paper.start_time

                end_time = test_paper.end_time
                end_date = test_paper.end_date
                
                end_hr = end_time.hour
                end_min =end_time.minute
                end_sec = end_time.second
            
            
                # Current date time 
                currentDate = date.today()
                currentTime = datetime.now()
                currentTimeObj = time(currentTime.hour , currentTime.minute , currentTime.second) 
                currHr = currentTime.hour
                currMin = currentTime.minute

                total_day_diff =end_date.day - start_date.day

                # time set on timer timer 
                hr = (end_time.hour - currHr)  + total_day_diff*24
                min = end_time.minute - currMin
                sec = end_time.second  -currentTime.second
                start = (currentTimeObj.hour == 0  and start_time.hour>=0 ) or (end_time.hour == 0 and currentTimeObj.hour>=0)
                print(end_time.hour)
                
                timeAllot = str(end_hr  - start_time.hour) +":" + str(end_min - start_time.minute) +":" + str(end_sec - start_time.second)
                if start_date == currentDate and currentDate<=end_date :
                    if (currentTimeObj == start_time and currentTimeObj<end_time ) or start:
                        print("Exam started")
                
                    elif currentTimeObj>=end_time:
                        messages.info(request , 'Exam time finished ')
                        return HttpResponseRedirect('home')
                    elif currentTimeObj<start_time:
                        messages.info(request , 'Exam is not started')
                        return HttpResponseRedirect('home')
                elif start_date > currentDate:
                    messages.info(request , 'Test is not started')
                    return HttpResponseRedirect('home')
                else:
                    messages.info(request , 'Test was finished')
                    return HttpResponseRedirect('home')
                
                #1 question 1 min
                total_ques = test_paper.total_question           
                examStatus = 1
                context = {'questions' : question_pool , 
                        'examStatus':examStatus ,
                        'totalQuestion':total_ques,
                        'topicName':test_paper.test_paper_name,
                        'time':timeAllot ,
                        'hr':hr ,
                        'examStatus':examStatus ,
                            'min':min,
                            'sec':sec,
                            }
                res  = render(request , 'test_paper.html',context)
        else:
            messages.info(request , 'No Test Available')
            res = HttpResponseRedirect('home')
    else:
        messages.info(request , 'Enter valid code for test')
        res =  HttpResponseRedirect('home')
    return res 

    
#-----------------------------------------------------------------------------------------------------------
#This view used for showing all the test paper set are going on and give then
def compete(request):
    if 'name' not in request.session.keys():
        res = HttpResponseRedirect('login')
    testPaper = TestPaperSet.objects.all()
    context = {'testPapers':testPaper}
    res  = render(request , 'all_test.html',context)
    return res

#-----------------------------------------------------------------------------------------------------------
#This view used for setting NIMCET test paper format by rendering 'test_paper.html' file
def NIMCET_Test(request):
    if 'name' not in request.session.keys():
        res = HttpResponseRedirect('login')
    
    total_question = 120
    total_math =  50
    total_analytical_ability =40
    total_english = 20
    total_computer = 10  
   
    math_questions = list(QuestionImages.objects.filter(question_title ="MATH"))
    analytical_ability_questions = list(QuestionImages.objects.filter(question_title ="ANALYTICAL"))
    english_questions = list(QuestionImages.objects.filter(question_title ="ENGLISH"))
    computer_questions = list(QuestionImages.objects.filter(question_title ="COMPUTER"))
    question_list = []
    if len(math_questions)!=0:
        random.shuffle(math_questions)
        for q in math_questions[:total_math]:
            question_list.append(q)
        examStatus = 1

    if len(analytical_ability_questions)!=0:
        random.shuffle(analytical_ability_questions)
        for q in analytical_ability_questions[:total_analytical_ability]:
            question_list.append(q)
        examStatus = 1

    if len(english_questions)!=0:
        random.shuffle(english_questions)
        for q in english_questions[:total_english]:
            question_list.append(q)
        examStatus = 1

    if len(computer_questions)!=0:
        random.shuffle(computer_questions)
        for q in computer_questions[:total_computer]:
            question_list.append(q)
        examStatus = 1

    if examStatus!=1:
        examStatus = 2  #if no question found

    hr = total_question//60 
    min = total_question%60
    sec = 0
    #1 question 1 min
    timeAllot = total_question
    request.session['NIMCET']  = True
    context = {'questions' : question_list , 
               'examStatus':examStatus ,
               'totalQuestion':total_question,
               'topicName':"NIMCET",
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
    
    if request.session.has_key('NIMCET'):
        NIMCET = True
        right ={
            'MATH':0,
            'ANALYTICAL':0,
            'COMPUTER' :0,
            'ENGLISH':0
        }
        wrong ={
            'MATH':0,
            'ANALYTICAL':0,
            'COMPUTER' :0,
            'ENGLISH':0
        }
        del request.session['NIMCET']

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
                if NIMCET:
                    right[question_img.question_title]+=1
                    
            else:
                total_wrong +=1
                wrong_attempted_ques.append(question_img.question_id)
                if NIMCET:
                    wrong[question_img.question_title]+=1
            
        except:
            pass
   

  
    # finds the set of not_attempted question of the test
    right_and_wrong_que = set(right_attempted_ques).union(set(wrong_attempted_ques))
    qid_list =  set(qid_list)
    setA  = right_and_wrong_que - qid_list
    setB  = qid_list - right_and_wrong_que
    not_attempted_ques = list(setA.union(setB))

    total_attempt = len(right_and_wrong_que)
    print("Total attempted question :")
    print(total_attempt)
    if total_attempt!=0:
        points = (total_right - total_wrong) /  total_attempt *10
    else:
        points = 0
   
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

'''
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

'''
#-----------------------------------------------------------------------------------------------------------
#This view used for Showing test result of each test  by rendering "show_result.html" file
# NOTE:When result will be displayed at that time rating will be updated each question 
def get_difficulty_of_question(questionRating):
    right = questionRating.total_times_right
    wrong = questionRating.total_times_wrong
    total_attempted = right + wrong
    if total_attempted !=0:
        difficulty = (wrong/total_attempted)*100
        return difficulty
    return 0


def showTestResult(request):
    if 'name' not in request.session.keys():
        res = HttpResponseRedirect('login')
    
    #fetch latest result
    results  = Result.objects.filter(result_id = Result.objects.latest('result_id').result_id , username_id = request.session['username'])
    candidates = Candidate.objects.filter(username = request.session['username'])
   
    
    NIMCET_score = results[0].right*4 - results[0].wrong
    context = {'results' : results , 'NIMCET_score':NIMCET_score ,'candidate':candidates[0]}


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
    if len(candidate)!=0:
        points =format(candidate[0].points, ".2f")
        
        context = {'candidate':candidate[0],'points':points ,'results':results }
        res = render(request, 'user_account.html',context)
    else:
        messages.info(request , "Account not found")
        res = HttpResponseRedirect('home')
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
            name = request.POST['name']
            if str(name).isalpha():
                candidate.name = name
                edited = True
            else:
                messages.info(request,"Enter valid Name")
                edited = False

        if len(request.POST['email'])!=0:
            candidate.email = request.POST['email']
            edited = True

        if len(request.POST['contact'])!=0:
            contact_no = request.POST['contact']
            if (not str(contact_no).isnumeric())or len(contact_no)!=10 :
                messages.info(request,"Please Enter valid phone number")
                edited = False
            else:
                candidate.contact_no = contact_no
                edited = True

                

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


def postMessage(request):
    if 'name' not in request.session.keys():
        res = HttpResponseRedirect('login')
    if request.method == 'POST':
        user_message = request.POST['message']
        discuss_room = DiscussRoom()
        user = Candidate.objects.get(username = request.session['username'])
        discuss_room.message = user_message
        discuss_room.username = user
        discuss_room.save()
        print(user_message)
    res =HttpResponseRedirect('show_room_chat')
    return res

def showRoomChat(request):
    if 'name' not in request.session.keys():
        res = HttpResponseRedirect('login')
    discuss_room = DiscussRoom.objects.filter().order_by('-discuss_room_id')[:50][::1]
    context = {
        'room' : discuss_room
    }
    res =render(request ,'discuss_room.html',context)
    return res





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
