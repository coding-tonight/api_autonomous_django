from rest_framework import serializers

from clients.models import Clients


class ClientSerializer(serializers.Serializer):
    reference_id = serializers.CharField(read_only=True)
    client_name = serializers.CharField(required=True, error_messages={
                                        'required': 'client name can  not be null.'})
    logo_url = serializers.ImageField(
        required=True,
        error_messages={'required': 'logo can not be null'})

    def validate_client_name(self, value):
        """check if client is null or not
        """
        if value is None:
            raise serializers.ValidationError('Client is null')

        return value

    def validate_logo_url(self, value):
        """check if logo url is null or null
        """
        if value is None:
            raise serializers.ValidationError('logo image is null')

        return value

    def create(self, validated_data):
        """create client 
        """
        return Clients.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.client_name = validated_data.get('client_name')
        instance.logo_url = validated_data.get('logo_url')
        instance.save()

        return instance
