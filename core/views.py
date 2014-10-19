from django.shortcuts import render
from .models import File
import os

def home(request):
	pdf = File.objects.all()[0]
	print str(pdf.file)[7:]
	command = 'cd ;cd projetos/slides/converter/media/photos;mkdir %s;cp %s teste;cd teste;convert %s *.jpg; rm %s' % ( (str(pdf.file)[7:-4] + 'dir'), str(pdf.file)[7:], str(pdf.file)[7:], str(pdf.file)[7:])
	#os.system(command)
	print command
	context = {'range': range(41)}
	template = "home.html"
	return render(request, template, context)