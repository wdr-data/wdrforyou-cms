from django.utils import timezone
from django.db import models

from .translations import Translation
from .attachment import Attachment


class Report(Attachment):
    """
    Meldungen sind themenbezogene, in sich abgeschlossene Nachrichten.</p><p>
    Sie enthalten eine Information auf Deutsch. Zudem können Fragmente mit der Übersetzung
    zu weiteren Sprachen enthalten sein.
    """

    class Meta:
        verbose_name = 'Meldung'
        verbose_name_plural = 'Meldungen'
        ordering = ['-created']

    published = models.BooleanField(
        'Freigegeben', null=False, default=False,
        help_text='Solange dieser Haken nicht gesetzt ist, wird diese Meldung nicht versendet und/oder angezeigt.')
    delivered = models.BooleanField(
        'Versendet', null=False, default=False)
    created = models.DateTimeField(
        'Erstellt',
        default=timezone.now)

    headline = models.CharField('Titel', max_length=200, null=False)
    german = models.BooleanField('Deutsch', null=False, blank=True, default=False)
    arabic = models.BooleanField(
        'Arabisch',
        help_text="Soll auf Arabisch übersetzt werden",
        null=False,
        blank=True,
        default=False)
    persian = models.BooleanField(
        'Persisch',
        help_text="Soll auf Persisch übersetzt werden",
        null=False,
        blank=True,
        default=False)
    english = models.BooleanField(
        'Englisch',
        help_text="Soll auf Englisch übersetzt werden",
        null=False,
        blank=True,
        default=False)

    text = models.CharField('Text Deutsch', max_length=628, null=False)
    link = models.CharField(
        'Link', max_length=1024, null=True, blank=True,
        help_text='Hier eine Link-URL eintragen, wird als Button an die Push-Nachricht angehängt.')

    def __str__(self):
        return self.headline

    @classmethod
    def last(cls, *, count=1, offset=0, only_published=True, delivered=False, by_date=True):
        reports = cls.objects.all()

        if only_published:
            reports = reports.filter(published=True)

        if not delivered:
            reports = reports.filter(delivered=False)

        if by_date:
            reports = reports.order_by('-created')
        else:
            reports = reports.order_by('-id')

        return reports[offset:count]


class ReportTranslation(Translation):

    class Meta:
        verbose_name = 'Meldungs-Übersetzung'
        verbose_name_plural = 'Meldungs-Übersetzung'
        ordering = ('id', )

    report = models.ForeignKey('Report', on_delete=models.CASCADE, related_name='translations',
                               related_query_name='translation')

    def __str__(self):
        return self.report.headline
