from django import forms
from datetime import date
from django.contrib.admin import widgets
from django.forms import ModelForm

from posts.models import Post

class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['subject', 'location', 'date', 'body',] 

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        self.fields['subject'].required = True
        self.fields['subject'].widget = forms.TextInput(
            attrs = {
                'placeholder': 'Subject',
                'class': 'pure-input-1-3',
                'id': 'input-subject',
            }
        )

        self.fields['date'].required = True
        self.fields['date'].initial = date.today().strftime("%m/%d/%Y")
        self.fields['date'].widget = forms.TextInput(
            attrs = {
                'id': 'input-date',
            }
        )

        self.fields['location'].required = True
        self.fields['location'].widget = forms.TextInput(
            attrs = {
                'placeholder': 'Location',
                'class': 'pure-input-1-3',
                'id': 'input-location',
            }
        )

        self.fields['body'].required = True
        self.fields['body'].widget = forms.Textarea(
            attrs = {
                'class': 'pure-input-2-3',
                'id': 'input-body',
                'rows': 8,
            }
        )
