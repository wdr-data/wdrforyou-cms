from rest_framework import viewsets, serializers

from cms.models.faq import FAQFragment, FAQ, FAQTranslation


class FAQFragmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = FAQFragment
        fields = ('id', 'text', 'media', 'media_original', 'media_note', )


class FAQTranslationSerializer(serializers.ModelSerializer):

    class Meta:
        model = FAQTranslation
        fields = ('id', )

    def to_representation(self, obj):
        rep = super().to_representation(obj)

        serializer = FAQFragmentSerializer(many=True, read_only=True)
        fragments = obj.fragments.all()

        rep['fragments'] = serializer.to_representation(fragments)
        return rep


class FAQSerializer(serializers.ModelSerializer):
    german = FAQTranslationSerializer()
    english = FAQTranslationSerializer()
    arabic = FAQTranslationSerializer()
    persian = FAQTranslationSerializer()

    class Meta:
        model = FAQ
        fields = ('id', 'name', 'handle', 'german', 'english', 'arabic', 'persian')


class FragmentViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.order_by('-id')
    serializer_class = FAQSerializer
    filter_fields = ('id', 'handle')
