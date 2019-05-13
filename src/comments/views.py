from django.shortcuts import render, reverse
from django.http import Http404
from .models import Comment
from .forms import CommentForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
# Create your views here.


def comment_thread(request, id):
    try:
        obj = Comment.objects.get(id=id)
        obj_post = obj.post
    except:
        raise Http404

    if not obj.parent:
        parent_obj = obj

    form = CommentForm(request.POST or None)
    if form.is_valid() and request.user.is_authenticated:
        post = obj_post
        content = form.cleaned_data.get('content')
        author = request.user
        parent = parent_obj

        new_comment, created = Comment.objects.get_or_create(
                            post = post,
                            author= author,
                            content = content,
                            parent = parent,
                        )
        return HttpResponseRedirect(obj.get_absolute_url())

    context = {
        'comment':obj,
        'post':obj_post,
        'form': form,
    }
    
    return render(request, "comments/comment_thread.html", context)


@login_required
def comment_delete(request, id):
    try:
        obj = Comment.objects.get(id=id)
    except:
        raise Http404
    if not obj.author == request.user:
        messages.error(request, "You don't have to permission to delete this comment", extra_tags='alert alert-danger')
    if request.method=='POST':
        try:
            parent_obj_url = obj.parent.get_absolute_url()
        except:
            parent_obj_url = obj.post.get_absolute_url()
        obj.delete()
        messages.success(request, 'The comment has been deleted successfully', extra_tags='alert alert-primary')
        return HttpResponseRedirect(parent_obj_url)
    context = {
        'object': obj
    }
    return render(request, 'comments/confirm_delete.html', context)

@login_required
def comment_update(request, id):
    try:
        obj = Comment.objects.get(id=id)
    except:
        raise Http404

    if obj.parent:
        obj_url = obj.parent.get_absolute_url()
    else:
        obj_url = obj.get_absolute_url()


    form = CommentForm(request.POST or None ,instance=obj)
    if request.method=='POST' and form.is_valid() and request.user.is_authenticated and obj.author == request.user:
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, "the comment is updated successfully", extra_tags="alert alert-primary")
        if obj.parent:
            return HttpResponseRedirect(obj.parent.get_absolute_url())
        else:
            return HttpResponseRedirect(obj.get_absolute_url())

    context = {
        'form': form,
        'returnUrl': obj_url
    }
    return render(request, 'comments/comment_update.html', context)


        