import uuid
from django.conf import settings
from django.core.mail import send_mail

def sendmail(email, sendername, body, seat_details):
    # Debug prints to verify inputs
    print(email)
    print(sendername)
    print(body)
    print(seat_details)
    
    # Create the email message
    email_message = (
        f"Thank you for booking seats for the show '{body.movie.name}'.\n"
        f"Show Details:\n"
        f"Show Name: {body.movie.name}\n"
        f"THEATER NAME: {seat_details.theater}\n\n"
        f"Seats: {seat_details.seat_number}\n\n"
        
        f"Enjoy the show!\n\n"
        f"Best regards,\nThe Theater Team"
    )
    
    # Create the subject
    subject = f"Dear {sendername}"
    
    # Sender email address
    email_from = settings.EMAIL_HOST_USER
    
    # Ensure recipient_list is a list
    recipient_list = ["koushikdama5@gmail.com"]  # Correctly wrapped in a list
    recipient_list = [email]
    
    # Send the email
    send_mail(subject, email_message, email_from, recipient_list)
