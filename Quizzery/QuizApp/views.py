from django import template
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib.auth import views as auth_views
from django.contrib import messages
from datetime import datetime
import pytz
utc = pytz.UTC

# Create your views here.


def register(request):
    print(1)
    if request.method == 'POST':
        print(2)
        namer = request.POST['user_name']
        passwordr = request.POST['password']
        emailr = request.POST['email']
        a = len(UserTable.objects.filter())
        user_idr = a+1
        if len(UserTable.objects.filter(name=namer)) > 0:
            return HttpResponse('User already exist')
        if len(UserTable.objects.filter(email=emailr)) > 0:
            return HttpResponse('User already exist')
        UserTable.objects.create(name=namer, password=passwordr, email=emailr, user_id=user_idr)
        return redirect('/login/')

    return render(request, 'registration.html')


def login(request):
    if request.method == 'POST':
        namer = request.POST['user_name']
        passwordr = request.POST['password']
        data = UserTable.objects.filter(name=namer)
        if not data:
            return HttpResponse('User does not exist try again.')
        # print(data)
        # for x in data:
        #     print(x.password)

        p = 0
        for x in data:
            if x.password != passwordr:
                return HttpResponse('Incorrect password')
            p = x.user_id
        request.session['user_id'] = p
        return redirect('home/')
    return render(request, 'login.html')


def home(request):
    # user_id=request.GET['p']
    # print(user_id)
    return render(request, 'home.html')


def dashboard(request):
    if request.method == "GET":
        template = 'dashboard.html'
        quiz_id = request.GET['quiz_id']
        data = QuizExamTable.objects.filter(quiz_id=quiz_id)
        data1=QuizTable.objects.filter(quiz_id=quiz_id)
        context = {
            'leaderboard': data,
            'quiz':data1
        }
        return render(request, template, context)

def changeend(request):
    print(datetime.now())
    if request.method=="GET":
        template = 'dashboard.html'
        quiz_id = request.GET['quiz_id']
        data = QuizExamTable.objects.filter(quiz_id=quiz_id)
        QuizTable.objects.filter(quiz_id=quiz_id).update(end_time=datetime.now())
        data1 = QuizTable.objects.filter(quiz_id=quiz_id)
        
        context = {
            'leaderboard': data,
            'quiz': data1
        }
        return render(request, template, context)



def hometaker(request):
    data = QuizTable.objects.filter(public=True)
    context = {
        'quizzes': data
    }
    return render(request, 'hometaker.html', context)


def upcomingtaker(request):
    return render(request, 'upcomingtaker.html')


def index(request):
    return render(request, 'index.html')


def oldquizzes(request):
    data = QuizTable.objects.filter(user_id=request.session['user_id'])
    print(len(data))
    context = {
        'quizzes': data
    }
    return render(request, 'oldquizzes.html', context)


def form(request):
    if request.method == "POST":
        quiz_name = request.POST["quiz Name"]
        quiz_descr = request.POST["description"]
        start_timer = request.POST["start time"]
        end_timer = request.POST["end time"]
        total_time = request.POST["quiz time"]
        # hh=int(total_time)//60
        # if hh<10:
        #     hh='0'+str(hh)
        # mm=int(total_time)%60
        # if mm<10:
        #     mm='0'+str(hh)
        # ss='00'
        # timee=str(hh)+':'+str(mm)+':'+ss
        # ttime = datetime.strftime(timee, '%H:%M:%S')
        if request.POST["exampleRadios"] == 'option1':
            publicr = True
        else:
            publicr = False
        a = len(QuizTable.objects.all())
        r = UserTable.objects.get(user_id=request.session['user_id'])

        quiz_idr = a+1
        request.session['quiz_id'] = quiz_idr
        QuizTable.objects.create(quizname=quiz_name, quiz_id=quiz_idr, start_time=start_timer, quiz_desc=quiz_descr,
                                 end_time=end_timer, quiz_time=total_time, public=publicr, user_id=r)
        return redirect('creatingquestions/')
    current_datetime = datetime.now()
    c = str(current_datetime)[:10]+'T'+str(current_datetime)[11:16]
    print(c)
    context = {
        'datetime': c
    }

    return render(request, 'form.html', context)


def creatingquestions(request):
    if request.method == "POST":
        p = len(QuestionsTable.objects.filter(
            quiz_id=request.session['quiz_id']))
        questionr = request.POST['question']
        option_1r = request.POST['option_1']
        option_2r = request.POST['option_2']
        option_3r = request.POST['option_3']
        option_4r = request.POST['option_4']
        answerr = request.POST['exampleRadios']
        c = QuizTable.objects.get(quiz_id=request.session['quiz_id'])
        QuestionsTable.objects.create(question=questionr, quiz_id=c, option_1=option_1r, question_no=p+1,
                                      option_2=option_2r, option_3=option_3r, option_4=option_4r,  answer=answerr)

        data = {
            'question_no': p+2
        }
        return render(request, 'creatingquestions.html', data)
    data = {
        'question_no': 1
    }
    return render(request, 'creatingquestions.html', data)


def upcoming(request):
    return render(request, 'upcomingmaker.html')


