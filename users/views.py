from django.shortcuts import render , redirect
from django.views.generic import (ListView, CreateView, DeleteView, UpdateView)
from .forms import UserRegisterForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages



from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f' Your Account  has been created Successfully @ {username} !')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    user = request.user
    profile = user.profile

    context = {
        'user': user,
        'profile': profile
    }    

    return render(request, 'users/profile.html', context)








