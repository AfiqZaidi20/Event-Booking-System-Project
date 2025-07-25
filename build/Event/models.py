from django.db import models

class CongregateMember(models.Model):
    con_id = models.AutoField(primary_key=True)
    con_name = models.CharField(max_length=150)
    con_password = models.TextField(max_length=20)
    con_phone_number = models.CharField(max_length=15)


class MosqueCommunity(models.Model):
    mc_id = models.AutoField(primary_key=True)
    mc_name = models.CharField(max_length=150)
    mc_password = models.TextField(max_length=20)
    mc_phone_number = models.CharField(max_length=15)


class HeadOfMosqueCommunity(models.Model):
    homc_id = models.AutoField(primary_key=True)
    homc_name = models.CharField(max_length=150)
    homc_password = models.TextField(max_length=20)
    homc_phone_number = models.CharField(max_length=15)


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=150)
    event_date = models.DateField()
    event_time = models.TimeField()
    booking_date = models.DateField()


class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    congregate_member = models.ForeignKey(CongregateMember, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    booking_date = models.DateField()
    payment_status = models.CharField(max_length=20, default='Pending')


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    con_id = models.ForeignKey(CongregateMember, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    booking_date = models.DateField()
    event_name = models.CharField(max_length=150)


class BookingReport(models.Model):
    report_id = models.AutoField(primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)