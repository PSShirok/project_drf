from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@admin.admin',
            first_name='Admin',
            last_name='Home'
        )
        user.set_password('123qweasd')

        user.save()
