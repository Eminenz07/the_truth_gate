from django.contrib.auth import login
from .forms import SignUpForm  # Import custom form
from django.shortcuts import render, redirect
from django.contrib import messages

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)  # Use SignUpForm
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            # User requested no welcome toast, homepage is enough
            
            # Newsletter Subscription Logic
            if form.cleaned_data.get('subscribe_newsletter'):
                from core.models import NewsletterSubscriber
                NewsletterSubscriber.objects.get_or_create(email=user.email)
            
            # Smart Redirect (Handle 'next' parameter)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('home')
    else:
        form = SignUpForm()  # Use SignUpForm
    return render(request, 'accounts/signup.html', {'form': form})
