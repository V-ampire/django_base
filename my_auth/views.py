from django.views import View
from django.views.generic import FormView, TemplateView
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from django.template.context_processors import csrf
from urllib.parse import urlparse
from .utils import get_next_url, get_client_ip, check_temp_url_token
from .models import TemporaryBanIP, ConfirmedUser
from .forms import LoginForm, ConfirmedUserCreationForm, ResendConfirmForm



class MyLoginView(View):
    """
        LoginView с ограничение количества запросов
    """

    authentication_form = LoginForm
    template_name = 'my_auth/login.html'
    
    def get_form_class(self):
        return self.authentication_form
    
    @property
    def attempts_15_minutes_block(self):
        return settings.AUTH_ATTEMPTS['15_MINUTES_BLOCK']
    
    @property
    def attempts_24_hours_block(self):
        return settings.AUTH_ATTEMPTS['24_HOURS_BLOCK']

    def get(self, request):
        # if user is authenticated then redirect to LOGIN_REDIRECT_URL
        if auth.get_user(request).is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            # Иначе формируем контекст с формой авторизации и отдаём страницу 
            # с этим контекстом.
            context = self.create_context_username_csrf(request)
            return render(request, self.template_name, context=context)

    def post(self, request):
        login_form = self.get_form_class()
        form = login_form(request, data=request.POST)
        ip = get_client_ip(request)
         # получаем или создаём новую запись об IP, с которого вводится пароль, на предмет блокировки
        obj, created = TemporaryBanIP.objects.get_or_create(
            defaults={
                'ip_address': ip,
                'time_unblock': timezone.now()
            },
            ip_address=ip
        )
        # если IP заблокирован и время разблокировки не настало
        if obj.status is True and obj.time_unblock > timezone.now():
            context = self.create_context_username_csrf(request)
            if obj.attempts == self.attempts_15_minutes_block or obj.attempts == self.attempts_15_minutes_block * 2:
                # то открываем страницу с сообщением о блокировки на 15 минут при 3 и 6 неудачных попытках входа
                return render(request, 'my_auth/block_15_minutes.html')
            elif obj.attempts == self.attempts_24_hours_block:
                # при 9 неудачных попытках открываем страницу о блокировке на 24 часа
                return render(request, 'my_auth/block_24_hours.html')
        elif obj.status is True and obj.time_unblock < timezone.now():
            obj.status = False
            obj.save()

        # если пользователь ввёл верные данные, то авторизуем его и удаляем запись о блокировке IP
        if form.is_valid():
            auth.login(request, form.get_user())
            obj.delete()
            next_ = urlparse(get_next_url(request)).path
            if next_ == 'admin/login' and request.user.is_staff:
                return redirect('/admin/')
            return redirect(next_)
        else:
            # иначе считаем попытки и устанавливаем время разблокировки и статус блокировки
            obj.attempts += 1
            if self.attempts_15_minutes_block or obj.attempts == self.attempts_15_minutes_block * 2:
                obj.time_unblock = timezone.now() + timezone.timedelta(minutes=15)
                obj.status = True
            elif obj.attempts == self.attempts_24_hours_block:
                obj.time_unblock = timezone.now() + timezone.timedelta(1)
                obj.status = True
            elif obj.attempts > self.attempts_24_hours_block:
                obj.attempts = 1
            obj.save()

        context = self.create_context_username_csrf(request)
        context['form'] = form

        return render(request, self.template_name, context=context)

    def create_context_username_csrf(self, request):
        """
            Вспомогательный метод для формирования контекста с csrf_token
            и добавлением формы авторизации в этом контексте
        """
        context = {}
        context.update(csrf(request))
        context['form'] = self.get_form_class()
        return context


class RegisterView(FormView):
    template_name = 'my_auth/register/register.html'
    form_class = ConfirmedUserCreationForm
    success_url = reverse_lazy('my_auth:register_done')

    def form_valid(self, form):
        # use_https = self.request.is_secure(),
        user = form.save()
        # Отправить письмо асинхронно?
        user.send_confirmation()
        return super().form_valid(form)


class RegisterDoneView(TemplateView):
    template_name = 'my_auth/register/register_done.html'


class RegisterConfirmView(View):
    """
        Если токен действующий то подтвердить юзера
        иначе редирект на confirm_fail
        Если юзер уже подтвержден то редирект на confirm_done
        Если юзер не зареган то вернуть 404
    """
    def get(self, request, token):
        username = check_temp_url_token(token)
        if username:
            user = get_object_or_404(ConfirmedUser, username=username)
            user.confirm = True
            user.save()
            return redirect('my_auth:register_confirm_done')
        return redirect('my_auth:register_confirm_fail')  


class RegisterConfirmDoneView(TemplateView):
    template_name = 'my_auth/register/register_confirm_done.html'


class RegisterConfirmFailView(TemplateView):
    template_name = 'my_auth/register/register_confirm_fail.html'


class SendConfirmView(LoginRequiredMixin, View):
    """
        Повторная отправка ссылки на подтверждение
        Отправляется из закрытой части сайта уже залогиненому юзеру
    """
    def get(self, request):
        user = get_object_or_404(ConfirmedUser, pk=request.user.pk)
        # use_https = request.is_secure(),
        user.send_confirmation()
        return redirect('my_auth:register_done')


class ResendConfirmView(FormView):
    """Отправка новой ссылки подтверждения"""
    template_name = 'my_auth/register/resend_confirm.html'
    form_class = ResendConfirmForm
    success_url = reverse_lazy('my_auth:register_done')
    
    def form_valid(self, form):
        user = get_object_or_404(ConfirmedUser, email=form.cleaned_data['email'])
        # use_https = self.request.is_secure(),
        user.send_confirmation()
        super(ResendConfirmView, self).form_valid(form)