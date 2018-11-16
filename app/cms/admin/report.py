import os
from time import sleep
from posixpath import join as urljoin

from django.contrib import admin, messages
from django.db import transaction
from django import forms
from emoji_picker.widgets import EmojiPickerTextInput
from emoji_picker.widgets import EmojiPickerTextarea
import requests

from ..models.report import Report, ReportTranslation
from .translation import TranslationModelForm, TranslationAdminInline
from .attachment import AttachmentAdmin

PUSH_TRIGGER_URL = urljoin(os.environ['BOT_SERVICE_ENDPOINT'], 'sendReport')


class ReportTranslationModelForm(TranslationModelForm):

    class Meta:
        model = ReportTranslation
        fields = ['language', 'text', 'link', 'media', 'media_original', 'media_note']


class ReportTranslationInlineFormset(forms.models.BaseInlineFormSet):
    def is_valid(self):
        return super().is_valid() and not any([bool(e) for e in self.errors])

    def clean(self):

        super().clean()

        if not self.instance.published:
            return

        # get forms that actually have valid data
        filled_translations = []

        for form in self.forms:
            try:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    filled_translations.append(form.cleaned_data['language'])
            except AttributeError:
                # annoyingly, if a subform is invalid Django explicity raises
                # an AttributeError for cleaned_data
                pass

        required_translations = [
            language for language in ('english', 'arabic', 'persian')
            if getattr(self.instance, language)
        ]

        missing_translations = []

        for required_translation in required_translations:
            if required_translation not in filled_translations:
                missing_translations.append(required_translation)

        if missing_translations:
            raise forms.ValidationError(
                "Fehlende Übersetzungen: " +
                ', '.join(l.capitalize() for l in missing_translations))


class ReportTranslationAdminInline(TranslationAdminInline):
    model = ReportTranslation
    form = ReportTranslationModelForm
    formset = ReportTranslationInlineFormset

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
        fields = ['published', 'delivered',
            'headline', 'arabic', 'persian', 'english', 'text', 'link', 
            'media', 'media_original', 'media_note']


class ReportAdmin(AttachmentAdmin):
    form = ReportModelForm
    list_display = ('published', 'delivered', 'headline', 'created', 'translations',)
    list_display_links = ('headline', )
    inlines = (ReportTranslationAdminInline, )

    def translations(self, obj):
        languages = [
            language for language in ('english', 'arabic', 'persian')
            if getattr(obj, language)
        ]
        translated_languages = [
            t.language for t in obj.translations.all()
        ]
        return [('✅ ' if l in translated_languages else '❌ ') + l.capitalize() for l in languages]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        all_messages = messages.get_messages(request)

        errors = [msg for msg in all_messages if msg.level == messages.ERROR]

        # Getting messages from the request deletes them, so we have to re-add them
        for message in all_messages:
            messages.add_message(
                request, message.level, message.message, extra_tags=message.extra_tags)
    
        try:
            if obj.published and not obj.delivered and not errors:

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

            elif obj.published and not obj.delivered and errors:
                messages.warning(
                    request, 'Nachricht wurde nicht versendet, da Fehler aufgetreten sind')

        except Exception as e:
            messages.error(request, str(e))


ReportAdmin.translations.short_description = 'Übersetzungen'

# Register your models here.
admin.site.register(Report, ReportAdmin)
