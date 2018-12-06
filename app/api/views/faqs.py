from rest_framework import viewsets, serializers

from cms.models.faq import FAQFragment, FAQ, FAQTranslation


class FAQTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQTranslation
        fields = ('id', 'text', 'media', 'media_original', 'media_note', )


class FAQTranslationViewSet(viewsets.ModelViewSet):
    queryset = FAQTranslation.objects.all().order_by('id')
    serializer_class = FAQTranslationSerializer


class ModelSerializerWithFAQTranslations(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_representation(self, obj):
        rep = super().to_representation(obj)

        serializer = self.translation_serializer_class(many=True, read_only=True)
        translations = obj.translations.all()

        rep['translations'] = serializer.to_representation(translations)
        return rep


class FAQFragmentSerializer(ModelSerializerWithFAQTranslations):
    translation_serializer_class = FAQTranslationSerializer
    class Meta:
        model = FAQFragment
        fields = ('id', 'question', 'text', 'media', 'media_original', 'media_note', )


class FAQSerializer(serializers.ModelSerializer):

    class Meta:
        model = FAQ
        fields = ('id', 'name', 'slug', 'media_original', 'media_note', 'media',  )


class FragmentViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.order_by('-id')
    serializer_class = FAQSerializer
    filter_fields = ('id', 'slug')
