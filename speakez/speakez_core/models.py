from django.db import models
import uuid
from datetime import datetime
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField
from django.core.validators import FileExtensionValidator

# Create your models here.

class Refugee(models.Model):
    class Meta:
        verbose_name = 'Refugee'
        verbose_name_plural = "Refugees"

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

    phone_number = models.CharField(_("Phone Number"), max_length=25, blank=False, null=False)
    demographic_info = models.CharField(_("Demographic Info"), max_length=250, blank=True, null=True)
    ethnicity = models.CharField(_("Ethinicity"), max_length=250, blank=True, null=True)

    # Address
    street_number = models.CharField(_("Street Number"), max_length=30, blank=True, null=True)
    street_name = models.CharField(_("Street Name"), max_length=150, blank=True, null=True)
    city = models.CharField(_("City"), max_length=200, blank=True, null=True)
    zip_code = models.CharField(_("ZIP Code"), max_length=10, blank=True, null=True)

    emergency_contact = models.CharField(_("Emergency Contact"), max_length=300, blank=True, null=True)
    martial_status = models.CharField(max_length=9, choices=MARTIAL_STATUSES, default=SINGLE)

    def __str__(self):
        return self.last_name + ', ' + self.first_name

    def get_name(self):
        return self.first_name + " " + self.middle_name + " " + self.last_name

    def get_refugee_id(self):
        return self.id


class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = "Categories"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    date_time_created = models.DateTimeField(_("Date and Time Created"), default=timezone.now)
    title = models.CharField(_("Title"), max_length=250)

    def __str__(self):
        return self.title


class CallMessage(models.Model):
    class Meta:
        verbose_name = 'Call Message'
        verbose_name_plural = "Call Messages"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_time_created = models.DateTimeField(_("Date and Time Created"), default=timezone.now)
    duration = models.FloatField(_("Duration in seconds"))
    title = models.CharField(_("Title"), max_length=250)
    content = models.TextField(_("Content"), blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    audio = models.FileField(_("Audio"), upload_to='uploads/', validators=[FileExtensionValidator(allowed_extensions=['wav'])], blank=True, null=True)

    def __str__(self):
        return self.title


class CallLog(models.Model):
    class Meta:
        verbose_name = 'Call Log'
        verbose_name_plural = "Call Logs"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    admin_id = models.CharField(_("caller id"), max_length=250, blank=False, null=False)
    admin_username = models.CharField(_("caller username"), max_length=250, blank=False, null=False)
    date_time_created = models.DateTimeField(_("Date and Time Created"), default=timezone.now)
    message_sent = models.ForeignKey(CallMessage, on_delete=models.CASCADE)

 

class CallLogDetail(models.Model):
    class Meta:
        verbose_name = 'Call Log Detail'
        verbose_name_plural = "Call Log Details"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient = models.ForeignKey(Refugee, on_delete=models.CASCADE)
    call_sid = models.CharField(_("twilio call sid"), max_length=34, blank=False, null=False)
    call_log = models.ForeignKey(CallLog, on_delete=models.CASCADE)


class CallStatus(models.Model):
    class Meta:
        verbose_name = 'Call Status'
        verbose_name_plural = "Call Statuses"

    Called = models.CharField(_("phone number being called"), max_length=64)
    ToState = models.CharField(_(""), max_length=64)
    CallerCountry = models.CharField(_(""), max_length=64)
    Direction = models.CharField(_(""), max_length=64)
    Timestamp = models.CharField(_(""), max_length=64)
    CallbackSource = models.CharField(_(""), max_length=64)
    SipResponseCode = models.CharField(_(""), max_length=64)
    CallerState = models.CharField(_(""), max_length=64)
    ToZip = models.CharField(_(""), max_length=64)
    SequenceNumber = models.CharField(_(""), max_length=64)
    CallSid = models.CharField(primary_key=True, max_length=64)
    To = models.CharField(_(""), max_length=64)
    CallerZip = models.CharField(_(""), max_length=64)
    ToCountry = models.CharField(_(""), max_length=64)
    CalledZip = models.CharField(_(""), max_length=64)
    ApiVersion = models.CharField(_(""), max_length=64)
    CalledCity = models.CharField(_(""), max_length=64)
    CallStatus = models.CharField(_(""), max_length=64)
    Duration = models.CharField(_(""), max_length=64)
    From = models.CharField(_(""), max_length=64)
    CallDuration = models.CharField(_(""), max_length=64)
    AccountSid = models.CharField(_(""), max_length=64)
    CalledCountry = models.CharField(_(""), max_length=64)
    CallerCity = models.CharField(_(""), max_length=64)
    ToCity = models.CharField(_(""), max_length=64)
    FromCountry = models.CharField(_(""), max_length=64)
    Caller = models.CharField(_(""), max_length=64)
    FromCity = models.CharField(_(""), max_length=64)
    CalledState = models.CharField(_(""), max_length=64)
    FromZip = models.CharField(_(""), max_length=64)
    AnsweredBy = models.CharField(_(""), max_length=64)
    FromState = models.CharField(_(""), max_length=64)
