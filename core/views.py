from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .forms import LoginForm
from django.contrib.auth import authenticate,update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import pandas as pd
from . models import CheckIn, Profile, Course, Class,Event
from .forms import CourseForm, EventForm, ClassForm,ChangePasswordForm,UsernameChangeForm,EmailChangeForm,CheckInForm
from django.http import HttpRequest
from math import radians, sin, cos, sqrt, atan2



def index(request):
    context = {
        'title': 'WhereAreYou',
    }
    return render(request, 'core/index.html', context)

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                # Create the user
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
                
                # Create the profile for the user
                Profile.objects.create(user=user)
                
                messages.success(request, 'Account created successfully. Please log in.')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')
    else:
        return render(request, 'core/signup.html')
    
@login_required
def edit_profile(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    
    return render(request, 'core/edit_profile.html', {'profile': profile})

@login_required
def change_username(request, username):
    user = request.user
    if request.method == 'POST':
        form = UsernameChangeForm(request.POST, instance=user)
        if form.is_valid():
            new_username = form.cleaned_data['username']
            if User.objects.filter(username=new_username).exclude(pk=user.pk).exists():
                messages.error(request, 'Username is already taken. Please choose a different one.')
            else:
                form.save()
                return redirect('edit_profile', username=username)
    else:
        form = UsernameChangeForm(instance=user)
    return render(request, 'core/change_username.html', {'form': form})

@login_required
def change_email(request, username):
    user = request.user
    if request.method == 'POST':
        form = EmailChangeForm(request.POST, instance=user)
        if form.is_valid():
            new_email = form.cleaned_data['email']
            if User.objects.filter(email=new_email).exclude(pk=user.pk).exists():
                messages.error(request, 'Email is already taken. Please choose a different one.')
            else:
                form.save()
                return redirect('edit_profile', username=username)
    else:
        form = EmailChangeForm(instance=user)
    return render(request, 'core/change_email.html', {'form': form})


@login_required
def change_password(request, username):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(user, request.POST)
        if form.is_valid():
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            if password1 == password2:
                user = form.save()
                update_session_auth_hash(request, user)  # Important to maintain session
                messages.success(request, 'Your password was successfully updated!')
                return redirect('edit_profile', username=username)
            else:
                messages.error(request, 'Passwords do not match')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ChangePasswordForm(user)
    return render(request, 'core/change_password.html', {'form': form})
    
@login_required
def delete_profile(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    if request.method == 'POST':
        profile.delete()
        messages.success(request, 'Profile and all related data deleted successfully.')
        return redirect('signup')
    return render(request, 'core/delete_profile.html', {'profile': profile})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                # Retrieve the Profile instance for the authenticated user
                try:
                    profile = Profile.objects.get(user=user)
                except Profile.DoesNotExist:
                    # Handle the case where profile does not exist (create if necessary)
                    profile = Profile.objects.create(user=user)
                # Redirect to 'home' passing the username as an argument
                return redirect('home', username=profile.user.username)
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})

@login_required
def log_out(request, username):
    if request.method == 'POST':
        auth_logout(request)
        return redirect('login')
    return render(request, 'core/log_out.html')

# @login_required
# def home(request, username):
#     print(username)
#     user = User.objects.get(username='bmwdoame')

def home(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user__username=username)
    courses = Course.objects.filter(lecturer_profile=profile)
    context = {'profile': profile, 'courses': courses}
    return render(request, 'core/home.html', context)

def add_course(request, username):
    profile = Profile.objects.get(user__username=username)
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course_name = form.cleaned_data['name']
            if Course.objects.filter(name=course_name, lecturer_profile=profile).exists():
                messages.error(request, f'A course with the name "{course_name}" already exists for your profile.')
            else:
                course = form.save(commit=False)
                course.lecturer_profile = profile
                course.save()
                messages.success(request, f'Course "{course_name}" created successfully.')
                return redirect('home', username=username)
    else:
        form = CourseForm()
    return render(request, 'core/add_course.html', {'form': form})

@login_required
def delete_course(request, username, coursename):
    profile = get_object_or_404(Profile, user__username=username)
    course = get_object_or_404(Course, name=coursename, lecturer_profile=profile)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course and all related data deleted successfully.')
        return redirect('home', username=username)
    return render(request, 'core/delete_course.html', {'course': course})

# def view_event(request, event_id):
#     event = Event.objects.get(event_id=event_id)
#     context =  {'event': event}
#     return render(request, 'core/view_event.html', context)

@login_required
def view_course(request, username, coursename):
    profile = Profile.objects.get(user__username=username)
    course = get_object_or_404(Course, name=coursename, lecturer_profile=profile)
    classes = Class.objects.filter(course=course)
    return render(request, 'core/view_course.html', {'course': course, 'classes': classes})

