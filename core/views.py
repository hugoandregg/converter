from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.views.static import serve

from .models import File
from .forms import FileForm

import os, subprocess


@login_required
def index(request):
	user = request.user
	slides = File.objects.filter(user=user)
	context = {'slides': slides, 'user': user}
	template = "core/index.html"
	return render(request, template, context)

@login_required
def createSlide(request):
	user = request.user
	form = FileForm(request.POST, request.FILES)
	if form.is_valid():
		titulo = form.cleaned_data['titulo']
		titulo = titulo.replace(" ", "_")
		file = form.cleaned_data['file']
		novo_slide = File(
			user=user,
			titulo=titulo,
			file=file
			)
		novo_slide.save(force_insert=True)

		converter(request, user.username, novo_slide.titulo, str(novo_slide.file))

		return HttpResponseRedirect("/slides/")

	return render(request, "core/create.html", {"form":form})


def converter(request, username, titulo, slide):
	if str(slide[-3:]) == "ppt" or "pdf":
		if str(slide[-3:]) == "ppt":
			comando = 'cd media/photos ;unoconv -f pdf %s.ppt' % str(slide[7:-4])
			os.system(comando)

			novo_slide = File.objects.order_by('-pk')[0]
			novo_slide.file = 'photos/%s.pdf' % str(slide[7:-4])
			novo_slide.save() 

			comando = 'cd media/photos ;rm %s.ppt' % str(slide[7:-4])
			os.system(comando)

			slide = str(novo_slide.file)

		comando = "cd media/photos ;zip %s.zip %s.pdf" % (username, str(slide[7:-4]))
		os.system(comando)

		comando = '''cd templates/assets/img/%s;mkdir %s ;cd ../../../../media/photos;
			cp %s ../../templates/assets/img/%s/%s;
			cd ../../templates/assets/img/%s/%s;
			convert %s *.jpg; rm %s''' % (username, titulo, str(slide[7:]), username, titulo, username, titulo, str(slide[7:]), str(slide[7:]))
		os.system(comando)
		
	return HttpResponseRedirect("/slides/")

@login_required
def delete(request, slide):
	user = request.user
	file = user.file_set.get(titulo=slide)

	username = request.user.username
	comando = "cd templates/assets/img/%s;rm -rf %s" % (username, file.titulo)
	os.system(comando)

	comando = "cd media/photos ;zip --delete %s.zip %s.pdf" % (username, str(file.file.name[7:-4])) 
	os.system(comando)

	file.delete()

	return HttpResponseRedirect("/slides/")

def show(request, username, slide): #publico
	usuario = User.objects.get(username=username)
	verifica_slide = usuario.file_set.get(titulo=slide)
	if usuario and verifica_slide:
		caminho = "%s/%s" % (username, slide)
		contador_arquivos = subprocess.check_output("cd templates/assets/img/%s/;ls | wc -l" % caminho, stderr=subprocess.STDOUT, shell=True)
		contador_arquivos = int(contador_arquivos)
		slides_relacionados = usuario.file_set.filter()[:3]

		context = {'range': range(contador_arquivos), 'caminho': caminho, 'user': usuario, 'slide': verifica_slide, 'slides_relacionados': slides_relacionados}
		template = "core/show.html"
		return render(request, template, context)
	else:
		return HttpResponseRedirect("/slides/")

def showProfile(request, username): #publico
	usuario = User.objects.get(username=username)
	if usuario:
		slides = usuario.file_set.all()
		context = {'slides': slides, 'user': usuario}
		template = "core/showProfile.html"
		return render(request, template, context)
	else:
		return HttpResponseRedirect("/")		


def download(request, username, slide): #publico
	usuario = User.objects.get(username=username)
	verifica_slide = usuario.file_set.get(titulo=slide)
	if usuario and verifica_slide:
		filepath = 'media/%s' % verifica_slide.file
		return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
	else:
		return HttpResponseRedirect("/slides/")

def downloadZip(request, username):
	usuario = User.objects.get(username=username)
	if usuario:
		filepath = 'media/photos/%s.zip' % usuario.username
		return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
	else:
		return HttpResponseRedirect("/slides/")
