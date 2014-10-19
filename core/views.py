from django.shortcuts import render
from .models import File
import os, subprocess

def home(request):
	pdf = File.objects.all()[0]
	print str(pdf.file)[7:]
	#ainda falta criar pasta para cada slide
	comando = 'cd ;cd projetos/slides/converter/media/photos;cp %s ../../templates/assets/img;cd ../../templates/assets/img;convert %s *.jpg; rm %s' % (str(pdf.file)[7:], str(pdf.file)[7:], str(pdf.file)[7:])
	os.system(comando)
	contador_arquivos = subprocess.check_output("cd; cd projetos/slides/converter/templates/assets/img; ls | wc -l", stderr=subprocess.STDOUT, shell=True)
	context = {'range': range(int(contador_arquivos))}
	template = "home.html"
	return render(request, template, context)