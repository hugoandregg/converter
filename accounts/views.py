from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from accounts.forms import RegistrationForm
import os

def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    else:
       return HttpResponseRedirect("/explore")
def create_user(request):
    if not request.user.is_authenticated():
        form = RegistrationForm(request.POST or None)

        if request.method == "POST" and form.is_valid():
            form.save()

            user = authenticate(username=form.cleaned_data["username"],
                    password=form.cleaned_data["password1"])
            login(request, user)

            comando = "cd templates/assets/img; mkdir %s" % user.username
            os.system(comando)
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")

    return render(request, "registration/create.html", {
        "form": form,
    })