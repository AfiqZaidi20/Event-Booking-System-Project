from django.contrib import admin
from .models import Event, Booking, Payment, CongregateMember, MosqueCommunity, HeadOfMosqueCommunity, BookingReport

# DO NOT include SystemUser since it's no longer in your models.py

admin.site.register(Event)
admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(CongregateMember)
admin.site.register(MosqueCommunity)
admin.site.register(HeadOfMosqueCommunity)
admin.site.register(BookingReport)
