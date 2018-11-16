# Generated by Django 2.1.2 on 2018-10-29 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_auto_20181009_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='media',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='Verarbeitet'),
        ),
        migrations.AddField(
            model_name='report',
            name='media_note',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Credit'),
        ),
        migrations.AddField(
            model_name='report',
            name='media_original',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='Medien-Anhang'),
        ),
        migrations.AddField(
            model_name='reporttranslation',
            name='media',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='Verarbeitet'),
        ),
        migrations.AddField(
            model_name='reporttranslation',
            name='media_note',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Credit'),
        ),
        migrations.AddField(
            model_name='reporttranslation',
            name='media_original',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='Medien-Anhang'),
        ),
    ]