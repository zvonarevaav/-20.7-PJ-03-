from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Announcement, Comment, Category
from .filters import AnnouncementFilter
from .forms import AnnouncementForm
from datetime import datetime
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import Group


def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='premium')
    if not user.groups.filter(name='premium').exists():
        premium_group.user_set.add(user)
        messages.success(request, 'Ваш аккаунт обновлен до премиум статуса!')
    return redirect('announcements')


def logout_user(request):
    logout(request)
    return redirect('announcements')


def subscribe(request, pk):
    category = get_object_or_404(Category, id=pk)
    user = request.user
    if user.is_authenticated:
        if user not in category.subscribers.all():
            category.subscribers.add(user)
            messages.success(request, f'Вы успешно подписались на категорию "{category.category_name}".')
        else:
            messages.warning(request, f'Вы уже подписаны на категорию "{category.category_name}".')
    else:
        messages.error(request, 'Для подписки на категорию необходимо авторизоваться.')
    return redirect('category_list', pk=pk)


class IndexView(TemplateView):
    template_name = "user_page.html"


class AnnouncementsList(ListView):
    model = Announcement
    template_name = 'announcements.html'
    context_object_name = 'announcements'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class AnnouncementDetail(DetailView):
    model = Announcement
    template_name = 'announcement.html'
    context_object_name = 'announcement'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(announcement__id=self.kwargs['pk'])
        return context


class CategoryListView(ListView):
    model = Announcement
    template_name = 'category_list.html'
    context_object_name = 'category_announcement_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Announcement.objects.filter(categories=self.category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


class SearchAnnouncementsList(ListView):
    model = Announcement
    template_name = 'search.html'
    context_object_name = 'search_announcements'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = AnnouncementFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class AnnouncementCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('announcements.add_announcement',)
    form_class = AnnouncementForm
    model = Announcement
    template_name = 'announcement_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        messages.success(self.request, 'Объявление успешно создано!')
        return super().form_valid(form)


class AnnouncementUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('announcements.change_announcement',)
    form_class = AnnouncementForm
    model = Announcement
    template_name = 'announcement_create.html'

    def form_valid(self, form):
        messages.success(self.request, 'Объявление успешно обновлено!')
        return super().form_valid(form)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(author=self.request.user.author)


class AnnouncementDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('announcements.delete_announcement',)
    model = Announcement
    template_name = 'announcement_delete.html'
    success_url = reverse_lazy('announcements')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Объявление успешно удалено!')
        return super().delete(request, *args, **kwargs)
