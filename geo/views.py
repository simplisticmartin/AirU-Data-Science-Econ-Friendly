
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import *
from .models import *
from django.core.mail import send_mail

def arrayToText(array):
    str = ""
    for x in array:
        str = str + x + ", "
    print(str)
    return str[0:-2]

def basic(request):
    """ Homepage """
    if request.method == 'POST':
        form = NewStudentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            netid = (form.cleaned_data['netid']).strip()
            if NewStudent.objects.filter(netid=netid).count() > 0:
                return HttpResponseRedirect('/error_exists/')
            # hometown = form.cleaned_data['hometown']
            year = form.cleaned_data['year']
            school = form.cleaned_data['school']
            major = form.cleaned_data['major']
            minor = form.cleaned_data['minor']
            extracurriculars = form.cleaned_data['extracurriculars']
            extra_sa = form.cleaned_data['extra_sa']
            if extra_sa == '':
                extra_sa = "None"
            career = form.cleaned_data['career']
            career_sa = form.cleaned_data['career_sa']
            if career_sa == '':
                career_sa = "None"
            print(career_sa)
            sa1 = form.cleaned_data['sa1']
            sa2 = form.cleaned_data['sa2']
            sa3 = form.cleaned_data['sa3']
            survey = form.cleaned_data['survey']
            heard = form.cleaned_data['heard']
            participated = form.cleaned_data['participated']
            partnering = form.cleaned_data['partnering']
            student = NewStudent(name = name,
                    netid = netid,
                    # hometown = hometown,
                    year = year,
                    college = school,
                    major = major,
                    minor = minor,
                    extracurricular = arrayToText(extracurriculars),
                    extra_sa = extra_sa,
                    career = arrayToText(career),
                    career_sa = career_sa,
                    sa1 = sa1,
                    sa2 = sa2,
                    sa3 = sa3,
                    partnering = partnering,
                    survey = arrayToText(survey),
                    participated = participated,
                    heard = heard,
                    )
            student.save()
            mail_title = 'Let\'s Get Coffee: Thanks!'
            message = '''Thanks for completing the New Students survey! You may wish to familiarize yourself with the schedule here: http://www.letsgetcoffeecornell.com/timeline/. \n Please be on the lookout for an email once an upperclassman has selected you. If you don't get one by Feb. 10th, please let us know. '''
            email = 'Let\'s Get Coffee<letsgetcoffeecornell@gmail.com>'
            recipients = [student.netid + '@cornell.edu']
            send_mail(mail_title, message, email, recipients)
            return HttpResponseRedirect('/thanks_newstudent/')
    else:
        form = NewStudentForm()
    return render(request, 'newstudent/basic.html', {
        'form' : form,
        'request' : request, })

#For closed state
def newstudent_closed(request):
    return render(request, 'newstudent_closed.html', {
        'request' : request, })
