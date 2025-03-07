from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.db.models import Q
from .models import Post, Genre
from .forms import UserRegisterForm

# Create your views here.

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by reading status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(reading_status=status)
            
        # Filter by genre
        genre = self.request.GET.get('genre')
        if genre:
            queryset = queryset.filter(genre__name=genre)
            
        # Search functionality
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(book_title__icontains=query) |
                Q(book_author__icontains=query) |
                Q(content__icontains=query) |
                Q(genre__name__icontains=query)
            ).distinct()
            
        return queryset.filter(status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['current_genre'] = self.request.GET.get('genre', '')
        context['current_status'] = self.request.GET.get('status', '')
        context['search_query'] = self.request.GET.get('q', '')
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get related posts (same genre)
        related_posts = Post.objects.filter(
            genre__in=self.object.genre.all(),
            status='published'
        ).exclude(id=self.object.id).distinct()[:3]
        context['related_posts'] = related_posts
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'book_title', 'book_author', 'genre', 'rating', 
             'content', 'book_cover', 'reading_status', 'recommended', 'status']

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your book review has been created!')
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'book_title', 'book_author', 'genre', 'rating', 
             'content', 'book_cover', 'reading_status', 'recommended', 'status']

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your book review has been updated!')
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Your book review has been deleted!')
        return super().delete(request, *args, **kwargs)

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})
