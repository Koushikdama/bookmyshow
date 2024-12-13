from django.db import models
from django.contrib.auth.models import User 
from decimal import Decimal
from django.utils.timezone import now


class Movie(models.Model):
    name= models.CharField(max_length=255)
    image= models.ImageField(upload_to="movies/")
    rating = models.DecimalField(max_digits=3,decimal_places=1)
    cast= models.TextField()
    description= models.TextField(blank=True,null=True) # optional

    def __str__(self):
        return self.name

class Theater(models.Model):
    name = models.CharField(max_length=255)
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name='theaters')
    time= models.DateTimeField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2,default=100.00)
    
     ########################################
    def total_seats(self):
        """Calculate total seats in the theater."""
        return self.seats.count()

    def available_seats(self):
        """Calculate available seats in the theater."""
        return self.seats.filter(is_booked=False).count()

    def dynamic_price(self):
        """Calculate dynamic price based on demand and time to the show."""
        total = self.total_seats()
        available = self.available_seats()

        if total == 0:  # Avoid division by zero
            return self.base_price

       # Example factors
        demand_factor = Decimal(1) - Decimal(available) / Decimal(total)  # Convert to Decimal
        time_factor = max(0, (self.time - now()).total_seconds() / (24 * 3600))  # Time to show in days
        
        # Convert time_factor to Decimal
        time_factor = Decimal(time_factor)

        # Adjust the base price dynamically (convert factors to Decimal)
        price_multiplier = Decimal(1) + demand_factor * Decimal(0.5) + (Decimal(1) - time_factor) * Decimal(0.3)

        # Calculate dynamic price
        return round(self.base_price * price_multiplier, 2)

    def __str__(self):
        return f'{self.name} - {self.movie.name} at {self.time}'

class Seat(models.Model):
    theater = models.ForeignKey(Theater,on_delete=models.CASCADE,related_name='seats')
    seat_number = models.CharField(max_length=10)
    is_booked=models.BooleanField(default=False)

    def __str__(self):
        return f'{self.seat_number} in {self.theater.name}'

class Booking(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    seat=models.OneToOneField(Seat,on_delete=models.CASCADE)
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE)
    theater=models.ForeignKey(Theater,on_delete=models.CASCADE)
    booked_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'Booking by{self.user.username} for {self.seat.seat_number} at {self.theater.name}'