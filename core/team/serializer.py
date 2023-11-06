from rest_framework import serializers

from team.models import Team

class TeamSerializer(serializers.Serializer):
    reference_id = serializers.CharField(read_only=True)
    member_name = serializers.CharField(required=True, error_messages={'required': 'Memmber name is null'})
    position = serializers.CharField(required=True,error_messages={'required': 'Position is null'})
    image = serializers.ImageField()


    def validate_member_name(self, value):
        if not value:
            raise serializers.ValidationError('member can not be null')
        
        return value

    def create(self, validated_data):
        return Team.objects.create(**validated_data)
    
    def update(self, instance , validated_data):
        instance.memmber_name = validated_data.get('member_name')
        instance.position = validated_data.get('position')
        instance.image = validated_data.get('image')
        instance.save()

        return instance