# jobs/serializers.py
from rest_framework import serializers
from .models import Job
import json

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

    def create(self, validated_data):
        payload = validated_data.pop('payload')
        payload_data = json.loads(payload)
        job = Job(**validated_data)
        job.set_payload(payload_data['func_name'], *payload_data['args'], **payload_data['kwargs'])
        job.save()
        return job

    def update(self, instance, validated_data):
        payload = validated_data.pop('payload', None)
        if payload:
            payload_data = json.loads(payload)
            instance.set_payload(payload_data['func_name'], *payload_data['args'], **payload_data['kwargs'])
        return super().update(instance, validated_data)
