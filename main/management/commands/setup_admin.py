from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Jadid Mebel admin foydalanuvchisini yaratadi (yoki parolni yangilaydi)"

    def add_arguments(self, parser):
        parser.add_argument('--username', default='admin')
        parser.add_argument('--password', default='jadid123')
        parser.add_argument('--email', default='admin@jadidmebel.uz')

    def handle(self, *args, **options):
        User = get_user_model()
        username = options['username']
        password = options['password']
        email = options['email']

        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email, 'is_staff': True, 'is_superuser': True},
        )
        if not created:
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
        user.set_password(password)
        user.save()

        action = "yaratildi" if created else "yangilandi"
        self.stdout.write(self.style.SUCCESS(
            f"Admin {action}:\n"
            f"  Login:  {username}\n"
            f"  Parol:  {password}\n"
            f"  Kirish: http://127.0.0.1:8000/dashboard/login/"
        ))
