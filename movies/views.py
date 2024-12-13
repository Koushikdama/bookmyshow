from django.shortcuts import render, redirect ,get_object_or_404
from .models import Movie,Theater,Seat,Booking
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from users.sendmail import sendmail
from django.utils.timezone import now
from django.core.mail import send_mail
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib import messages


def movie_list(request):
    search_query=request.GET.get('search')
    if search_query:
        movies=Movie.objects.filter(name__icontains=search_query)
    else:
        movies=Movie.objects.all()
    return render(request,'movies/movie_list.html',{'movies':movies})

# def theater_list(request,movie_id):
#     movie = get_object_or_404(Movie,id=movie_id)
#     theater=Theater.objects.filter(movie=movie)
#     return render(request,'movies/theater_list.html',{'movie':movie,'theaters':theater})
def theater_list(request,movie_id):
    movie = get_object_or_404(Movie,id=movie_id)
    theaters=Theater.objects.filter(movie=movie)
   
  
    print("theaters",theaters)
    for theater in theaters:
        print("teater",theater)
        print("theater.dynamic_price()  ",theater.dynamic_price())
        theater.dynamic_price_display = theater.dynamic_price()  
        print("finally",theater)
    return render(request,'movies/theater_list.html',{'movie':movie,'theaters':theaters})


@login_required(login_url='/login/')
def book_seats(request,theater_id):
    theaters=get_object_or_404(Theater,id=theater_id)
    print("theaters",theaters)
    seats=Seat.objects.filter(theater=theaters)
    print("seats",seats)
    for i in seats:
        print(i.is_booked)
        print(i.seat_number )
        print(i.id)
    if request.method=='POST':
        selected_Seats= request.POST.getlist('seats')
        print("selected_Seatsselected_Seats",selected_Seats)
        error_seats=[]
        print("selected_Seats",selected_Seats)
        if not selected_Seats:
            print("if 1")
            messages.info(request, 'No seat selected')
            return render(request,"movies/seat_selection.html",{'theater':theaters,"seats":seats,'error':"No seat selected"})
        print()
        for seat_id in selected_Seats:
            print("seat_id",seat_id)
            print("seat_id",type(seat_id))
            seat=get_object_or_404(Seat,id=int(seat_id),theater=theaters)
            print("seat",seat,"huw",seat.is_booked)
            if seat.is_booked:
                print(" seat.is_booked")
                error_seats.append(seat.seat_number)
                continue
            try:
                print("try")
                Booking.objects.create(
                    user=request.user,
                    seat=seat,
                    movie=theaters.movie,
                    theater=theaters
                )
                print("seat.is_booked=True")
                # seat.is_booked=True
                # seat.save()
            except IntegrityError as e:
                print("error_seats",error_seats)
                print(f"Error occurred: {e}")
                error_seats.append(seat.seat_number)
        if error_seats:
            print("if 2")
            # error_message=f"The following seats are already booked:{',',join(error_seats)}"
            messages.error(request, 'The following seats are already booked')
            error_message=f"The following seats are already booked:"
            return render(request,'movies/seat_selection.html',{'theater':theaters,"seats":seats,'error':"No seat selected..."})
        
        
      # Prepare the email message
      
        sendmail(request.user.email,request.user.username,theaters,seat)
        return redirect('profile')
    return render(request,'movies/seat_selection.html',{'theaters':theaters,"seats":seats})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    # Mark the seat as available again
    seat = booking.seat
    seat.is_booked = False
    seat.save()

    # Delete the booking record
    booking.delete()

    # Send a message to the WebSocket to notify of the seat availability change
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"seat_availability_theater_{booking.theater.id}", {
            'type': 'send_seat_availability',  # trigger the send_seat_availability method in consumer
        })

    return redirect('profile')

