from django.contrib import messages
from django.contrib.auth import \
    authenticate  # checa se o usuário vai ou nao autenticar
from django.contrib.auth import login, logout  # loga o usuário
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import LoginForm, RegisterForm


# Create your views here.
def registerview(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)

    return render(request, 'authors/pages/register_view.html', {
        'form': form,
    })


def registercreate(request):
    if not request.POST:
        raise Http404

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Usuário cadastrado')
        del (request.session['register_form_data'])
        return redirect(reverse('authors:login'))

    return redirect('authors:register')


def login_view(request):
    form = LoginForm()
    if (request.user.is_authenticated):
        return redirect(reverse('authors:dashboard'))
    else:

        return render(request, 'authors/pages/login.html', {
            'form': form,
            'form_action': reverse('authors:login_create')
        })


def login_create(request):
    if not request.POST:
        raise Http404
    form = LoginForm(request.POST)
    if form.is_valid():
        is_authenticated = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )
        if is_authenticated is not None:
            messages.success(request, 'Login bem sucedido')
            login(request, is_authenticated)
        else:
            messages.error(request, 'Login não autorizado')
    else:
        messages.error(request, 'Login não autorizado')
    return redirect(reverse('authors:dashboard'))


@login_required(login_url='authors:login', redirect_field_name='next')
def logoutAA(request):
    logout(request)
    return redirect(reverse('authors:login'))


@login_required(login_url='authors:login', redirect_field_name='next')
def Dashboard(request):
    return render(request, 'authors/pages/dashboard.html')
