# Generated by Django 2.1.2 on 2018-10-09 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0002_auto_20181009_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporttranslation',
            name='language',
            field=models.CharField(choices=[('arabic', 'Arabisch'), ('persian', 'Persisch'), ('english', 'Englisch')], max_length=640, verbose_name='Sprache'),
        ),
    ]
