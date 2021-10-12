from django.contrib import admin
import datetime

from main import forms
from main import models
from .utilities import send_activation_notification


def send_activation_notifications(modeladmin, request, queryset):
    for rec in queryset:
        if not rec.is_activated:
            send_activation_notification(rec)
    modeladmin.message_user(request, 'Письма с требованиями отправлены')


send_activation_notifications.short_description = (
    'Отправка писем с требованиями активации'
)


class NonactivatedFilter(admin.SimpleListFilter):
    title = 'Прошли активацию?'
    parameter_name = 'actstate'

    def lookups(self, request, model_admin):
        return (
            ('activated', 'Прошли'),
            ('threedays', 'Не прошли более 3 дней'),
            ('week', 'Не прошли более недели'),
        )

    def queryset(self, request, queryset):
        val = self.value()
        if val == 'activated':
            return queryset.filter(is_active=True, is_activated=True)
        elif val == 'threedays':
            d = datetime.date.today() - datetime.timedelta(days=3)
            return queryset.filter(
                is_active=False, is_activated=False, data_joined__date__lt=d
            )
        elif val == 'week':
            d = datetime.date.today() - datetime.timedelta(days=7)
            return queryset.filter(
                is_active=False, is_activated=False, data_joined__date__lt=d
            )


class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_activated', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = (NonactivatedFilter,)
    fields = (
        ('username', 'email'),
        ('first_name', 'last_name'),
        ('send_messages', 'is_active', 'is_activated'),
        ('is_staff', 'is_superuser'),
        'groups',
        'user_permissions',
        ('last_login', 'date_joined'),
    )
    readonly_fields = ('last_login', 'date_joined')
    actions = (send_activation_notifications,)


class SubRubricAdmin(admin.ModelAdmin):
    form = forms.SubRubricForm


class SubRubricInline(admin.TabularInline):
    model = models.SubRubric


class SuperRubricAdmin(admin.ModelAdmin):
    exclude = ('super_rubric',)
    inlines = (SubRubricInline,)


class AdditionalImageInline(admin.TabularInline):
    model = models.AdditionalImage


class BbAdmin(admin.ModelAdmin):
    list_display = ('rubric', 'title', 'content', 'author', 'created_at')
    fields = (
        ('rubric', 'author'),
        'title',
        'content',
        'price',
        'contacts',
        'image',
        'is_active',
    )
    inlines = (AdditionalImageInline,)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'author', 'bb', 'content', 'created_at')
    search_fields = ('author',)
    readonly_fields = ('created_at',)


admin.site.register(models.AdvUser, AdvUserAdmin)
admin.site.register(models.SuperRubric, SuperRubricAdmin)
admin.site.register(models.Bb, BbAdmin)
admin.site.register(models.Comment, CommentAdmin)
