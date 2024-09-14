from django.core.mail import send_mail
from django.conf import settings

def send_article_sibmission_mail(to_email,name,article_title,datetime):
    subject="Confirmation on successfull article submission"
    message = f"Dear {name} Hi this is Admin from ISJAMR . This is to confirm that an article {article_title.upper()} has been successfull submited on {datetime} . Thank you for submitting your article on ISJAMR."
    from_mail = settings.DEFAULT_FROM_EMAIL
    send_mail(subject,message,from_mail,[to_email])
    print(f"Email send successfully to {name}")