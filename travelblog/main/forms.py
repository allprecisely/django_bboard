from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from .apps import user_register
from main import models


class AuthenticationCustomForm(auth_forms.AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get('username')

        if not (qs_user := models.TravelUser.objects.filter(username=username)):
            raise ValidationError(_("A user with that username does not exist."))

        if not qs_user.first().is_active:
            raise ValidationError(_("This account is inactive."))

        return super().clean()


class ArticleForm(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = '__all__'
        widgets = {'author': forms.HiddenInput}


AIFormSet = forms.inlineformset_factory(
    models.Article, models.AdditionalImage, extra=2, fields='__all__'
)


class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')

    class Meta:
        model = models.TravelUser
        fields = ('username', 'email', 'first_name', 'last_name', 'send_messages')


class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label='Пароль (повторно)',
        widget=forms.PasswordInput,
        help_text='Введите тот же самый пароль еще раз для проверки',
    )

    def clean_password1(self):
        if password1 := self.cleaned_data['password1']:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {
                'password2': ValidationError(
                    'Введенные пароли не совпадают', code='password_mismatch'
                )
            }
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_register.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = models.TravelUser
        fields = (
            'username',
            'email',
            'password1',
            'password2',
            'first_name',
            'last_name',
            'send_messages',
        )


class CityForm(forms.ModelForm):
    country = forms.ModelChoiceField(
        queryset=models.Country.objects.all(),
        empty_label=None,
        label='Страна',
        required=True,
    )

    class Meta:
        model = models.City
        fields = '__all__'


class SearchForm(forms.Form):
    keyword = forms.CharField(required=False, max_length=20, label='')


class UserCommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        exclude = ('is_active',)
        widgets = {'article': forms.HiddenInput}


class GuestCommentForm(forms.ModelForm):
    captcha = CaptchaField(
        label='Введите текст с картинки',
        error_messages={'invalid': 'Неправильный ответ'},
    )

    class Meta:
        model = models.Comment
        exclude = ('is_active',)
        widgets = {'article': forms.HiddenInput}
