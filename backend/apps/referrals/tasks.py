import logging

from celery import shared_task
from django.utils import timezone

from .models import CaseStatus, ReferralCase

logger = logging.getLogger(__name__)

OPEN_STATUSES = [status for status, _label in CaseStatus.choices if status != CaseStatus.CLOSED]


@shared_task(
    bind=True,
    autoretry_for=(OSError,),
    retry_backoff=True,
    retry_backoff_max=60,
    retry_jitter=True,
    max_retries=3,
    ignore_result=True,
)
def record_case_created(self, case_id: str) -> None:
    exists = ReferralCase.objects.filter(id=case_id, is_synthetic=True).exists()
    if exists:
        logger.info("Synthetic referral accepted case_id=%s", case_id)


@shared_task(ignore_result=True)
def scan_referral_deadlines(batch_size: int = 100) -> int:
    bounded_batch_size = max(1, min(batch_size, 500))
    overdue_case_ids = list(
        ReferralCase.objects.filter(
            is_synthetic=True,
            status__in=OPEN_STATUSES,
            next_action_due__lt=timezone.now(),
        )
        .order_by("next_action_due")
        .values_list("id", flat=True)[:bounded_batch_size]
    )
    if overdue_case_ids:
        logger.warning("Synthetic referral deadlines overdue count=%s", len(overdue_case_ids))
    return len(overdue_case_ids)
