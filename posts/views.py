# POSTS VIEWS.PY FILE

# from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import Http404
from django.views import generic

from braces.views import SelectRelatedMixin

from . import models, forms

# Create your views here.

# When someone's logged into a session, I can call this user object and call things off of that
from django.contrib.auth import get_user_model
User = get_user_model()

class PostList(SelectRelatedMixin,generic.ListView):
    model = models.Post
    # Show list of posts related to the user or the group
    select_related = ('user','group')

class UserPosts(generic.ListView):
    model = models.Post
    template_name = 'posts/user_post_list.html'
    # When you call the UserPosts ListView, it will try to set the user of this post equal to the user you clicked on
    # See if the user exists, then fetch the posts that are related to that user
    def get_queryset(self):
        try:
            # When a post is selected, identify its User and fetch all posts that belong to the logged in User
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            # return all posts who's User also owns the selected post
            return self.post_user.posts.all()

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        # Return context data object of whoever posted this post
        return context

class PostDetail(SelectRelatedMixin,generic.DetailView):
    model = models.Post
    select_related = ('user','group')

    # Get the querset for the post, filter where the username we are passing in matches the username for all the posts
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))

class CreatePost(LoginRequiredMixin,SelectRelatedMixin,generic.CreateView):

    fields = ('message','group')
    model = models.Post

    def form_valid(self,form):
        self.object = form.save(commit=False)
        # Connect the post to the User
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class DeletePost(LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):
    # Once you delete a post, go back to posts page
    model = models.Post
    select_related = ('user','group')
    # Wait to confirm delete
    success_url = reverse_lazy('posts:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id = self.request.user.id)

    def delete(self,*args,**kwargs):
        messages.success(self.request,'Post Deleted')
        return super().delete(*args,**kwargs)
