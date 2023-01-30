from django.shortcuts import render
from account.models import Account
# Create your views here.
def home_screen_view(request):
    context={}
    context['some_string']= "this is some string that i am passing to view"
    accounts=Account.objects.all();
    context['account_list']=accounts


    return render(request, 'personal/home.html',context)