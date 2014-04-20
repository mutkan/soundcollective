from django.views.generic import TemplateView, FormView, View
from django.db.models import Q

from users.models import UserProfile, MusicianProfile, VenueProfile

class MainSearch(TemplateView):
    
    template_name = 'search_results.html'

    def get_context_data(self, **kwargs):
        
        context = super(MainSearch, self).get_context_data(**kwargs)    

        search_term = self.request.GET.get('search_term', '')

        listeners = UserProfile.objects.all().filter(
            Q(display_name__icontains=search_term) |
            Q(user__username__icontains=search_term) 
        )
        venues = VenueProfile.objects.all().filter(
            Q(display_name__icontains=search_term) |
            Q(username__icontains=search_term) 
        )
        musicians = MusicianProfile.objects.all().filter(
            Q(display_name__icontains=search_term) |
            Q(username__icontains=search_term) 
        )

        context.update({
            'listeners': listeners,
            'musicians': musicians,
            'venues': venues,
        })

        return context
