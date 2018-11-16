from django import forms
from django.contrib import admin

from emoji_picker.widgets import EmojiPickerTextarea

from .attachment import DisplayImageWidgetStackedInline


class TranslationModelForm(forms.ModelForm):
    text = forms.CharField(
        required=True,
        label="Text übersetzt",
        help_text="Hier nur den Meldungstext in der ausgewählten Sprache eintragen.",
        widget=EmojiPickerTextarea,
        max_length=640)


class TranslationAdminInline(DisplayImageWidgetStackedInline):
    image_display_fields = ['media']
    extra = 1
