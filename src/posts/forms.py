from posts.models import Posts
from django.forms import ModelForm
from django import forms
from tinymce import TinyMCE

# from pagedown.widgets import PagedownWidget
# from tinymce.widgets import TinyMCE
# from tinymce import models as tinymce_models
 

class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False

class PostsCreateForm(ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'title'}))
    content = forms.CharField(widget=TinyMCEWidget(attrs={'cols':80, 'rows':30, 'required': False,'class':'content-post-tiny', 'id':'content'}))

    class Meta:
        model = Posts
        fields = ['title','content','image']



class PostsUpdateForm(ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'title','readonly':'true'}))
    content = forms.CharField(widget=TinyMCEWidget(attrs={'cols':80, 'rows':30, 'required': False,'class':'content-post-tiny'}))

    class Meta:
        model = Posts
        fields = ['title','content','image']

