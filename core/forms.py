from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm,UserChangeForm
from django.core.exceptions import ValidationError
from .models import Course, Event, Class

class SignUpForm(UserCreationForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1','password2']
        
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your first name',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your last name',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your email address',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

    
    
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter your password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat your password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        

class UsernameChangeForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'New username',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

    class Meta:
        model = User
        fields = ('username',)

# forms.py



from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class EmailChangeForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your new email address',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        new_email = self.cleaned_data['email']
        if User.objects.filter(email=new_email).exists():
            raise ValidationError("This email address is already registered.")
        return new_email


class ChangePasswordForm(PasswordChangeForm):
    password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your new password',
            'class': 'w-full py-4 px-6 rounded-xl'
        })
    )
    
    password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm your new password',
            'class': 'w-full py-4 px-6 rounded-xl'
        })
    )


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter your password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name']
        
    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'The course name',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))    
    
    
class EventForm(forms.ModelForm):
    # Define custom validation method
    def clean(self):
        cleaned_data = super().clean()
        is_student_id_required = cleaned_data.get('is_student_id_required')
        is_index_number_required = cleaned_data.get('is_index_number_required')
        is_student_name_required = cleaned_data.get('is_student_name_required')

        # Check if at least one checkbox is selected
        if not any([is_student_id_required, is_index_number_required, is_student_name_required]):
            raise forms.ValidationError("Please select at least one checkbox.")

        return cleaned_data

    class Meta:
        model = Event
        fields = ['event_name', 'start_time', 'end_time', 'location_address', 'radius', 'is_student_id_required', 'is_index_number_required', 'is_student_name_required']
        widgets = {
            'event_name': forms.TextInput(attrs={'class': 'form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none'}),
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none'}),
            'location_address': forms.TextInput(attrs={'class': 'form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none', 'id': 'id_location_address'}),
            'radius': forms.NumberInput(attrs={'class': 'form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none', 'id': 'radius'}),
        }

class ClassForm(forms.ModelForm):
    class_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Class Name',
        'class': 'border w-full py-4 px-6 rounded-xl'
    }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Class description (optional)',
        'class': 'border w-full py-4 px-6 rounded-xl',
        'rows': 1,  # Initial rows
    }), required=False)

    class Meta:
        model = Class
        fields = ['class_name','description']  


class CheckInForm(forms.Form):
    student_id = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Student ID',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    index_number = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Index Number',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    student_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Student Name',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))