from rest_framework import serializers


class ImageSerializer(serializers.Serializer):
    image_path = serializers.CharField(label='path_of_image', required=True)
    attr = serializers.CharField(label="attr")
    attr_val = serializers.IntegerField()
