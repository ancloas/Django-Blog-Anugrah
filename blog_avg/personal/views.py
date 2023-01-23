from django.shortcuts import render
from personal.models  import Question
# Create your views here.
def home_screen_view(request):
    context={}
    context['some_string']= "this is some string that i am passing to view"
    
    question_list=Question.objects.all();
    context['question_list']=question_list


    return render(request, 'personal/home.html',context)