# Class Views
def add_class(request, username, coursename):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            course = get_object_or_404(Course, name=coursename)
            class_name = form.cleaned_data['class_name']
            if Class.objects.filter(course=course, class_name=class_name).exists():
                messages.error(request, 'A class with this name already exists for this course.')
            else:
                form.instance.course = course
                
                form.save()
                return redirect('view_course', username=username, coursename=coursename)
    else:
        form = ClassForm()
    return render(request, 'core/add_class.html', {'form': form})

@login_required
def delete_class(request, username, coursename, classname):
    class_obj = get_object_or_404(Class, course__name=coursename, class_name=classname)
    if request.method == 'POST':
        class_obj.delete()
        messages.success(request, 'Class and all related data deleted successfully.')
        return redirect('view_course', username=username, coursename=coursename)
    return render(request, 'core/delete_class.html', {'class_obj': class_obj})

def view_class(request: HttpRequest, username, coursename, classname):
    print(coursename)
    # Get the class based on username, coursename, and classname
    #profile = Profile.objects.get(user__username=username)
    class_obj = get_object_or_404(Class, course__name=coursename, class_name=classname)
    events = class_obj.event_set.all()  # Get all events related to this class
    context =  {'class': class_obj, 'events': events, 'coursename':coursename}
    return render(request, 'core/view_class.html', context)


# Event views 
def add_event(request, username, coursename, classname):
    profile = Profile.objects.get(user__username=username)
    class_obj = Class.objects.get(course__name=coursename, class_name=classname)
    course = Course.objects.get(name=coursename, lecturer_profile=profile)

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.related_class = class_obj
            event.location_address = form.cleaned_data['location_address']
            event.checkpoint_lat = request.POST.get("checkpoint_lat")
            event.checkpoint_lng = request.POST.get("checkpoint_lng")
            # Assign the class name and course name from the class object
            event.save()
            # Redirect to the 'view_class' URL with appropriate parameters
            return redirect('view_class', username=username, coursename=coursename, classname=classname)
        else:
            messages.error(request, 'Please check at least one box.')
    else:
        form = EventForm()

    return render(request, 'core/add_event.html', {'form': form, 'course': course})


@login_required
def delete_event(request, username, coursename, classname, event_id):
    event = get_object_or_404(Event, pk=event_id, related_class__course__name=coursename, related_class__class_name=classname)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully.')
        return redirect('view_class', username=username, coursename=coursename, classname=classname)
    return render(request, 'core/delete_event.html', {'event': event})

# event/views.py
def calculate_distance(lat1, lon1, lat2, lon2):

    R = 6371.0  # Radius of the Earth in kilometers
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance

def check_in(request, username, coursename, classname, event_id):
    event = get_object_or_404(Event, pk=event_id, related_class__course__lecturer_profile__user__username=username, related_class__course__name=coursename, related_class__class_name=classname)

    current_time = timezone.now()
    if current_time < event.start_time:
        return render(request, 'core/check_in_not_allowed.html', {'message': 'The event has not started yet.'})
    elif current_time > event.end_time:
        return render(request, 'core/check_in_not_allowed.html', {'message': 'The event has already ended.'})

    if request.method == 'POST':
        form = CheckInForm(request.POST)
        if form.is_valid():
            attendee_lat = float(request.POST['latitude'])
            attendee_lng = float(request.POST['longitude'])

            distance = calculate_distance(event.checkpoint_lat, event.checkpoint_lng, attendee_lat, attendee_lng)

            if distance <= event.radius:
                if event.is_student_id_required:
                    student_id = form.cleaned_data['student_id']
                else:
                    student_id = None
                if event.is_index_number_required:
                    index_number = form.cleaned_data['index_number']
                else:
                    index_number = None
                if event.is_student_name_required:
                    student_name = form.cleaned_data['student_name']
                else:
                    student_name = None

                CheckIn.objects.create(
                    event=event,
                    student_id=student_id,
                    index_number=index_number,
                    student_name=student_name
                )

                return render(request, 'core/check_in_success.html')
            else:
                return render(request, 'core/check_in_not_allowed.html', {'message': 'You are not within the radius of the event.'})
    else:
        form = CheckInForm()

    return render(request, 'core/check_in.html', {
        'form': form,
        'event': event,
        'is_student_id_required': event.is_student_id_required,
        'is_index_number_required': event.is_index_number_required,
        'is_student_name_required': event.is_student_name_required,
    })
    
def check_in_not_allowed(request):
    return render(request, 'core/check_in_not_allowed.html', {})


@login_required
def view_event(request, username, coursename, classname, event_id):
    event = get_object_or_404(Event, pk=event_id, related_class__course__name=coursename, related_class__class_name=classname)
    check_ins = CheckIn.objects.filter(event=event)

    context = {
        'event': event,
        'check_ins': check_ins,
        'is_student_id_required': event.is_student_id_required,
        'is_index_number_required': event.is_index_number_required,
        'is_student_name_required': event.is_student_name_required,
    }
    

    return render(request, 'core/view_event.html', context)

