from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.urls import reverse, reverse_lazy
from employee.forms import UserForm
from ems.decorators import role_required


def user_login(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if request.GET.get('next', None):
                # checking request.GET have any next value via .get method
                # it takes two arg first the attribute to find and second default value
                # value of next is userful sometimes user come from another url
                # and after successful login we want to return back him to the same url
                return HttpResponseRedirect(request.GET['next'])
            return HttpResponseRedirect(reverse('employee_list'))
        else:
            context['error'] = "Provide valid credentials!"
            return render(request, "auth/login.html", context)
    else:
        return render(request, "auth/login.html", context)


@login_required(login_url='/login/')
def success(request):
    context = {}
    context['user'] = request.user
    return render(request, 'auth/success.html', context)


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_login'))


@login_required(login_url='/login/')
def employee_list(request):
    context = {}
    context['users'] = User.objects.all()
    context['title'] = 'Employees'
    return render(request, 'employee/index.html', context)


@login_required(login_url='/login/')
def employee_details(request, id=None):
    context = {}
    user = get_object_or_404(User, pk=id)

    context['user'] = user
    return render(request, 'employee/details.html', context)


@login_required(login_url='/login/')
@role_required(allowed_roles=["Admin"])
def employee_add(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('employee_list'))
            # reverse method takes a perameter
            # which is the matching name field in the urls.py
            # when it finds the name field it convert that into url
            # Here, reverse('employee_list') -> employee/
        else:
            return render(request, 'employee/add.html', {"user_form": user_form})
    else:
        user_form = UserForm()
        return render(request, 'employee/add.html', {"user_form": user_form})


@login_required(login_url='/login/')
def employee_edit(request, id=None):
    user = get_object_or_404(User, pk=id)
    if request.method == 'POST':
        # passing instance=user means you have to update the data
        # else it is going to create a new row
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('employee_list'))
        else:
            return render(request, 'employee/edit.html', {"user_form": user_form})
    else:
        user_form = UserForm(instance=user)
        return render(request, 'employee/edit.html', {"user_form": user_form})


@login_required(login_url='/login/')
def employee_delete(request, id=None):
    user = get_object_or_404(User, pk=id)
    if request.method == 'POST':
        user.delete()
        return HttpResponseRedirect(reverse('employee_list'))
    else:
        context = {}
        context['user'] = user
        return render(request, 'employee/delete.html', context)


class ProfileUpdate(UpdateView):
    fields = ['designation', 'salary']
    template_name = 'auth/profile_update.html'
    success_url = reverse_lazy('my_profile')

    def get_object(self):
        return self.request.user.employee

class MyProfile(DetailView):
    template_name = 'auth/profile.html'

    def get_object(self):
        return self.request.user.employee