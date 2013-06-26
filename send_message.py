'''
Created on Jun 23, 2013

@author: Cameron Wyatt
'''
"""
Sending text messages using an email
AT&T: number@txt.att.net
Sprint: number@messaging.sprintpcs.com
T-Mobile: number@tmomail.net
Verizon: number@vtext.com
"""
"""
TODO:
    Come up with better subject/message text
    Add the ability to specify which carrier a phone number belongs to
        then automatically append the correct ending (e.g. @vtext.com)
        Then the user does not need to remember the endings
"""

import smtplib
import argparse
import os
from datetime import datetime
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from email.MIMEMultipart import MIMEMultipart


def craft_email(from_address, to, location=None):
    """Create an email message from <from_address> to <to>

    Args:
        from_address: the email address that the email will be from
        to: the list of addresses to send the email to
        location: if specified, the location of the image to attach
    """

    MSG_SUBJECT = "ALERT! {}".format(datetime.now())
    msg = MIMEMultipart()
    msg['Subject'] = MSG_SUBJECT
    msg['From'] = from_address
    msg['To'] = ", ".join(to)

    MSG_BODY = MSG_SUBJECT
    msg_text = MIMEText(MSG_BODY)
    msg.attach(msg_text)

    if location and os.path.isfile(location):
        try:
            with open(location, 'rb') as image:
                msg_image = MIMEImage(image.read())
                msg.attach(msg_image)
        except Exception:
            print "Unable to open file {}".format(location)
    else:
        print "Unable to find file {}".format(location)

    return msg


def main():
    """Drive the program

    Parse the command line arguments
    Login to gmail using the account <from_address> using <password>
    If -e, send email to addresses listed
    If -f, send <file_name> in email to <to_email> addresses
    If -t, send text message to numbers listed
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("from_address", help="where the email/txt message\
        will come from")
    parser.add_argument("password", help="password for <from> account")
    parser.add_argument("-f", "--file_name", help="the file name of the\
        image to email")
    parser.add_argument("-e", "--to_email", help="email(s) to send the message\
        to", nargs="+")
    parser.add_argument("-t", "--to_text", help="phone number(s) to send the\
        message to", nargs="+")

    args = parser.parse_args()
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(args.from_address.split("@")[0], args.password)

        if args.to_email:
            email_msg = craft_email(args.from_address, args.to_email, \
                                    args.file_name)
            server.sendmail(args.from_address, args.to_email,
                            email_msg.as_string())
        if args.to_text:
            msg = "ALERT! {}".format(datetime.now())
            server.sendmail(args.from_address, args.to_text, msg)
    except Exception, e:
            print e
    finally:
        server.quit()


if __name__ == '__main__':
    main()
