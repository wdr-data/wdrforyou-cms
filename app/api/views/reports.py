from rest_framework import viewsets

from cms.models.report import Report

from .translations import ReportTranslationSerializer, ModelSerializerWithTranslations


class ReportSerializer(ModelSerializerWithTranslations):
    translation_serializer_class = ReportTranslationSerializer

    class Meta:
        model = Report
        fields = ('id', 'created', 'published', 'delivered', 'headline', 'text', 'link',
            'german', 'arabic', 'persian', 'english', 'media', 'media_original', 'media_note', )


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.filter(published=True).order_by('-created')
    serializer_class = ReportSerializer
    filter_fields = ('arabic', 'persian', 'english', 'published', 'delivered')
