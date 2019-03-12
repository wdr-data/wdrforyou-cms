import os, re
from time import sleep
from posixpath import join as urljoin

from django.contrib import admin, messages
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from emoji_picker.widgets import EmojiPickerTextInput
from emoji_picker.widgets import EmojiPickerTextarea

import requests

from ..models.report import Report, ReportTranslation
from .translation import TranslationModelForm, TranslationAdminInline
from .attachment import AttachmentAdmin
from .slack import post_message, section, divider, context, element

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
    headline = forms.CharField(
        label='Überschrift',
        help_text="Überschrift für die Meldungen-Liste eintragen.",
        widget=EmojiPickerTextInput,
        max_length=200)

    text = forms.CharField(
        required=True,
        label="Text Deutsch",
        help_text="Hier nur die Meldung auf Deutsch eintragen. "
                  "Die Übersetzung zu anderen Sprachen wird weiter unten eingegeben, falls nötig.",
        widget=EmojiPickerTextarea,
        max_length=640)

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
    list_display_links = ('headline',)
    inlines = (ReportTranslationAdminInline,)

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

        languages = [lang for lang in ['arabic', 'persian', 'english'] if getattr(obj, lang)]
        cms_url = re.sub(r'/add/$', f'/{obj.id}/change', request.build_absolute_uri())

        if not change:
            blocks = [
                section(f"*🚨 Neue Meldung:* <{cms_url}|{obj.headline}>"),
                section(obj.text),
                divider(),
                section(f"🌐 Angeforderte <{cms_url}|Übersetzungen>: {', '.join(languages).upper()}"),
                context(element(f"Meldung von {request.user} angelegt.")),
            ]

            post_message(blocks=blocks)

        elif 'text' in form.changed_data:
            blocks = [
                section(f"*🚨 Update der Meldung! *"
                        f"<{cms_url}|🌐 Übersetzen> \n\n{obj.text}"),
                divider(),
                section(f"Angeforderte Übersetzungen: {', '.join(languages).upper()}"),
                divider(),
                context(element(f"Änderung von {request.user} vorgenommen.")),
            ]

            post_message(blocks=blocks)

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

                        blocks_success = [
                            section(f"🚀 Meldung abgenommen und auf dem Weg zum User!"),
                            context(element(f"Freigegeben von {request.user}. {str(timezone.now()-obj.created)}"))
                        ]
                        post_message(blocks=blocks_success)

                    else:
                        messages.error(request, '🚨 Nachricht konnte nicht gesendet werden!')

                transaction.on_commit(commit_hook)

            elif obj.published and not obj.delivered and errors:
                messages.warning(
                    request, 'Nachricht wurde nicht versendet, da Fehler aufgetreten sind')

        except Exception as e:
            messages.error(request, str(e))

    def save_formset(self, request, form, formset, change):
        super().save_formset(request, form, formset, change)
        blocks = []
        try:
            obj = formset.forms[0].instance.report
        except ObjectDoesNotExist:
            return

        languages = [lang for lang in ['arabic', 'persian', 'english'] if getattr(obj, lang)]
        cms_url = re.sub(r'/add/$', f'/{obj.id}/change', request.build_absolute_uri())

        for form_ in formset.forms:

            if form_.instance.language in languages:
                languages.remove(form_.instance.language)
                try:
                    if form_.cleaned_data and form_.cleaned_data.get('DELETE', True):
                        languages.append(form_.instance.language)
                except AttributeError:
                    # annoyingly, if a subform is invalid Django explicity raises
                    # an AttributeError for cleaned_data
                    pass

            if 'text' in form_.changed_data:
                blocks.extend(
                    [
                        section(f"*✏️ Übersetzung {form_.instance.language.upper()} * von {request.user}"),
                        section(f"{form_.instance.text}"),
                        divider(),
                    ]
                )

        if not languages and not obj.published:
            blocks.append(section(f"Alle Übersetzungen sind da! *<{cms_url}|🚀 Abnahme>*"))
        else:
            blocks.append(section(f"🌐 Fehlende *<{cms_url}| Übersetzungen>*: *{', '.join(languages).upper()}*"))

        if blocks:
            post_message(blocks=blocks)


ReportAdmin.translations.short_description = 'Übersetzungen'

# Register your models here.
admin.site.register(Report, ReportAdmin)
