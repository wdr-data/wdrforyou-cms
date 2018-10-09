from django.db import models


class Translation(models.Model):

    class Meta:
        verbose_name = 'Übersetzung'
        verbose_name_plural = 'Übersetzungen'
        abstract = True
    
    ARABIC = 'arabic'
    PERSIAN = 'persian'
    ENGLISH = 'english'

    language = models.CharField('Sprache', null=False, max_length=640,
        choices=[
            (ARABIC, 'Arabisch'),
            (PERSIAN, 'Persisch'),
            (ENGLISH, 'Englisch')])
    text = models.CharField('Text Übersetzung', max_length=640, null=False, blank=False)
