from django.contrib.auth import login
from .forms import SignUpForm  # Import custom form
from django.shortcuts import render, redirect
from django.contrib import messages

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)  # Use SignUpForm
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to The Truth Gate, {user.first_name}!") # Use First Name
            
            # Smart Redirect (Handle 'next' parameter)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('home')
    else:
        form = SignUpForm()  # Use SignUpForm
    return render(request, 'accounts/signup.html', {'form': form})
