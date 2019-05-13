from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormMixin
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.list import ListView
from django.views.generic import View
from posts.models import Posts
from comments.models import Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from posts.forms import PostsCreateForm, PostsUpdateForm
from comments.forms import CommentForm
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from activities.models import Activity
from django.db.models import Count
from accounts.models import MyUser

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Posts
    template_name = 'posts/posts_form.html'
    form_class = PostsCreateForm

    def form_valid(self, form):
        request = self.request
        # #Add logged-in user as autor of comment THIS IS THE KEY TO THE SOLUTION
        form.instance.user = self.request.user
        print(request.POST)
        if 'post' in request.POST:
            form.instance.status = 'D'
            form.instance.validate = True
            messages.success(request, 'The post has been sent for review it should be published in passed the site policy', extra_tags='alert alert-primary')
            
        # # Call super-class form validation behaviour
        return super(PostCreateView, self).form_valid(form)


class PostDetailView(FormMixin, DetailView):
    model = Posts
    template_name = 'posts/posts_detail.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('posts:detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            like = Activity.objects.filter(user=self.request.user).filter(posts__slug=self.object.slug)
            if like:
                context['like'] = True
            else:
                context['like'] = False
        context['comment_form'] = CommentForm(initial={
            'post': self.object
        })
        context['comments'] = self.object.comments.all()
        context['now'] = timezone.now()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.post = self.get_object()
        try:
            parent_id = int(self.request.POST.get('parent_id'))
        except:
            parent_id = None
        
        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()
                comment.parent = parent_obj
        comment.save()
        return super(PostDetailView, self).form_valid(form)
        

class PostListView(ListView):
    model = Posts
    paginate_by = 6

    def get_context_data(self, *args, **kwargs):
        context = super(PostListView, self).get_context_data(*args, **kwargs)
        context['now'] = timezone.now()
        return context

    def get_queryset(self , *args, **kwargs):
        request = self.request
        query = request.GET.get('q' , None)
        if query is not None:
            return Posts.objects.search(query)
        return Posts.objects.all().filter(status='P')

class AthorPostListView(ListView):
    model = Posts
    template_name = 'posts/posts_author_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AthorPostListView, self).get_context_data(*args, **kwargs)
        query = MyUser.objects.get(id=self.kwargs['id'])
        context['author'] = query
        return context

    def get_queryset(self, *args, **kwargs):
        user_id = self.kwargs['id']
        if user_id is not None:
            return Posts.objects.all().filter(user__id=user_id).filter(status='P')
        return None

class ValidatePostListView(ListView):
    model = Posts
    template_name = 'posts/posts_validate_list.html'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_admin:
            return Posts.objects.validate_posts()
        else:
            raise PermissionDenied


class PostDeleteView(DeleteView):
    model = Posts
    success_url = reverse_lazy('posts:list')
    error_message = "You are not authorized to delete this post"
    success_message = "Delete Successfully"

    def get_object(self):
        obj = super(PostDeleteView, self).get_object()
        if obj.user == self.request.user:
            return obj
        raise PermissionDenied

class PostUpdateView(UpdateView):
    model = Posts
    template_name_suffix = '_update_form'
    form_class = PostsUpdateForm

    def get_object(self):
        obj = super(PostUpdateView, self).get_object()
        if obj.user == self.request.user:
            return obj
        raise PermissionDenied


# def add_comment_to_post(request, slug):
#     post = get_object_or_404(Posts, slug=slug)
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.author = request.user
#             comment.save()
#             return redirect('posts:detail', slug=post.slug)
#     else:
#         form = CommentForm()
#     return render(request, 'posts/posts_detail.html', {'comment_form': form,'slug':slug})


@login_required
def post_approve(request, id):
    post = get_object_or_404(Posts, id=id)
    post.approve()
    return redirect('posts:detail', slug=post.slug)

@login_required
def post_hide(request, id):
    post = get_object_or_404(Posts, id=id)
    post.hide()
    return redirect('posts:detail', slug=post.slug)


