from django import forms
from django.contrib import admin

from emoji_picker.widgets import EmojiPickerTextarea


class TranslationModelForm(forms.ModelForm):
    text = forms.CharField(
        required=True, label="Text", widget=EmojiPickerTextarea, max_length=640)


class TranslationAdminInline(admin.StackedInline):
    extra = 1
