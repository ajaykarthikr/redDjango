from django.core.management.base import BaseCommand
from administration.models import User
from essentials.methods import encryptPassword
from redDjango.constants import APP_NAME, DOMAIN_NAME, SUPERUSER_ACCESS
from administration.company.methods import addCompanyAdmin


class Command(BaseCommand):
    help = 'Creates a superuser'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        name = '%s Super User' % APP_NAME
        email = 'superuser@%s' % DOMAIN_NAME
        password = encryptPassword(SUPERUSER_ACCESS)
        u = User.objects.create(
            name=name, email=email, password=password,
            isVerified=True)
        addCompanyAdmin(u)
        self.stdout.write(self.style.SUCCESS(
            'Superuser created successfully. Email: ' + email))
