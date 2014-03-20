import datetime, os
import soundcloud

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, get_user_model
from django.contrib.auth.models import User
from django.contrib.sites.models import RequestSite, Site, get_current_site
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic.list import ListView

from functools import wraps

from posts.forms import ShoutboxPostForm
from posts.models import ShoutboxPost

from registration import signals
from registration.models import RegistrationProfile
from registration.views import _RequestPassingFormView

from tags.models import MusicianPostTag, UserPostTag, VenuePostTag

from uploads.models import Image

from users.forms import UserLoginForm, UserRegistrationForm, EditUserProfileForm, UserProfileImageListForm, MusicianRegistrationForm, EditMusicianProfileForm, VenueRegistrationForm
from users.models import UserProfile, MusicianProfile, VenueProfile

class InaccessibleView(TemplateView):

	template_name = 'inaccessible.html'

def check_if_user(function):

    @wraps(function)
    def decorator(request, *args, **kwargs):
    	if request.user.username == kwargs['username']:
    		return function(request, *args, **kwargs)
    	else:
    		return HttpResponseRedirect(reverse('inaccessible'))

    return decorator

class UsersView(ListView):

    model = UserProfile
    template_name = 'users/listeners_list.html'

class UserHomeView(TemplateView):

    template_name = 'users/home.html'

class UserProfileView(CreateView):
    
    template_name = 'users/listeners_profile.html'
    form_class = ShoutboxPostForm
    
    def get_object(self, queryset=None):
            obj = User.objects.get(username=self.kwargs['username'])
            return obj
    
    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)

        context['user'] = self.get_object()

        user_profile = UserProfile.objects.get(user_id=context['user'].id)
        context['user_profile'] = user_profile
        try:
            context['is_user'] = True if self.get_object().id == self.request.user.id else False
        except:
            context['is_user'] = False

        shoutbox_posts = user_profile.shoutbox_posts.order_by("-created_date")
        paginator = Paginator(shoutbox_posts, 10)
        page = self.request.GET.get('page')
        try:
            shoutbox = paginator.page(page)
        except PageNotAnInteger:
            shoutbox = paginator.page(1)
        except EmptyPage:
            shoutbox = paginator.page(paginator.num_pages)
        context['shoutbox'] = shoutbox

        client = soundcloud.Client(client_id=os.environ['SOUNDCLOUD_ID'])
        track_url = user_profile.embedded_player
        try:
            context['embedded_player'] = client.get('/oembed', url=track_url)
        except:
            context['embedded_player'] = ''

        return context

    def form_valid(self, form):
        shoutbox_post = form.save()
        shoutbox_post.created_by = UserProfile.objects.get(user_id=self.request.user.id)
        shoutbox_post.modified_by = UserProfile.objects.get(user_id=self.request.user.id)
        shoutbox_post.save()

        user_profile = UserProfile.objects.get(user_id=self.get_object().id)
        user_profile.shoutbox_posts.add(shoutbox_post)

        return HttpResponseRedirect(reverse('listeners_profile', args=(self.get_object().username,)))

class UserProfileEditView(UpdateView):

    form_class = EditUserProfileForm
    template_name = 'users/listeners_profile_edit.html'

    def get_object(self, queryset=None):
        user = User.objects.get(username=self.kwargs['username'])
        obj = UserProfile.objects.get(user=user)

        return obj
    
    def get_context_data(self, **kwargs):
        context = super(UserProfileEditView, self).get_context_data(**kwargs)
        context['user'] = user = self.get_object()
        
        return context
    
    def form_valid(self, form):
        user_profile = form.save()
        
        try:
            if self.request.FILES['profile_image']:
                profile_image = Image.objects.create()
                profile_image.created_by = user_profile
                profile_image.modified_by = user_profile
                profile_image.image = self.request.FILES['profile_image']
                profile_image.save()

                user_profile.profile_image = profile_image
        except:
            pass
        try: 
            if self.request.FILES['splash_image']:
                splash_image = Image.objects.create()
                splash_image.created_by = user_profile
                splash_image.modified_by = user_profile
                splash_image.image = image=self.request.FILES['splash_image']
                splash_image.save()

                user_profile.splash_image = splash_image
        except:
            pass

        user_profile.save()

        return HttpResponseRedirect(reverse('listeners_profile', args=(self.get_object().user.username,)))
                
class UserProfileImageListView(FormView):
    
    form_class = UserProfileImageListForm 
    template_name = 'users/listeners_profile_images.html'