def quiz(request):
    # x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    # if x_forwarded_for:
    #     ip = x_forwarded_for.split(',')[0]
    # else:
    #     ip = request.META.get('REMOTE_ADDR')
    date = datetime.now()
    if request.method == 'GET':

        template = "quiz.html"
        var = request.GET['quiz_id']
        p = QuizExamTable.objects.filter(quiz_id=var)
        c= QuizTable.objects.filter(quiz_id=var)
        for x in c:
            s=str(x.start_time)
            e=str(x.end_time)
            print(s)
            print(e)
            print(date)
            date1=str(date)
            sy=int(s[:4])
            sm=int(s[5:7])
            sd=int(s[8:10])
            sh=int(s[11:13])
            ss=int(s[14:16])
            ey = int(e[:4])
            em = int(e[5:7])
            ed = int(e[8:10])
            eh = int(e[11:13])
            es = int(e[14:16])
            dy = int(date1[:4])
            dm = int(date1[5:7])
            dd = int(date1[8:10])
            dh = int(date1[11:13])
            ds = int(date1[14:16])
            print(sy,sm,sd,sh,ss,ey,em,ed,eh,ed,dy,dm,dd,dh,ds)
            if (sy>dy or sm>dm or sd>dd) :
                
                return HttpResponse('Quiz not Started')
            if sy==dy or sm==dm or sd==dd: 
                if (sh >= dh and ss > ds):
                    return HttpResponse('Quiz not Started')

            if (ey<dy or em<dm or ed<dd) :
                data = QuizExamTable.objects.filter(quiz_id=var)
                context = {
                   'leaderboard': data
                   }
                return render(request, 'userdashboard.html', context)
            if (ey==dy or em==dm or ed==dd) :
                if (eh <= dh and es < ds):
                    data1 = QuizExamTable.objects.filter(quiz_id=var)
                    context = {
                    'leaderboard': data1
                }
                    return render(request, 'userdashboard.html', context)

        #     start_time = x.start_time.replace(tzinfo=utc)

        #     end_time = x.end_time.replace(tzinfo=utc)
        #     # x.start_time = utc.localize(x.start_time)

        #     # x.end_time = utc.localize(x.end_time)
        #     if end_time <= datetime.now():
        #         data = QuizExamTable.objects.filter(quiz_id=var)
        #         context = {
        #             'leaderboard': data
        #         }
        #         return render(request, 'userdashboard.html', context)
        #     if start_time >= datetime.now():
        #         return HttpResponse('Quiz not Started')



        for x in p:
            if x.ipaddress == '127.0.0.1' :
                # score = x.score
                # name = x.quiz_username
                # data = QuestionsTable.objects.filter(
                #     quiz_id=request.session['quiz_id'])
                # data1 = {
                #     'questions': data
                # }
                # total = len(data1['questions'])
                # percentage = (score/total)*100
                # incorrect = total-score
                # data3 = {
                #     'total': total,
                #     'score': score,
                #     'percentage': percentage,
                #     'incorrect': incorrect

                # }
                
                data = QuizExamTable.objects.filter(quiz_id=var)
                context = {
                        'leaderboard': data
                        }
                return render(request, 'userdashboard.html', context)
        request.session['quiz_id'] = var
        data = QuestionsTable.objects.filter(quiz_id=var)
        data4 = QuizTable.objects.filter(quiz_id=var)

        context = {
            'questions': data,
            'quiz': data4,
            'date':date
        }

        return render(request, template, context)
    else:
        name = request.POST['user_name']
        quiz_id = request.session['quiz_id']
        data = QuestionsTable.objects.filter(
            quiz_id=request.session['quiz_id'])
        data1 = {
            'questions': data
        }
        r = QuizTable.objects.get(quiz_id=quiz_id)
        scorer = 0
        total = len(data1['questions'])
        for f in data1['questions']:
            a = f.question
            x = 0
            answer = request.POST[a]
            if answer == f.answer:
                scorer += 1
                x = 1
            QuestionAnswerTable.objects.create(
                question=a, quiz_id=r, quiz_username=name, answer=answer, score=x)
        percentage = (scorer/total)*100
        res = "{:.2f}".format(percentage)
        incorrect = total-scorer
        data3 = {
            'total': total,
            'score': scorer,
            'percentage': res,
            'incorrect': incorrect,
            'quiz_id':r

        }
        QuizExamTable.objects.create(
            quiz_id=r, quiz_username=name, ipaddress='127.0.0.1', time_of_joining=date, score=scorer)
        return render(request, 'resulttaker.html', data3)


def gotoquiz(request):

    data = QuestionsTable.objects.filter(quiz_id=request.session['quiz_id'])
    data2 = QuizTable.objects.filter(quiz_id=request.session['quiz_id'])
    data1 = {
        'questions': data,
        'quiz': data2
    }
    if request.method == "POST":
        score = 0
        total = len(data1['questions'])
        for q in data1['questions']:
            a = q.question
            answer = request.POST[a]
            if answer == q.answer:
                score += 1
        percentage = (score/total)*100
        res = "{:.2f}".format(percentage)
        incorrect = total-score
        data3 = {
            'total': total,
            'score': score,
            'percentage': res,
            'incorrect': incorrect,
            'quiz': request.session['quiz_id']

        }
        return render(request, 'result.html', data3)

    return render(request, 'gotoquiz.html', data1)
