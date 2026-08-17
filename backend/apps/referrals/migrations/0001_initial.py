import uuid

import django.db.models.deletion
from django.db import migrations, models
from django.db.models import Q


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ReferralCase",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("reference", models.CharField(max_length=24, unique=True)),
                ("patient_alias", models.CharField(max_length=80)),
                ("patient_country", models.CharField(max_length=80)),
                ("patient_age_band", models.CharField(max_length=30)),
                ("specialty", models.CharField(max_length=80)),
                ("clinical_question", models.CharField(max_length=500)),
                ("summary", models.TextField(max_length=2000)),
                ("status", models.CharField(choices=[("draft", "Draft"), ("awaiting_consent", "Awaiting consent"), ("completeness_review", "Completeness review"), ("ready_to_route", "Ready to route"), ("provider_review", "Provider review"), ("information_required", "Information required"), ("response_ready", "Response ready"), ("patient_decision", "Patient decision"), ("preparing_travel", "Preparing travel"), ("treatment", "Treatment"), ("handback", "Handback"), ("closed", "Closed")], default="draft", max_length=32)),
                ("consent_status", models.CharField(choices=[("not_requested", "Not requested"), ("pending", "Pending"), ("granted", "Granted"), ("declined", "Declined"), ("withdrawn", "Withdrawn")], default="not_requested", max_length=24)),
                ("is_planned_care", models.BooleanField(default=True)),
                ("is_synthetic", models.BooleanField(default=True)),
                ("corridor_label", models.CharField(default="Illustrative corridor", max_length=120)),
                ("next_action", models.CharField(max_length=280)),
                ("next_action_owner", models.CharField(max_length=100)),
                ("next_action_due", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "ordering": ["-updated_at"],
                "indexes": [models.Index(fields=["status", "next_action_due"], name="ref_case_queue_idx"), models.Index(fields=["updated_at"], name="ref_case_updated_idx")],
                "constraints": [models.CheckConstraint(condition=Q(("is_synthetic", True)), name="prototype_cases_synthetic"), models.CheckConstraint(condition=Q(("is_planned_care", True)), name="prototype_planned_care")],
            },
        ),
        migrations.CreateModel(
            name="CaseEvent",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("event_type", models.CharField(max_length=60)),
                ("actor_label", models.CharField(max_length=100)),
                ("actor_role", models.CharField(max_length=80)),
                ("summary", models.CharField(max_length=280)),
                ("occurred_at", models.DateTimeField()),
                ("case", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="events", to="referrals.referralcase")),
            ],
            options={"ordering": ["-occurred_at", "-created_at"], "indexes": [models.Index(fields=["case", "-occurred_at"], name="ref_event_timeline_idx")]},
        ),
        migrations.CreateModel(
            name="CaseParticipant",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("display_name", models.CharField(max_length=100)),
                ("role", models.CharField(choices=[("patient", "Patient"), ("referrer", "Referring doctor"), ("specialist", "Receiving specialist"), ("hospital", "Hospital team"), ("coordinator", "Care coordinator")], max_length=24)),
                ("organization", models.CharField(blank=True, max_length=120)),
                ("access_scope", models.CharField(max_length=240)),
                ("access_state", models.CharField(choices=[("active", "Active"), ("pending", "Pending"), ("revoked", "Revoked")], default="active", max_length=16)),
                ("purpose", models.CharField(max_length=160)),
                ("case", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="participants", to="referrals.referralcase")),
            ],
            options={"ordering": ["created_at"], "constraints": [models.UniqueConstraint(fields=("case", "display_name", "role"), name="unique_case_participant_label")]},
        ),
        migrations.CreateModel(
            name="InformationRequest",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("item", models.CharField(max_length=180)),
                ("reason", models.CharField(max_length=280)),
                ("requester_name", models.CharField(max_length=100)),
                ("requester_role", models.CharField(max_length=80)),
                ("state", models.CharField(choices=[("open", "Open"), ("answered", "Answered"), ("unavailable", "Unavailable")], default="open", max_length=20)),
                ("is_blocking", models.BooleanField(default=False)),
                ("due_at", models.DateTimeField(blank=True, null=True)),
                ("response_note", models.CharField(blank=True, max_length=280)),
                ("case", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="information_requests", to="referrals.referralcase")),
            ],
            options={"ordering": ["state", "due_at"]},
        ),
        migrations.CreateModel(
            name="ProviderResponse",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("response_type", models.CharField(choices=[("clinical_opinion", "Clinical opinion"), ("coordination_plan", "Coordination plan"), ("indicative_quote", "Indicative quote")], max_length=32)),
                ("title", models.CharField(max_length=160)),
                ("author_name", models.CharField(max_length=100)),
                ("author_role", models.CharField(max_length=100)),
                ("organization", models.CharField(max_length=140)),
                ("summary", models.TextField(max_length=1600)),
                ("limitations", models.TextField(max_length=800)),
                ("state", models.CharField(choices=[("draft", "Draft"), ("issued", "Issued"), ("superseded", "Superseded")], max_length=20)),
                ("issued_at", models.DateTimeField(blank=True, null=True)),
                ("version", models.PositiveSmallIntegerField(default=1)),
                ("case", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="responses", to="referrals.referralcase")),
            ],
            options={"ordering": ["-issued_at", "-created_at"], "constraints": [models.UniqueConstraint(fields=("case", "response_type", "version"), name="unique_case_response_version")]},
        ),
        migrations.CreateModel(
            name="RecordItem",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("label", models.CharField(max_length=140)),
                ("category", models.CharField(max_length=80)),
                ("clinical_date", models.DateField(blank=True, null=True)),
                ("source_label", models.CharField(max_length=120)),
                ("state", models.CharField(choices=[("ready", "Ready"), ("needs_update", "Needs update"), ("requested", "Requested"), ("unavailable", "Unavailable")], max_length=20)),
                ("note", models.CharField(blank=True, max_length=240)),
                ("case", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="records", to="referrals.referralcase")),
            ],
            options={"ordering": ["-clinical_date", "created_at"]},
        ),
    ]
