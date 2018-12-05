from rest_framework import viewsets, serializers

from cms.models.faq import FAQFragment, FAQ

class FAQFragmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQFragment
        fields = ('id', 'question', 'text', 'media', 'media_original', 'media_note', )

class ModelSerializerWithFragments(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_representation(self, obj):
        rep = super().to_representation(obj)

        serializer = self.fragment_serializer_class(many=True, read_only=True)
        fragments = obj.fragments.all()

        rep['faq'] = serializer.to_representation(fragments)
        return rep

class FragmentSerializer(ModelSerializerWithFragments):
    fragment_serializer_class = FAQFragmentSerializer

    class Meta:
        model = FAQ
        fields = ('id', 'name', 'slug', 'text', 'media_original', 'media_note', 'media',  )


class FragmentViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.order_by('-id')
    serializer_class = FragmentSerializer
