import os
from time import sleep
from posixpath import join as urljoin

from django.contrib import admin, messages
from django.db import transaction
from django.utils import timezone
from django import forms
from emoji_picker.widgets import EmojiPickerTextInput
from emoji_picker.widgets import EmojiPickerTextarea
import requests

from ..models.report import Report, ReportTranslation
from .translation import TranslationModelForm, TranslationAdminInline

PUSH_TRIGGER_URL = urljoin(os.environ['BOT_SERVICE_ENDPOINT'], 'sendReport')

class ReportTranslationModelForm(TranslationModelForm):

    class Meta:
        model = ReportTranslation
        fields = ['language', 'text']


class ReportTranslationAdminInline(TranslationAdminInline):
    model = ReportTranslation
    form = ReportTranslationModelForm

    extra = 1

class ReportModelForm(forms.ModelForm):

    headline = forms.CharField(label='Überschrift', widget=EmojiPickerTextInput, max_length=200)
    text = forms.CharField(
        required=True, label="Text Deutsch", widget=EmojiPickerTextarea, max_length=640)

    delivered = forms.BooleanField(
        label='Versendet',
        help_text="Wurde diese Meldung bereits in einem Highlights-Push vom Bot versendet?",
        disabled=True,
        required=False)

    class Meta:
        model = Report
        fields = ['created', 'published', 'delivered',
            'headline', 'arabic', 'persian', 'english', 'text']

class ReportAdmin(admin.ModelAdmin):
    form = ReportModelForm
    inlines = (ReportTranslationAdminInline, )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
    
        try:
            if obj.published and not obj.delivered:

                def commit_hook():
                    sleep(1)  # Wait for DB
                    r = requests.post(
                        url=PUSH_TRIGGER_URL,
                        json={'id': obj.id}
                    )

                    if r.status_code == 200:
                        messages.success(request, '🚨 Nachricht wird jetzt gesendet...')

                    else:
                        messages.error(request, '🚨 Nachricht konnte nicht gesendet werden!')

                transaction.on_commit(commit_hook)

        except Exception as e:
            messages.error(request, str(e))


# Register your models here.
admin.site.register(Report, ReportAdmin)
