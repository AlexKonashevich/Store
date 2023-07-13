from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from django.urls import reverse_lazy
from products.models import Basket
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView, UpdateView
from users.models import User
from django.contrib.messages.views import SuccessMessageMixin
from common.views import TitleMixin


class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Store - Авторизация'


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Поздравляем! Вы успешно зарегистрированы!'
    title = 'Store - Регистрация'


class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('index')
    title = 'Store - Личный кабинет'

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data()
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        return context

    # def login(request):
    #     if request.method == 'POST':
    #         form = UserLoginForm(data=request.POST)
    #         if form.is_valid():
    #             username = request.POST['username']
    #             password = request.POST['password']
    #             user = auth.authenticate(username=username, password=password)
    #             if user:
    #                 auth.login(request, user)
    #                 return HttpResponseRedirect(reverse('index'))
    #     else:
    #         form = UserLoginForm()
    #     context = {'form': form}
    #     return render(request, 'users/login.html', context)


# def register(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Поздравляем! Вы успешно зарегистрированы!')
#             return HttpResponseRedirect(reverse('users:login'))
#     else:
#         form = UserRegistrationForm()
#     context = {'form': form}
#     return render(request, 'users/register.html', context)


# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('users:profile'))
#     else:
#         form = UserProfileForm(instance=request.user)
#
#     context = {'title': 'Store - Профиль',
#                'form': form,
#                'baskets': Basket.objects.filter(user=request.user),
#                }
#     return render(request, 'users/profile.html', context)


# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('index'))
