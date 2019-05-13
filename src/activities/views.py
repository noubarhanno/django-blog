from django.shortcuts import render
from .models import Activity
from posts.models import Posts
from activities.models import Activity
from django.views.generic import View
from django.http import Http404, JsonResponse

class PostLike(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = request.GET
            post_slug = request.GET.get('slug', None) 
            if post_slug is not None and self.request.user.is_authenticated:
                post = Posts.objects.get(slug=post_slug)
                like = Activity.objects.filter(user=request.user).filter(posts__slug=post_slug)
                if post:
                    if not like.exists():
                        post.activities.create(activity_type=Activity.LIKE, user=request.user)
                        return JsonResponse({'like': True})
                    else: 
                        like.delete()
                        return JsonResponse({'like': False})
        raise Http404

class PostLikes(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = request.GET
            post_slug = request.GET.get('slug', None)
            if post_slug is not None:
                post = Posts.objects.get(slug=post_slug)
                likeCount = Activity.objects.filter(activity_type=Activity.LIKE).filter(posts__slug=post_slug)
                if post:
                    return JsonResponse({'likeCount':likeCount.count()})
        raise Http404
        
