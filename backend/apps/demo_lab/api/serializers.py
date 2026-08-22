from rest_framework import serializers

from ..models import SyntheticDoctorProfile, SyntheticPatientProfile


class SyntheticDoctorSerializer(serializers.ModelSerializer):
    login_email = serializers.EmailField(
        source="user.identity_profile.normalized_email",
        read_only=True,
    )
    availability_label = serializers.CharField(source="get_availability_display", read_only=True)
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = SyntheticDoctorProfile
        fields = [
            "id",
            "fixture_key",
            "display_name",
            "login_email",
            "specialty",
            "city",
            "hospital_name",
            "experience_years",
            "languages",
            "availability",
            "availability_label",
            "response_hours",
            "credential_state",
            "avatar_url",
            "profile_summary",
            "is_synthetic",
        ]

    def get_avatar_url(self, instance):
        return f"/demo/avatar/{instance.avatar_key}"


class SyntheticPatientSerializer(serializers.ModelSerializer):
    login_email = serializers.EmailField(
        source="user.identity_profile.normalized_email",
        read_only=True,
    )
    journey_stage_label = serializers.CharField(source="get_journey_stage_display", read_only=True)
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = SyntheticPatientProfile
        fields = [
            "id",
            "fixture_key",
            "display_alias",
            "login_email",
            "home_country",
            "age_band",
            "specialty_interest",
            "journey_stage",
            "journey_stage_label",
            "preferred_city",
            "language",
            "coordination_need",
            "avatar_url",
            "is_synthetic",
        ]

    def get_avatar_url(self, instance):
        return f"/demo/avatar/{instance.avatar_key}"
