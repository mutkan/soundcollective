from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from users.models import UserProfile, MusicianProfile, VenueProfile

class EditUserProfileForm(ModelForm):
    profile_image = forms.ImageField()
    profile_image.required = False
    profile_image.widget = forms.ClearableFileInput(
        attrs = {
            'id': 'input-profile-image',
        }
    )

    splash_image = forms.ImageField()
    splash_image.required = False
    splash_image.widget = forms.ClearableFileInput(
        attrs = {
            'id': 'input-splash-image',
        }
    )

    class Meta:
        model = UserProfile
        fields = ['display_name', 'location', 'blurb', 'embedded_player', 'contact_twitter', 'contact_facebook']

    def __init__(self, *args, **kwargs):
        super(EditUserProfileForm, self).__init__(*args, **kwargs)

        self.fields['display_name'].required = False
        self.fields['display_name'].widget = forms.TextInput(
                attrs = {
                        'placeholder': 'Display Name',
                        'class': 'form-control',
                        'id': 'input-display-name',
                }
        )

        self.fields['location'].required = False
        self.fields['location'].widget = forms.TextInput(
                attrs = {
                        'placeholder': 'Location',
                        'class': 'form-control',
                        'id': 'input-location',
                }
        )

        self.fields['blurb'].required = False
        self.fields['blurb'].widget = forms.Textarea(
                attrs = {
                        'placeholder': 'Blurb',
                        'class': 'form-control',
                        'id': 'input-blurb',
                        'rows': 5,
                }
        )

        self.fields['embedded_player'].required = False
        self.fields['embedded_player'].widget = forms.Textarea(
                attrs = {
                        'placeholder': 'Embed a music player',
                        'class': 'form-control',
                        'id': 'input-embedded_player',
                        'rows': 5,
                }
        )

        self.fields['contact_twitter'].required = False
        self.fields['contact_twitter'].widget = forms.TextInput(
                attrs = {
                        'placeholder': 'Twitter Username',
                        'class': 'form-control',
                        'id': 'input-twitter',
                }
        )

        self.fields['contact_facebook'].required = False
        self.fields['contact_facebook'].widget = forms.TextInput(
                attrs = {
                        'placeholder': 'Facebook Username',
                        'class': 'form-control',
                        'id': 'input-facebook',
                }
        )

class EditMusicianProfileForm(ModelForm):
    profile_image = forms.ImageField()
    profile_image.required = False
    profile_image.widget = forms.ClearableFileInput(
        attrs = {
            'id': 'input-profile-image',
        }
    )

    splash_image = forms.ImageField()
    splash_image.required = False
    splash_image.widget = forms.ClearableFileInput(
        attrs = {
            'id': 'input-splash-image',
        }
    )

    class Meta:
        model = MusicianProfile
        fields = ['display_name', 'location', 'blurb', 'embedded_player', 'contact_email', 'contact_twitter', 'contact_facebook']

    def __init__(self, *args, **kwargs):
        super(EditMusicianProfileForm, self).__init__(*args, **kwargs)

        self.fields['display_name'].required = False
        self.fields['display_name'].widget = forms.TextInput(
                attrs = {
                        'placeholder': 'Display Name',
                        'class': 'form-control',
                        'id': 'input-display-name',
                }
        )

        self.fields['location'].required = False
        self.fields['location'].widget = forms.TextInput(
                attrs = {
                        'placeholder': 'Location',
                        'class': 'form-control',
                        'id': 'input-location',
                }
        )

        self.fields['blurb'].required = False
        self.fields['blurb'].widget = forms.Textarea(
                attrs = {
                        'placeholder': 'Blurb',
                        'class': 'form-control',
                        'id': 'input-blurb',
                        'rows': 5,
                }
        )

        self.fields['embedded_player'].required = False
        self.fields['embedded_player'].widget = forms.Textarea(
                attrs = {
                        'placeholder': 'Embed a music player',
                        'class': 'form-control',
                        'id': 'input-embedded_player',
                        'rows': 5,
                }
        )

        self.fields['contact_email'].required = False
        self.fields['contact_email'].widget = forms.TextInput(
                attrs = {
                        'placeholder': 'Email',
                        'class': 'form-control',
                        'id': 'input-email',
                }
        )
        
        self.fields['contact_twitter'].required = False
        self.fields['contact_twitter'].widget = forms.TextInput(
                attrs = {
                        'placeholder': 'Twitter Username',
                        'class': 'form-control',
                        'id': 'input-twitter',
                }
        )

        self.fields['contact_facebook'].required = False
        self.fields['contact_facebook'].widget = forms.TextInput(
                attrs = {
                        'placeholder': 'Facebook Username',
                        'class': 'form-control',
                        'id': 'input-facebook',
                }
        )

