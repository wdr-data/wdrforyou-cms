# Generated by Django 2.1.7 on 2019-05-08 10:03

from django.db import migrations


def mark_published(apps, schema_editor):
    ReportTranslation = apps.get_model("cms", "ReportTranslation")

    for rt in ReportTranslation.objects.all():
        rt.published = rt.report.published
        rt.delivered = rt.report.delivered

        rt.save()


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0012_auto_20190507_1207'),
    ]

    operations = [
        migrations.RunPython(mark_published)
    ]
