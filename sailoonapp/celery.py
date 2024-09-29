from django.utils import timezone
from datetime import timedelta
from django.core.management.base import BaseCommand
from sailoonapp.models import User

class Command(BaseCommand):
    help = 'Delete users who have been deactivated for more than 90 days.'

    def handle(self, *args, **kwargs):
        cutoff_date = timezone.now() - timedelta(days=90)
        users_to_delete = User.objects.filter(is_active=False, deactivated_at__lte=cutoff_date)
        count = users_to_delete.count()
        users_to_delete.delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} user(s).'))


# active_users = User.objects.filter(is_active=True)
