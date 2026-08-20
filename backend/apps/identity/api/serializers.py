from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    password = serializers.CharField(
        min_length=1,
        max_length=256,
        trim_whitespace=False,
        write_only=True,
        style={"input_type": "password"},
    )
