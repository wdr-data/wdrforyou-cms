from rest_framework import serializers, viewsets

from cms.models.report import ReportTranslation


class ReportTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportTranslation
        fields = ('id', 'language', 'text', )


class ReportTranslationViewSet(viewsets.ModelViewSet):
    queryset = ReportTranslation.objects.all().order_by('id')
    serializer_class = ReportTranslationSerializer


class ModelSerializerWithTranslations(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_representation(self, obj):
        rep = super().to_representation(obj)

        serializer = self.translation_serializer_class(many=True, read_only=True)
        translations = obj.translations.all()

        rep['translations'] = serializer.to_representation(translations)
        return rep
