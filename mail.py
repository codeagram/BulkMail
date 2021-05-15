#!/usr/bin/env python3
""" A script to send bulk mail to multiple emails
    reading from csv file having name and email columns"""
import csv
import smtplib
import ssl
from getpass import getpass
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def get_credentials():

    """ Get user credentials to login to email account """

    print("This program send emails using SMTP protocol with Gmail")
    sender = input("Your Email: ")
    password = getpass()

    return (sender, password)


def get_message(sender):

    """ Reading customized message in text file
        and convert it to email body"""

    message = MIMEMultipart('alternative')
    message['From'] = sender
    message['Subject'] = input('Subject: ')

    try:
        with open('message.txt', 'r') as f:
            text = f.read()

    except Exception as e:
        print("File containing message not found!")
        print(e)

    part = MIMEText(text, 'plain')
    message.attach(part)

    return message


def add_attachment():

    """ Add attachment to the email """

    filename = input('Attachment Filename: ')

    with open(filename, 'rb') as f:
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(f.read())

    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', f'attachment; filename={filename}')

    return attachment


def send_mail():

    """ Sending emails """

    smtp = 'smtp.gmail.com'
    port = 465
    context = ssl.create_default_context()

    sender, password = get_credentials()
    message = get_message(sender)
    attachment = add_attachment()
    message.attach(attachment)

    with smtplib.SMTP_SSL(smtp, port, context=context) as server:
        try:
            server.login(sender, password)
            print(f"Logged In as {sender}")
            filename = input("Filename containing receivers email: ")
            with open(filename) as f:
                read = csv.reader(f)
                next(read)
                for name, email in read:
                    receiver = email
                    message['To'] = receiver
                    server.sendmail(sender, receiver, message.as_string())
                    print(f"Mail Sent To {name.title()}")

            print("All Mails Sent")

        except Exception as e:
            print("Failed!")
            print(e)


if __name__ == '__main__':
    send_mail()
