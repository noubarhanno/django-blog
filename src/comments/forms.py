from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control comment-reply-thread','rows':2}))
    # content = forms.CharField(widget=PagedownWidget(show_preview=False))

    class Meta:
        model = Comment
        fields = ('content',)
