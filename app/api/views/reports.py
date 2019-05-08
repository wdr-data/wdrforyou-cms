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

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Report.objects.filter(published=True).order_by('-created')
        language = self.request.query_params.get('language', None)

        if language is not None:
            queryset = queryset.filter(translation__language=language, translation__published=True)

        return queryset

    serializer_class = ReportSerializer
    filter_fields = ('arabic', 'persian', 'english', 'published', 'delivered')
