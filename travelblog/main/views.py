from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordResetCompleteView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.core.signing import BadSignature
from django.db.models import Q
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView

from main import forms
from main import models
from .utilities import signer


class ArticleLoginView(LoginView):
    form_class = forms.AuthenticationCustomForm
    template_name = 'main/login.html'


class ArticleLogoutView(LogoutView):
    template_name = 'main/logout.html'


class ArticlePasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Пароль успешно изменен'


class ArticlePasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'main/password_reset_complete.html'


class ArticlePasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'main/password_reset_confirm.html'
    success_url = reverse_lazy('main:password_reset_complete')


class ArticlePasswordResetDoneView(PasswordResetDoneView):
    template_name = 'main/password_reset_done.html'


class ArticlePasswordResetView(PasswordResetView):
    template_name = 'main/password_reset.html'
    success_url = reverse_lazy('main:password_reset_done')
    subject_template_name = 'email/reset_subject.txt'
    email_template_name = 'email/reset_email.txt'


def by_city(request, pk):
    city = get_object_or_404(models.City, pk=pk)
    articles = models.Article.objects.filter(is_active=True, city=pk)
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
        articles = articles.filter(q)
    else:
        keyword = ''

    form = forms.SearchForm(initial={'keyword': keyword})
    paginator = Paginator(articles, 2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'city': city, 'page': page, 'articles': page.object_list, 'form': form}
    return render(request, 'main/by_city.html', context)


def detail(request, city_pk, pk):
    article = get_object_or_404(models.Article, pk=pk)
    ais = article.additionalimage_set.all()
    comments = models.Comment.objects.filter(article=pk, is_active=True)
    initial = {'article': article.pk}
    if request.user.is_authenticated:
        initial['author'] = request.user.username
        form_class = forms.UserCommentForm
    else:
        form_class = forms.GuestCommentForm

    form = form_class(initial=initial)

    if request.method == 'POST':
        c_form = form_class(request.POST)
        if c_form.is_valid():
            c_form.save()
            messages.add_message(request, messages.SUCCESS, 'Комментарий добавлен')
        else:
            form = c_form
            messages.add_message(request, messages.WARNING, 'Комментарий не добавлен')

    context = {'article': article, 'ais': ais, 'comments': comments, 'form': form}
    return render(request, 'main/detail.html', context)


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = models.TravelUser
    template_name = 'main/change_user_info.html'
    form_class = forms.ChangeUserInfoForm
    success_url = reverse_lazy('main:profile')
    success_message = 'Данные пользователя изменены'

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = models.TravelUser
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('main:index')

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удален')
        return super().post(request, *args, **kwargs)

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)


def index(request):
    articles = models.Article.objects.filter(is_active=True)[:10]
    return render(request, 'main/index.html', {'articles': articles})


def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


@login_required
def profile(request):
    articles = models.Article.objects.filter(author=request.user.pk)
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
        articles = articles.filter(q)
    else:
        keyword = ''

    form = forms.SearchForm(initial={'keyword': keyword})
    page = Paginator(articles, 2).get_page(request.GET.get('page', 1))
    context = {'page': page, 'articles': page.object_list, 'form': form}
    return render(request, 'main/profile.html', context)


@login_required
def profile_article_add(request):
    if request.method == 'POST':
        form = forms.ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save()
            formset = forms.AIFormSet(request.POST, request.FILES, instance=article)
            if formset.is_valid():
                formset.save()
                messages.add_message(request, messages.SUCCESS, 'Статья добавлена')
                return redirect('main:profile')
    else:
        form = forms.ArticleForm(initial={'author': request.user.pk})
        formset = forms.AIFormSet()
    context = {'form': form, 'formset': formset}
    return render(request, 'main/profile_article_add.html', context)


@login_required
def profile_article_detail(request, pk):
    article = get_object_or_404(models.Article, pk=pk)
    ais = article.additionalimage_set.all()
    comments = models.Comment.objects.filter(article=pk, is_active=True)
    context = {'article': article, 'ais': ais, 'comments': comments}
    return render(request, 'main/profile_article_detail.html', context)


@login_required
def profile_article_change(request, pk):
    article = get_object_or_404(models.Article, pk=pk)
    if request.method == 'POST':
        form = forms.ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article = form.save()
            formset = forms.AIFormSet(request.POST, request.FILES, instance=article)
            if formset.is_valid():
                formset.save()
                messages.add_message(request, messages.SUCCESS, 'Статья исправлена')
                return redirect('main:profile')
    else:
        form = forms.ArticleForm(instance=article)
        formset = forms.AIFormSet(instance=article)
    context = {'form': form, 'formset': formset}
    return render(request, 'main/profile_article_change.html', context)


@login_required
def profile_article_delete(request, pk):
    article = get_object_or_404(models.Article, pk=pk)
    if request.method == 'POST':
        article.delete()
        messages.add_message(request, messages.SUCCESS, 'Статья удалена')
        return redirect('main:profile')
    else:
        context = {'article': article}
        return render(request, 'main/profile_article_delete.html', context)


class RegisterDoneView(TemplateView):
    template_name = 'main/register_done.html'


class RegisterUserView(CreateView):
    model = models.TravelUser
    template_name = 'main/register_user.html'
    form_class = forms.RegisterUserForm
    success_url = reverse_lazy('main:register_done')


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad_signature.html')
    user = get_object_or_404(models.TravelUser, username=username)
    if user.is_activated:
        template = 'main/user_is_activated.html'
    else:
        template = 'main/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)
