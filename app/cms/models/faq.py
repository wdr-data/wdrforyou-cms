from django.db import models
from django.utils.text import slugify

from .attachment import Attachment


class FAQTranslation(Attachment):

    class Meta:
        verbose_name = 'FAQ Übersetzung'
        verbose_name_plural = 'FAQ Übersetzungen'

    text = models.CharField('Text Übersetzung', max_length=628, null=False, blank=False)

    def __str__(self):
        return f'{self.text}'


class FAQ(Attachment):
    """
    FAQs werden über Payloads ausgespielt.
    """

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    name = models.CharField('Titel', max_length=200, null=False)
    slug = models.CharField('Slug', max_length=200, null=True, blank=True)

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

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while FAQ.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


class FAQFragment(Attachment):

    class Meta:
        verbose_name = 'FAQ-Fragment'
        verbose_name_plural = 'FAQ-Fragmente'
        ordering = ('id', )

    question = models.CharField('Frage', max_length=20, null=True, blank=True)
    text = models.CharField('Text', max_length=640, null=False, blank=False)

    def __str__(self):
        return f'{self.faq.name} - {self.question}'
