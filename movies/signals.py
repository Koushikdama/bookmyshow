# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from .models import Booking, Seat

# @receiver(post_save, sender=Booking)
# def update_seat_on_booking(sender, instance, created, **kwargs):
#     """
#     Signal to update the seat's is_booked status when a Booking is created.
#     """
#     if created:
#         seat = instance.seat
#         seat.is_booked = True
#         seat.save()

# @receiver(post_delete, sender=Booking)
# def free_seat_on_booking_delete(sender, instance, **kwargs):
#     """
#     Signal to free up a seat when a Booking is deleted.
#     """
#     seat = instance.seat
#     seat.is_booked = False
#     seat.save()

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Booking, Seat

@receiver(post_save, sender=Booking)
def update_seat_availability(sender, instance, created, **kwargs):
    print("signal processing")
    if created:
        # Mark the seat as booked
        seat = instance.seat
        seat.is_booked = True
        seat.save()
