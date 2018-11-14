from django.db import models
from .attachment import Attachment


class Translation(Attachment):

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
    text = models.CharField('Text Übersetzung', max_length=628, null=False, blank=False)
    link = models.CharField(
        'Link', max_length=1024, null=True, blank=True,
        help_text='Hier eine Link-URL eintragen, wird als Button an die Push-Nachricht angehängt.')
