from django.core.management.base import BaseCommand, CommandError
from speakez_core.models import Refugee

class Command(BaseCommand):
    help = 'Add 2 test departments for testing UI'

    def handle(self, *args, **options):
        if (Refugee.objects.all().count() > 0):
            Refugee.objects.all().delete()
        refugee1 = Refugee.objects.create(
            first_name="John",
            middle_name="W.",
            last_name= 'Smith',
            gender="male",
            age=22,
            phone_number="123-456-7890",
            demographic_info="Test",
            ethnicity="White",
            street_number="17 B.",
            street_name="Main St.",
            city="Syracuse",
            zip_code="13210",
            martial_status="single",
        )
        refugee1.save()
        refugee2 = Refugee.objects.create(
            first_name="Jane",
            middle_name="D.",
            last_name= 'Johnson',
            gender="female",
            age=37,
            phone_number="123-456-7890",
            demographic_info="Test",
            ethnicity="White",
            street_number="17 B.",
            street_name="Main St.",
            city="Syracuse",
            zip_code="13210",
            martial_status="single",
        )
        refugee2.save()
        length = Refugee.objects.all().count()
        self.stdout.write(self.style.SUCCESS('Successfully created ' + str(length) + ' test refugee models'))