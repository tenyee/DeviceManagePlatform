from django.http import HttpResponse
from django.shortcuts import render

def Hello(request):
	return HttpResponse("1234")	

def Index(request):
	return render(request, 'index.html')