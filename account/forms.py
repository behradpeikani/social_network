from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Profile

# from .models import Profile

not_allowed_usernames = ['admin', 'css', 'js', 'static', 'static_root', 'instagram', 'media', 'login', 'logout', 'user',
'users', 'python', 'sql', 'delete', 'update', 'create', 'html', 'django', 'administrator', 'root']

class RegisterForm(forms.Form):
	first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter your first name", "class": "form-control"}),max_length=20, min_length=3)
	last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter your last name", "class": "form-control"}), max_length=20, min_length=3)
	username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter username", "class": "form-control"}), max_length=20, min_length=3)
	email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Enter email", "class": "form-control"}))
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={"placeholder": "Enter password", "class": "form-control"}), min_length=8)
	password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={"placeholder": "Confirm password", "class": "form-control"}), min_length=8)

	class Meta:
		model = User
		fields = '__all__'

	def clean_username(self):
		username = self.cleaned_data.get('username')
		qs = User.objects.filter(username__iexact=username)
		if username in not_allowed_usernames:
			raise forms.ValidationError('invalid username, pick another')
		if qs.exists():
			raise forms.ValidationError('invalid username, pick another')
		return username

	def clean_email(self):
		email = self.cleaned_data.get('email')
		qs = User.objects.filter(email__iexact=email)
		if qs.exists():
			raise forms.ValidationError('invalid email, pick another')
		return email

	def clean(self):
		data = self.cleaned_data
		password = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password != password2:
			raise forms.ValidationError('Passwords do not match! Try again.')
		return data

class LoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter username", "class": "form-control"}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Enter password", "class": "form-control"}))

	class Meta:
		model = User
		fields = '__all__'

	def clean_username(self):
		username = self.cleaned_data.get('username')
		qs = User.objects.filter(username__iexact=username)
		if not qs.exists():
			raise forms.ValidationError('This is an invalid username')

class ProfileForm(forms.ModelForm):
	username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))

	class Meta:
		model = Profile
		fields = ('bio', 'profile_pic')