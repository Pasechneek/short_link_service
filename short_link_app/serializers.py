from rest_framework import serializers

from short_link_app.models import ShortLinkService


class ShortLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortLinkService
        fields = ('origin_link', 'short_link', 'count')
