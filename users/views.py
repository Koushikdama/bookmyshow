from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import UserRegisterForm, UserUpdateForm
from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from movies.models import Movie , Booking,Theater
from datetime import datetime
from datetime import datetime, timedelta
from django.shortcuts import render
from movies.models import Movie, Theater

def home(request):
    # Get all movies
    movies = Movie.objects.all()
    
    # Get the current date
    current_date = datetime.now().date()

    # Query theaters for shows happening today
    todays_shows = Theater.objects.filter(time__date=current_date)
    print("todays_shows", todays_shows)

    # Calculate tomorrow's date
    tomorrow_date = current_date + timedelta(days=1)

    # Filter the shows for tomorrow's date
    tomorrow_shows = Theater.objects.filter(time__date=tomorrow_date)
    print("tomarrow", tomorrow_shows)

    # Extract movies from the shows
    movies_with_shows_today = Movie.objects.filter(theaters__in=todays_shows).distinct()
    movies_with_shows_tomorrow = Movie.objects.filter(theaters__in=tomorrow_shows).distinct()
    
    print("movies_with_shows_today", movies_with_shows_today)
    for i in movies_with_shows_today:
        print("iii", i.name)
    
    # Pass the data to the template
    return render(request, 'home.html', {
        'movies': movies,
        'todat_shows': movies_with_shows_today,
        
    })

def register(request):
    if request.method == 'POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password1')
            user=authenticate(username=username,password=password)
            login(request,user)
            return redirect('profile')
    else:
        form=UserRegisterForm()
    return render(request,'users/register.html',{'form':form})

def login_view(request):
    if request.method == 'POST':
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect('/')
    else:
        form=AuthenticationForm()
    return render(request,'users/login.html',{'form':form})

@login_required
def profile(request):
    bookings= Booking.objects.filter(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)

    return render(request, 'users/profile.html', {'u_form': u_form,'bookings':bookings})

@login_required
def reset_password(request):
    if request.method == 'POST':
        form=PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form=PasswordChangeForm(user=request.user)
    return render(request,'users/reset_password.html',{'form':form})