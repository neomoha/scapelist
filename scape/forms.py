import re
from django.contrib.auth.models import User
from django import forms

class RegistrationForm(forms.Form):
    required_css_class = 'required'
    username = forms.CharField(label=u'Username', max_length=30)
    email = forms.EmailField(label=u'Email')
    password1 = forms.CharField(label=u'Password',widget=forms.PasswordInput())
    password2 = forms.CharField(label=u'Password (Again)',widget=forms.PasswordInput())

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Passwords do not match.')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Username can only contain alphanumeric characters and the underscore.')
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Username is already taken.')

class AttachSongForm(forms.Form):
    tags = forms.CharField(label=u'Tags', required=True, widget=forms.TextInput(attrs={'size': '128'}))
    song_title = forms.CharField(widget=forms.HiddenInput(), max_length=255)
    song_artist = forms.CharField(widget=forms.HiddenInput(), max_length=255)
    song_echonest_id = forms.CharField(widget=forms.HiddenInput(), max_length=50)
    song_spotify_trackid = forms.CharField(widget=forms.HiddenInput(), max_length=50)