class MusicianRegistrationView(CreateView):

    form_class = MusicianRegistrationForm
    template_name = 'users/musicians_registration.html'

    def form_valid(self, form):
        musician_profile = form.save()

        musician_profile.created_by = self.request.user.userprofile
        musician_profile.modified_by = self.request.user.userprofile
        musician_profile.user_profiles.add(self.request.user.userprofile)

        musician_profile.save()

        return HttpResponseRedirect(reverse('musicians_profile', args=(musician_profile.username,)))

class MusiciansView(ListView):

    model = MusicianProfile
    template_name = 'users/musicians_list.html'

class MusiciansProfileViewOld(CreateView):

    template_name = 'users/musicians_profile.html'
    form_class = ShoutboxPostForm
    
    def get_object(self, queryset=None):
        obj = MusicianProfile.objects.get(username=self.kwargs['name'])
        return obj
    
    def get_context_data(self, **kwargs):
        context = super(MusiciansProfileViewOld, self).get_context_data(**kwargs)

        musician_profile = self.get_object()
        context['user_profile'] = musician_profile

        try:
            context['is_user'] = True if self.get_object().user_profiles.all().filter(id=self.request.user.userprofile.id) else False
        except:
            context['is_user'] = False

        shoutbox_posts = musician_profile.shoutbox_posts.order_by("-created_date")
        paginator = Paginator(shoutbox_posts, 10)
        page = self.request.GET.get('page')
        try:
            shoutbox = paginator.page(page)
        except PageNotAnInteger:
            shoutbox = paginator.page(1)
        except EmptyPage:
            shoutbox = paginator.page(paginator.num_pages)
        context['shoutbox'] = shoutbox

        context['upcoming_shows'] = MusicianPostTag.objects.filter(tagged_musician=musician_profile).order_by('post__date').exclude(post__date__lt=datetime.date.today()-datetime.timedelta(days=1))[:3]

        client = soundcloud.Client(client_id=os.environ['SOUNDCLOUD_ID'])
        track_url = musician_profile.embedded_player
        try:
            context['embedded_player'] = client.get('/oembed', url=track_url)
        except:
            context['embedded_player'] = ''

        return context

    def form_valid(self, form):
        shoutbox_post = form.save()
        shoutbox_post.created_by = UserProfile.objects.get(user_id=self.request.user.id)
        shoutbox_post.modified_by = UserProfile.objects.get(user_id=self.request.user.id)
        shoutbox_post.save()

        user_profile = self.get_object()
        user_profile.shoutbox_posts.add(shoutbox_post)

        return HttpResponseRedirect(reverse('musicians_profile', args=(self.get_object().username,)))

class MusiciansProfileView(CreateView):

    template_name = 'users/musicians_profile_maroon.html'
    form_class = ShoutboxPostForm
    
    def get_object(self, queryset=None):
        obj = MusicianProfile.objects.get(username=self.kwargs['name'])
        return obj
    
    def get_context_data(self, **kwargs):
        context = super(MusiciansProfileView, self).get_context_data(**kwargs)

        musician_profile = self.get_object()
        context['user_profile'] = musician_profile

        try:
            context['is_user'] = True if self.get_object().user_profiles.all().filter(id=self.request.user.userprofile.id) else False
        except:
            context['is_user'] = False

        shoutbox_posts = musician_profile.shoutbox_posts.order_by("-created_date")
        paginator = Paginator(shoutbox_posts, 10)
        page = self.request.GET.get('page')
        try:
            shoutbox = paginator.page(page)
        except PageNotAnInteger:
            shoutbox = paginator.page(1)
        except EmptyPage:
            shoutbox = paginator.page(paginator.num_pages)
        context['shoutbox'] = shoutbox

        context['upcoming_shows'] = MusicianPostTag.objects.filter(tagged_musician=musician_profile).order_by('post__date').exclude(post__date__lt=datetime.date.today()-datetime.timedelta(days=1))[:3]

        client = soundcloud.Client(client_id=os.environ['SOUNDCLOUD_ID'])
        track_url = musician_profile.embedded_player
        try:
            player = client.get('/oembed', url=track_url, maxheight='166')
            context['embedded_player'] = player.fields()['html'] 
        except:
            context['embedded_player'] = ''

        return context

    def form_valid(self, form):
        shoutbox_post = form.save()
        shoutbox_post.created_by = UserProfile.objects.get(user_id=self.request.user.id)
        shoutbox_post.modified_by = UserProfile.objects.get(user_id=self.request.user.id)
        shoutbox_post.save()

        user_profile = self.get_object()
        user_profile.shoutbox_posts.add(shoutbox_post)

        return HttpResponseRedirect(reverse('musicians_profile', args=(self.get_object().username,)))

