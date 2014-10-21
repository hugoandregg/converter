from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from .models import File
from .forms import FileForm

import os, subprocess

def home(request):
	pdf = File.objects.all()[0]
	print str(pdf.file)#[7:]
	#ainda falta criar pasta para cada slide
	comando = 'cd ;cd projetos/slides/converter/media/photos;cp %s ../../templates/assets/img;cd ../../templates/assets/img;convert %s *.jpg; rm %s' % (str(pdf.file)[7:], str(pdf.file)[7:], str(pdf.file)[7:])
	#os.system(comando)
	contador_arquivos = subprocess.check_output("cd; cd projetos/slides/converter/templates/assets/img; ls | wc -l", stderr=subprocess.STDOUT, shell=True)
	context = {'range': range(int(contador_arquivos))}
	template = "home.html"
	return render(request, template, context)

@login_required
def index(request):
	user = request.user

	#chama a funcao para converter o arquivo
	if request.session.get('conv', True):
		try: #se nao existir nenhum objeto, daria problema
			slide = user.file_set.all()[user.file_set.count()-1]
		except:
			slide = None
		if slide:
			username = request.user.username
			converter(request, username, slide.titulo, str(slide.file))
			request.session['conv'] = False

	slides = File.objects.filter(user=user)
	context = {'slides': slides, 'user': user}
	template = "index.html"
	return render(request, template, context)

@login_required
def create(request):
	user = request.user
	form = FileForm(request.POST, request.FILES)
	if form.is_valid():
		titulo = form.cleaned_data['titulo']
		file = form.cleaned_data['file']
		novo_slide = File(
			user=user,
			titulo=titulo,
			file=file
			)
		novo_slide.save(force_insert=True)

		#como nao da certo converter ja nessa funcao, criei uma variavel global para ser verificada no index
		conv = request.session.get('conv')
		if not conv:
			conv = True
		request.session['conv'] = conv
		return HttpResponseRedirect("/")

	return render(request, "create.html", {"form":form})


def converter(request, username, titulo, slide):
	if slide:
		comando = '''cd templates/assets/img/%s;mkdir %s ;cd ../../../../media/photos;
			cp %s ../../templates/assets/img/%s/%s;
			cd ../../templates/assets/img/%s/%s;
			convert %s *.jpg; rm %s''' % (username, titulo, str(slide[7:]), username, titulo, username, titulo, str(slide[7:]), str(slide[7:]))
		os.system(comando)
		
	return HttpResponseRedirect("/")

@login_required
def delete(request, slide):
	user = request.user
	file = user.file_set.get(titulo=slide)
	file.delete()

	username = request.user.username
	comando = "cd templates/assets/img/%s;rm -rf %s" % (username, slide)
	os.system(comando)

	return HttpResponseRedirect("/")


#def show(request, user, slide): #publico
	
#def publicindex(request, user): #publico