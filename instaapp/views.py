from django.template import loader
from django.shortcuts import render, HttpResponse
from .models import *

def index(request):	

	template = loader.get_template('instaapp/main.html')

	context = {	}

	return HttpResponse(template.render(context, request))