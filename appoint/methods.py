"""
Appoint notification methods.
"""
################################################################

from django.core.mail import EmailMessage

# from django.contrib import messages

################################################################


def email(notification, text):
    """
    Send a notification by email.
    """
    subject, body = text.split("\n", 1)
    # clean subject
    subject = " ".join(subject.splitlines())
    # also, trim whitespace:
    subject = subject.replace("\t", " ")
    while "  " in subject:
        subject = subject.replace("  ", " ")
    body = body.lstrip("\n")

    email = EmailMessage(
        subject=subject, body=body, to=[notification.notificant.email.address]
    )
    return bool(email.send())


################################################################


# def messages(notification, text):
#     """
#     Send a notification using django.contrib.messages
#     Can't do this without a request object... :-(
#     """
#     return False
#

################################################################
