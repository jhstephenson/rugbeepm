from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a superuser'

    def handle(self, *args, **kwargs):
        if User.objects.filter(username='jstephen').exists():
            self.stdout.write(self.style.WARNING('Superuser "jstephen" already exists'))
            return

        try:
            User.objects.create_superuser(
                username='jstephen',
                email='jstephen@scc-i.com',
                password='acknbssb1',
                first_name='James',
                last_name='Stephenson'
            )
            self.stdout.write(self.style.SUCCESS('Superuser "jstephen" created successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating superuser: {str(e)}'))
