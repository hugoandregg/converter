from django.shortcuts import render
from .models import File
import os

def home(request):
	pdf = File.objects.all()[0]
	print str(pdf.file)[7:]
	your_command = 'cd ;cd projetos/slides/slides/media/photos;cp %s teste;cd teste;convert %s *.jpg; rm %s' % (str(pdf.file)[7:], str(pdf.file)[7:], str(pdf.file)[7:])
	os.system(your_command)
	context = {}
	template = "home.html"
	return render(request, template, context)