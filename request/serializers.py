from rest_framework import serializers

from collection.models import Collection
from request.models import Request, KeyValueContainer


class CollectionLiteSerializer(serializers.ModelSerializer):

    def to_internal_value(self, data):
        return Collection.objects.get(pk=data)

    class Meta:
        model = Collection
        fields = ['id', 'name', 'type']
        read_only_fields = ['name', 'type']


class KeyValueContainerSerializer(serializers.ModelSerializer):

    class Meta:
        model = KeyValueContainer
        fields = ['enable', 'key', 'value', 'description']


class KeyValueContainerCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = KeyValueContainer
        fields = ['enable', 'type', 'key', 'value', 'description', 'request']


class RequestFullSerializer(serializers.ModelSerializer):
    collection = CollectionLiteSerializer(required=False)
    headers = KeyValueContainerSerializer(source='get_headers', many=True, required=False)
    params = KeyValueContainerSerializer(source='get_params', many=True, required=False)

    class Meta:
        model = Request
        fields = ['id', 'name', 'http_method', 'url', 'body', 'collection', 'headers', 'params']

    def validate_http_method(self, http_method):
        if http_method not in [Request.GET, Request.POST, Request.PUT, Request.DELETE]:
            raise serializers.ValidationError("your http method is not valid!")
        return http_method

    def create(self, validated_data):
        kvcs = dict()
        for kvc_type in [KeyValueContainer.HEADER, KeyValueContainer.PARAM]:
            key = str('get_' + kvc_type + 's')
            if key in validated_data:
                kvcs[kvc_type] = validated_data.pop(key)

        mhq_request = Request.objects.create(**validated_data)

        for kvc_type in kvcs.keys():
            for instance in kvcs[kvc_type]:
                instance['type'] = kvc_type
                instance['request'] = mhq_request.id
                instance = dict(instance)
                kvc_serializer = KeyValueContainerCreateSerializer(data=instance)
                kvc_serializer.is_valid(raise_exception=True)
                kvc_serializer.save()

        return mhq_request

    def update(self, instance, validated_data):
        for kvc_type in [KeyValueContainer.HEADER, KeyValueContainer.PARAM]:
            key = str('get_' + kvc_type + 's')
            if key not in validated_data:
                continue

            kvc_validated_datas = validated_data.pop(key)
            kvc_instances = []
            if kvc_type == KeyValueContainer.HEADER:
                kvc_instances = instance.get_headers()
            if kvc_type == KeyValueContainer.PARAM:
                kvc_instances = instance.get_params()

            for i in range(min(len(kvc_validated_datas), len(kvc_instances))):
                kvd = kvc_validated_datas[i]
                ki = kvc_instances[i]
                ki.enable = kvd.get('enable', ki.enable)
                ki.key = kvd.get('key', ki.key)
                ki.value = kvd.get('value', ki.value)
                ki.description = kvd.get('description', ki.description)
                ki.save()

            for i in range(min(len(kvc_validated_datas), len(kvc_instances)), len(kvc_validated_datas)):
                kvd = kvc_validated_datas[i]
                kvd['type'] = kvc_type
                kvd['request'] = instance.id
                kvd = dict(kvd)
                kvc_serializer = KeyValueContainerCreateSerializer(data=kvd)
                kvc_serializer.is_valid(raise_exception=True)
                kvc_serializer.save()

            for i in range(min(len(kvc_validated_datas), len(kvc_instances)), len(kvc_instances)):
                ki = kvc_instances[i]
                ki.delete()

        instance = super().update(instance, validated_data)
        instance.save()
        return instance
