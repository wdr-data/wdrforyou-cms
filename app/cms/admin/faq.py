from django.contrib import admin
from django import forms
from emoji_picker.widgets import EmojiPickerTextarea, EmojiPickerTextInput

from ..models.faq import FAQ, FAQTranslation, FAQFragment
from .attachment import AttachmentAdmin, DisplayImageWidgetStackedInline


class FAQFragmentModelForm(forms.ModelForm):
    text = forms.CharField(
        required=True, label="Text", widget=EmojiPickerTextarea, max_length=640)

    class Meta:
        model = FAQFragment
        fields = ['text', 'media', 'media_original', 'media_note']


class FAQFragmentAdminInline(DisplayImageWidgetStackedInline):
    model = FAQFragment
    form = FAQFragmentModelForm

    fk_name = "translation"
    extra = 0


class FAQTranslationModelForm(forms.ModelForm):

    class Meta:
        model = FAQTranslation
        fields = []


class FAQTranslationAdmin(AttachmentAdmin):
    model = FAQTranslation
    form = FAQTranslationModelForm
    inlines = (FAQFragmentAdminInline, )


class FAQModelForm(forms.ModelForm):
    slug = forms.CharField(
        label='Slug', help_text="Wird automatisch ausgefüllt", disabled=True,
        required=False)

    class Meta:
        model = FAQ
        fields = ['name', 'slug', 'german', 'english', 'arabic', 'persian']


class FAQAdmin(AttachmentAdmin):
    form = FAQModelForm
    search_fields = ['name', 'slug']
    list_display = ('name', 'slug')


# Register your models here.
admin.site.register(FAQ, FAQAdmin)
admin.site.register(FAQTranslation, FAQTranslationAdmin)
