from django.db import models
import uuid
from datetime import datetime
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField

# Create your models here.

class Refugee(models.Model):
    SINGLE = 'single'
    MARRIED = 'married'
    MARTIAL_STATUSES = (
        (SINGLE, 'Single'),
        (MARRIED, 'MARRIED'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(_("First Name"), max_length=250, blank=True, null=True)
    middle_name = models.CharField(_("Middle Name"), max_length=250, blank=True, null=True)
    last_name = models.CharField(_("Last Name"), max_length=250, blank=True, null=True)
    gender = models.CharField(_("Gender"), max_length=100, blank=True, null=True)
    age = models.PositiveIntegerField(_("Age"), default=0)

    phone_number = models.CharField(_("Phone Number"), max_length=25, blank=True, null=True)
    demographic_info = models.CharField(_("Demographic Info"), max_length=250, blank=True, null=True)
    ethnicity = models.CharField(_("Ethinicity"), max_length=250, blank=True, null=True)

    # Address
    street_number = models.CharField(_("Street Number"), max_length=30, blank=True, null=True)
    street_name = models.CharField(_("Street Name"), max_length=150, blank=True, null=True)
    city = models.CharField(_("City"), max_length=200, blank=True, null=True)
    zip_code = models.CharField(_("ZIP Code"), max_length=10, blank=True, null=True)

    # Emergency contact ?
    martial_status = models.CharField(max_length=9, choices=MARTIAL_STATUSES, default=SINGLE)

    def __str__(self):
        return self.last_name + ', ' + self.first_name


