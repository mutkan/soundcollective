from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from users.models import UserProfile

class EditUserProfileForm(ModelForm):

	class Meta:
		model = UserProfile
		fields = ['profile_picture', 'location', 'first_name', 'last_name', 'interested_in', 'instruments']

class UserRegistrationForm(forms.Form):
	"""
	Overriding django-registration form.
	
	"""
	required_css_class = 'required'
	
	username = forms.RegexField(regex=r'^[\w.@+-]+$',
		max_length=64,
		label=_("Username"),
		widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'username',}),
		error_messages={'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")})
	email = forms.EmailField(
		label=_("E-mail"),
		widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'email',}))
	password1 = forms.CharField(
		widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'placeholder': 'password',}),
		label=_("Password"))
	password2 = forms.CharField(
		widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'placeholder': 'password confirmation',}),
		label=_("Password (again)"))
	
	def clean_username(self):
		"""
		Validate that the username is alphanumeric and is not already
		in use.
		
		"""
		existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
		if existing.exists():
			raise forms.ValidationError(_("A user with that username already exists."))
		else:
			return self.cleaned_data['username']
	
	def clean(self):
		"""
		Verifiy that the values entered into the two password fields
		match. Note that an error here will end up in
		``non_field_errors()`` because it doesn't apply to a single
		field.
		
		"""
		if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
			if self.cleaned_data['password1'] != self.cleaned_data['password2']:
				raise forms.ValidationError(_("The two password fields didn't match."))
		return self.cleaned_data

class UserLoginForm(AuthenticationForm):

	username = forms.RegexField(regex=r'^[\w.@+-]+$',
		max_length=64,
		label=_("Username"),
		widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'username',}),
		error_messages={'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")})
	password = forms.CharField(
		widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'placeholder': 'password',}),
		label=_("Password"))