class MusiciansProfileViewRed(CreateView):

    template_name = 'profile-mockup-red.html'
    form_class = ShoutboxPostForm
    
    def get_object(self, queryset=None):
        obj = MusicianProfile.objects.get(username=self.kwargs['name'])
        return obj
    
    def get_context_data(self, **kwargs):
        context = super(MusiciansProfileViewRed, self).get_context_data(**kwargs)

        musician_profile = self.get_object()
        context['user_profile'] = musician_profile

        try:
            context['is_user'] = True if self.get_object().user_profiles.all().filter(id=self.request.user.userprofile.id) else False
        except:
            context['is_user'] = False

        shoutbox_posts = musician_profile.shoutbox_posts.order_by("-created_date")
        paginator = Paginator(shoutbox_posts, 10)
        page = self.request.GET.get('page')
        try:
            shoutbox = paginator.page(page)
        except PageNotAnInteger:
            shoutbox = paginator.page(1)
        except EmptyPage:
            shoutbox = paginator.page(paginator.num_pages)
        context['shoutbox'] = shoutbox

        context['upcoming_shows'] = MusicianPostTag.objects.filter(tagged_musician=musician_profile).order_by('post__date').exclude(post__date__lt=datetime.date.today()-datetime.timedelta(days=1))[:3]

        client = soundcloud.Client(client_id=os.environ['SOUNDCLOUD_ID'])
        track_url = musician_profile.embedded_player
        try:
            context['embedded_player'] = client.get('/oembed', url=track_url)
        except:
            context['embedded_player'] = ''

        return context

    def form_valid(self, form):
        shoutbox_post = form.save()
        shoutbox_post.created_by = UserProfile.objects.get(user_id=self.request.user.id)
        shoutbox_post.modified_by = UserProfile.objects.get(user_id=self.request.user.id)
        shoutbox_post.save()

        user_profile = self.get_object()
        user_profile.shoutbox_posts.add(shoutbox_post)

        return HttpResponseRedirect(reverse('musicians_profile', args=(self.get_object().username,)))

class MusiciansProfileEditView(UpdateView):

    form_class = EditMusicianProfileForm
    template_name = 'users/musicians_profile_edit.html'

    def get_object(self, queryset=None):
        obj = MusicianProfile.objects.get(username=self.kwargs['name'])

        return obj
    
    def get_context_data(self, **kwargs):
        context = super(MusiciansProfileEditView, self).get_context_data(**kwargs)
        context['user'] = user = self.get_object()
        
        return context
    
    def form_valid(self, form):
        user_profile = form.save()
        
        try:
            if self.request.FILES['profile_image']:
                profile_image = Image.objects.create()
                profile_image.created_by = user_profile
                profile_image.modified_by = user_profile
                profile_image.image = self.request.FILES['profile_image']
                profile_image.save()

                user_profile.profile_image = profile_image
        except:
            pass
        try: 
            if self.request.FILES['splash_image']:
                splash_image = Image.objects.create()
                splash_image.created_by = user_profile
                splash_image.modified_by = user_profile
                splash_image.image = image=self.request.FILES['splash_image']
                splash_image.save()

                user_profile.splash_image = splash_image
        except:
            pass
        
#        import soundcloud
#        client = soundcloud.Client(client_id='YOUR_CLIENT_ID')
#
#        track_url = form.cleaned_data['
#        embed_info = client.get('/oembed', url=track_url)
#
#        print embed_info['html']

        user_profile.save()

        return HttpResponseRedirect(reverse('musicians_profile', args=(self.get_object().username,)))
   

class VenueRegistrationView(CreateView):

    form_class = VenueRegistrationForm
    template_name = 'users/venues_registration.html'

class VenuesView(ListView):

    model = VenueProfile
    template_name = 'users/venues_list.html'

