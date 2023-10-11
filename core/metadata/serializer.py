from rest_framework import serializers
from . models import MetaData


class MetaDataSerializer(serializers.Serializer):
    reference_id = serializers.CharField(read_only=True)
    website_name = serializers.CharField(required=True,
                                         error_messages={'required': 'website name can not be null.'})
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    landline_number = serializers.CharField()
    address_one = serializers.CharField()
    address_two = serializers.CharField()

    # def validate_website_name(self, value):
    #     if value is None or '':
    #         raise serializers.ValidationError(
    #             'website name  field can not be null')

    #     return value

    # def validate_phone_number(self, value):
    #     if len(value) != 10:
    #         raise serializers.ValidationError('phone must be 10 digits')
    #     return value

    def create(self, validation_data):
        return MetaData.objects.create(**validation_data)

    def update(self, instance,  validation_data):
        instance.website_name = validation_data.get('website_name')
        instance.email = validation_data.get('email')
        instance.phone_number = validation_data.get('phone_number')
        instance.landline_number = validation_data.get('landline_number')
        instance.address_one = validation_data.get('address_one')
        instance.address_two = validation_data.get('address_two')
        instance.save()
        return instance