class AddPhotoForm(forms.Form):
    
    images = forms.ImageField()
    images.required = True
    images.widget = forms.ClearableFileInput(
        attrs = {
            'id': 'input-add-photo',
        }
    )

class UserProfileImageListForm(forms.Form):

    profile = forms.ImageField()
    profile.required = False
    profile.widget = forms.ClearableFileInput(
        attrs = {
            'id': 'input-profile-image',
        }
    )

    splash = forms.ImageField()
    splash.required = False
    splash.widget = forms.ClearableFileInput(
        attrs = {
            'id': 'input-splash-image',
        }
    )

class UserRegistrationForm(forms.Form):
	"""
	Overriding django-registration form.

	"""
	required_css_class = 'required'

	username = forms.RegexField(regex=r'^[\w.@+-]+$',
		max_length=64,
		label=_("Username"),
		widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'input-username', 'type': 'text', 'placeholder': 'username',}),
		error_messages={'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")})
	email = forms.EmailField(
		label=_("E-mail"),
		widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'input-email', 'type': 'text', 'placeholder': 'email',}))
	password1 = forms.CharField(
		widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'input-password1', 'type': 'password', 'placeholder': 'password',}),
		label=_("Password"))
	password2 = forms.CharField(
		widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'input-password2', 'type': 'password', 'placeholder': 'password confirmation',}),
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

class MusicianRegistrationForm(ModelForm):

    class Meta:
        model = MusicianProfile
        fields = ['username', 'display_name', 'location', 'genre']

    def __init__(self, *args, **kwargs):
        super(MusicianRegistrationForm, self).__init__(*args, **kwargs)
    
	self.fields['username'] = forms.RegexField(regex=r'^[\w.@+-]+$',
            max_length=64,
            widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'input-username', 'type': 'text', 'placeholder': 'username',}),
            error_messages={'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")}
        )

	self.fields['display_name'] = forms.RegexField(regex=r'^[\w.@+-]+$',
            widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'input-email', 'type': 'text', 'placeholder': 'email',})
        )
            
	self.fields['location'] = forms.CharField(
            widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'input-location', 'placeholder': 'location',}),
        )

	self.fields['genre'] = forms.CharField(
            widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'input-genre', 'placeholder': 'genre',}),
        )

class VenueRegistrationForm(ModelForm):

    class Meta:
        model = VenueProfile
        fields = ['username', 'display_name', 'location', 'genre']

    def __init__(self, *args, **kwargs):
        super(VenueRegistrationForm, self).__init__(*args, **kwargs)
    
	self.fields['username'] = forms.RegexField(regex=r'^[\w.@+-]+$',
            max_length=64,
            widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'input-username', 'type': 'text', 'placeholder': 'username',}),
            error_messages={'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")}
        )

	self.fields['display_name'] = forms.RegexField(regex=r'^[\w.@+-]+$',
            widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'input-email', 'type': 'text', 'placeholder': 'email',})
        )
            
	self.fields['location'] = forms.CharField(
            widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'input-location', 'placeholder': 'location',}),
        )

	self.fields['genre'] = forms.CharField(
            widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'input-genre', 'placeholder': 'genre',}),
        )

class UserLoginForm(AuthenticationForm):
    username = forms.RegexField(
        regex = r'^[\w.@+-]+$',
        max_length = 64,
        widget=forms.TextInput(
            attrs = {
                'class': 'form-control',
                'id': 'input-username',
                'placeholder': 'Username',
            }
        ),
        error_messages={'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")}
    )
    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-control',
                'id': 'input-password',
                'placeholder': 'Password',
            }
        ),
    )
