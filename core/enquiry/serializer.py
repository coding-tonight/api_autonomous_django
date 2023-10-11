from rest_framework import serializers
from .models import Enquiry


class EnquirySerializer(serializers.Serializer):
    reference_id = serializers.CharField(read_only=True)
    full_name = serializers.CharField(required=True, error_messages={
                                      'required': 'Full Name is required.'})
    email = serializers.EmailField(
        error_messages={'required': 'email is  required.'})
    contact = serializers.CharField()
    message = serializers.CharField()

    # def validate_full_name(self, value):
    #     if len(value) == 0 or value is None:
    #         raise serializers.ValidationError('full name is null')
    #     return value

    def create(self, validation_data):
        return Enquiry.objects.create(**validation_data)

    def update(self, instance, validation_data):
        instance.full_name = validation_data.get('full_name')
        instance.email = validation_data.get('email')
        instance.contact = validation_data.get('contact')
        instance.message = validation_data.get('message')
        instance.save()
        return instance
