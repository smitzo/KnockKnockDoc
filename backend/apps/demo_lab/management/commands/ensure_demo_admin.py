from django.core.management.base import BaseCommand, CommandError

from apps.demo_lab.bootstrap import DemoCredentialError, ensure_demo_admin


class Command(BaseCommand):
    help = "Create or refresh only the persistent local prototype administrator."

    def handle(self, *args, **options):
        try:
            admin = ensure_demo_admin()
        except DemoCredentialError as exc:
            raise CommandError(str(exc)) from exc
        self.stdout.write(
            self.style.SUCCESS(
                f"Ensured local prototype administrator {admin.username}; no password was printed."
            )
        )
