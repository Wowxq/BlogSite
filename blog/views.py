from django.contrib.auth import login
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Blog
from django. utils import timezone
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView
from .forms import BlogForm, BlogEditForm, RegisterForm
from django.shortcuts import get_object_or_404


# Create your views here.
class HomeView(LoginRequiredMixin, TemplateView):
    login_url = "/login"
    template_name = "blog/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["blogs"] = Blog.objects.all()
        return context
    
class BlogListView(LoginRequiredMixin, TemplateView):
    login_url = "/login"
    template_name = "blog/list.html"
    queryset = Blog.objects.order_by('-date_created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blogs'] = Blog.objects.order_by('-date_created')
        context['current_time'] = timezone.now()
        return context

class BlogCreateView(LoginRequiredMixin, FormView):
    login_url = "/login"
    template_name = "blog/create.html"
    form_class = BlogForm

    def form_valid(self, form):
        
        blog = form.save(commit=False)
        blog.author = self.request.user
        blog.save()
        return super().form_valid(form)

    def get_success_url(self):
        
        return reverse_lazy('blogs')
    
class BlogEditView(LoginRequiredMixin, FormView):
    login_url = "/login"
    template_name = "blog/edit.html"
    form_class = BlogEditForm

    def get_initial(self):
        blog_id = self.kwargs['pk']
        blog = get_object_or_404(Blog, id=blog_id)
        return {'title': blog.title, 'description': blog.description}

    def form_valid(self, form):
        blog_id = self.kwargs['pk']
        blog = get_object_or_404(Blog, id=blog_id)
        blog.title = form.cleaned_data['title']
        blog.description = form.cleaned_data['description']
        blog.image = form.cleaned_data['image']
        blog.save()
        return super().form_valid(form)

    def get_success_url(self):
        blog_id = self.kwargs['pk']
        return reverse_lazy('blogs', kwargs={'pk': blog_id})
    
class SignUpView(FormView):
    template_name = 'registration/sign_up.html'
    form_class = RegisterForm
    success_url = ''  

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context
    

