from django.contrib import admin
from django import forms
from emoji_picker.widgets import EmojiPickerTextarea, EmojiPickerTextInput

from ..models.faq import FAQ, FAQFragment
from .attachment import AttachmentAdmin, DisplayImageWidgetStackedInline

class FAQFragmentModelForm(forms.ModelForm):
    question = forms.CharField(
        required=False, label="Frage", widget=EmojiPickerTextInput, max_length=20)
    text = forms.CharField(
        required=True, label="Text", widget=EmojiPickerTextarea, max_length=640)

    class Meta:
        model = FAQFragment
        fields = ['question', 'text', 'media', 'media_original', 'media_note']


class FAQFragmentAdminInline(DisplayImageWidgetStackedInline):
    model = FAQFragment
    form = FAQFragmentModelForm

    extra = 0


class FAQModelForm(forms.ModelForm):
    text = forms.CharField(
        required=True, label="Text", widget=EmojiPickerTextarea, max_length=640)

    slug = forms.CharField(
        label='Slug', help_text="Wird automatisch ausgefüllt", disabled=True,
        required=False)

    class Meta:
        model = FAQ
        fields = ['name', 'slug', 'text', 'media', 'media_original', 'media_note']


class FAQAdmin(AttachmentAdmin):
    form = FAQModelForm
    search_fields = ['name', 'slug']
    list_display = ('name', 'slug')
    inlines = (FAQFragmentAdminInline, )


# Register your models here.
admin.site.register(FAQ, FAQAdmin)
