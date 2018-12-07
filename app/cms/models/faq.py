from django.db import models
from django.utils.text import slugify

from .attachment import Attachment


class FAQTranslation(models.Model):

    class Meta:
        verbose_name = 'FAQ Übersetzung'
        verbose_name_plural = 'FAQ Übersetzungen'

    def __str__(self):
        return f'{self.fragments.all()[0].text[:10] if self.fragments.all() else ""}...'


class FAQFragment(Attachment):

    class Meta:
        verbose_name = 'FAQ-Fragment'
        verbose_name_plural = 'FAQ-Fragmente'
        ordering = ('id', )

    text = models.CharField('Chat-Bubble', max_length=640, null=False, blank=False)
    translation = models.ForeignKey(
        FAQTranslation, on_delete=models.CASCADE, verbose_name='FAQ Übersetzung',
        related_name='fragments', null=False)

    def __str__(self):
        return f'{self.text[:10]}...'


class FAQ(models.Model):
    """
    FAQs werden über Payloads ausgespielt.
    """

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    name = models.CharField('Titel', max_length=200, null=False)
    handle = models.CharField('Handle', max_length=200, null=True, blank=True)

    german = models.ForeignKey(FAQTranslation, on_delete=models.CASCADE, verbose_name='Text Deutsch',
                               related_name='german_faqs', null=True)
    english = models.ForeignKey(FAQTranslation, on_delete=models.CASCADE, verbose_name='Text Englisch',
                                related_name='english_faqs', null=True, blank=True)
    arabic = models.ForeignKey(FAQTranslation, on_delete=models.CASCADE, verbose_name='Text Arabisch',
                               related_name='arabic_faqs', null=True, blank=True)
    persian = models.ForeignKey(FAQTranslation, on_delete=models.CASCADE, verbose_name='Text Persisch',
                                related_name='persian_faqs', null=True, blank=True)

    def __str__(self):
        return f'{self.name}'