class BaseRegistrationView(_RequestPassingFormView):
	"""
	Base class for user registration views.
	
	"""
	disallowed_url = 'registration_disallowed'
	form_class = UserRegistrationForm
	http_method_names = ['get', 'post', 'head', 'options', 'trace']
	success_url = None
	template_name = 'registration/registration_form.html'
	
	def dispatch(self, request, *args, **kwargs):
		"""
		Check that user signup is allowed before even bothering to
		dispatch or do other processing.
		
		"""
		if not self.registration_allowed(request):
			return redirect(self.disallowed_url)
		return super(BaseRegistrationView, self).dispatch(request, *args, **kwargs)
	
	def form_valid(self, request, form):
		new_user = self.register(request, **form.cleaned_data)
		success_url = self.get_success_url(request, new_user)
		
		# success_url may be a simple string, or a tuple providing the
		# full argument set for redirect(). Attempting to unpack it
		# tells us which one it is.
		try:
			to, args, kwargs = success_url
			return redirect(to, *args, **kwargs)
		except ValueError:
			return redirect(success_url)
	
	def registration_allowed(self, request):
		"""
		Override this to enable/disable user registration, either
		globally or on a per-request basis.
		
		"""
		return True
	
	def register(self, request, **cleaned_data):
		"""
		Implement user-registration logic here. Access to both the
		request and the full cleaned_data of the registration form is
		available here.
		
		"""
		raise NotImplementedError

class UserRegistrationView(BaseRegistrationView):
	"""
	A registration backend which follows a simple workflow:
	
	1. User signs up, inactive account is created.
	
	2. Email is sent to user with activation link.
	
	3. User clicks activation link, account is now active.
	
	Using this backend requires that
	
	* ``registration`` be listed in the ``INSTALLED_APPS`` setting
	  (since this backend makes use of models defined in this
	  application).
	
	* The setting ``ACCOUNT_ACTIVATION_DAYS`` be supplied, specifying
	  (as an integer) the number of days from registration during
	  which a user may activate their account (after that period
	  expires, activation will be disallowed).
	
	* The creation of the templates
	  ``registration/activation_email_subject.txt`` and
	  ``registration/activation_email.txt``, which will be used for
	  the activation email. See the notes for this backends
	  ``register`` method for details regarding these templates.
	
	Additionally, registration can be temporarily closed by adding the
	setting ``REGISTRATION_OPEN`` and setting it to
	``False``. Omitting this setting, or setting it to ``True``, will
	be interpreted as meaning that registration is currently open and
	permitted.
	
	Internally, this is accomplished via storing an activation key in
	an instance of ``registration.models.RegistrationProfile``. See
	that model and its custom manager for full documentation of its
	fields and supported operations.
	
	"""
	def register(self, request, **cleaned_data):
		"""
		Given a username, email address and password, register a new
		user account, which will initially be inactive.
	
		Along with the new ``User`` object, a new
		``registration.models.RegistrationProfile`` will be created,
		tied to that ``User``, containing the activation key which
		will be used for this account.
	
		An email will be sent to the supplied email address; this
		email should contain an activation link. The email will be
		rendered using two templates. See the documentation for
		``RegistrationProfile.send_activation_email()`` for
		information about these templates and the contexts provided to
		them.
	
		After the ``User`` and ``RegistrationProfile`` are created and
		the activation email is sent, the signal
		``registration.signals.user_registered`` will be sent, with
		the new ``User`` as the keyword argument ``user`` and the
		class of this backend as the sender.
	
		"""
		username, email, password = cleaned_data['username'], cleaned_data['email'], cleaned_data['password1']
		if Site._meta.installed:
			site = Site.objects.get_current()
		else:
			site = RequestSite(request)
		new_user = RegistrationProfile.objects.create_inactive_user(username, email,
																	password, site)
		
		# user_profile creation
		user_profile = UserProfile.objects.create(user=new_user)
		user_profile.save()
		
		signals.user_registered.send(sender=self.__class__,
									 user=new_user,
									 request=request)
		return new_user
	
	def registration_allowed(self, request):
		"""
		Indicate whether account registration is currently permitted,
		based on the value of the setting ``REGISTRATION_OPEN``. This
		is determined as follows:
	
		* If ``REGISTRATION_OPEN`` is not specified in settings, or is
		  set to ``True``, registration is permitted.
	
		* If ``REGISTRATION_OPEN`` is both specified and set to
		  ``False``, registration is not permitted.
		
		"""
		return getattr(settings, 'REGISTRATION_OPEN', True)
	
	def get_success_url(self, request, user):
		"""
		Return the name of the URL to redirect to after successful
		user registration.
		
		"""
		return ('registration_complete', (), {})

@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=UserLoginForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """

    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":
        form = authentication_form(data=request.POST)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())
            
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    request.session.set_test_cookie()

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context,
                            current_app=current_app)
