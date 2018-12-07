# Generated by Django 2.1.3 on 2018-12-05 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0008_auto_20181115_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='arabic',
            field=models.BooleanField(blank=True, default=False, help_text='Soll auf Arabisch übersetzt werden', verbose_name='Arabisch'),
        ),
        migrations.AlterField(
            model_name='report',
            name='english',
            field=models.BooleanField(blank=True, default=False, help_text='Soll auf Englisch übersetzt werden', verbose_name='Englisch'),
        ),
        migrations.AlterField(
            model_name='report',
            name='media_note',
            field=models.CharField(blank=True, help_text='Bei Foto-Anhang hier die Quelle eintragen. Wird auf dem Foto angezeigt.', max_length=100, null=True, verbose_name='Credit'),
        ),
        migrations.AlterField(
            model_name='report',
            name='persian',
            field=models.BooleanField(blank=True, default=False, help_text='Soll auf Persisch übersetzt werden', verbose_name='Persisch'),
        ),
        migrations.AlterField(
            model_name='report',
            name='text',
            field=models.CharField(max_length=628, verbose_name='Text Deutsch'),
        ),
        migrations.AlterField(
            model_name='reporttranslation',
            name='media_note',
            field=models.CharField(blank=True, help_text='Bei Foto-Anhang hier die Quelle eintragen. Wird auf dem Foto angezeigt.', max_length=100, null=True, verbose_name='Credit'),
        ),
    ]