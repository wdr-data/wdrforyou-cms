from django.contrib import admin
from django.utils import timezone
from django import forms
from emoji_picker.widgets import EmojiPickerTextInput
from emoji_picker.widgets import EmojiPickerTextarea

from ..models.report import Report, ReportTranslation
from .translation import TranslationModelForm, TranslationAdminInline

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
        obj.modified = timezone.now()
        if obj.published and obj.published_date is None:
            obj.published_date = timezone.now()

        super().save_model(request, obj, form, change)

# Register your models here.
admin.site.register(Report, ReportAdmin)
