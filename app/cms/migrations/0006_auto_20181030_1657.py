# Generated by Django 2.1.2 on 2018-10-30 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0005_report_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='link',
            field=models.CharField(blank=True, help_text='Hier eine Link-URL eintragen, wird als Button an die Push-Nachricht angehängt.', max_length=1024, null=True, verbose_name='Link'),
        ),
    ]
