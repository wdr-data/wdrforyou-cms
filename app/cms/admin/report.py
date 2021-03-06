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
        fields = ['language', 'published', 'delivered', 'text', 'link', 'media', 'media_original', 'media_note']


class ReportTranslationInlineFormset(forms.models.BaseInlineFormSet):
    def is_valid(self):
        return super().is_valid() and not any([bool(e) for e in self.errors])


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
        max_length=305)

    delivered = forms.BooleanField(
        label='Versendet',
        help_text="Wurde diese Meldung bereits vom Bot versendet?",
        disabled=True,
        required=False)

    class Meta:
        model = Report
        fields = ['headline', 'published', 'delivered', 'text', 'link',
                  'media', 'media_original', 'media_note', 'arabic', 'persian', 'english',]


class ReportAdmin(AttachmentAdmin):
    form = ReportModelForm
    list_display = ('created', 'headline', 'deutsch', 'translations',)
    list_display_links = ('headline',)
    inlines = (ReportTranslationAdminInline,)

    def translations(self, obj):
        languages = [
            language for language in ('english', 'arabic', 'persian')
            if getattr(obj, language)
        ]
        translated_languages = {
            t.language: t for t in obj.translations.all()
        }

        display = []
        for lang in languages:

            if lang not in translated_languages:
                item = '❌️ '
            elif translated_languages[lang].delivered:
                item = '📤 '
            elif translated_languages[lang].published:
                item = '✅ '
            else:
                item = '✏️️ '

            item += lang.capitalize()
            display.append(item)

        return display

    def deutsch(self, obj):
        if obj.delivered:
            display = '📤 '
        elif obj.published:
            display = '✅ '
        else:
            display = '✏️️ '

        return display

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
            if not errors:

                def commit_hook(id):
                    sleep(1)  # Wait for DB

                    obj = Report.objects.get(id=id)

                    if not ((obj.published and not obj.delivered
                             or any(t.published and not t.delivered for t in obj.translations.all()))
                            and obj.published):
                        return

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

                transaction.on_commit(lambda: commit_hook(obj.id))

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
