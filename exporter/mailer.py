import sendgrid
import config as config
from sendgrid.helpers.mail import  Mail, Content

sg = sendgrid.SendGridAPIClient(apikey=config.SENDGRID_API_KEY)
from_mail = sendgrid.Email(config.SENDGRID_FROM_MAIL)

def send_download_link(to, link):
    to_mail = sendgrid.Email(to)
    content = Content("text/html", "<html> <h1>Your videos are ready</h1> Hello! Your download link is <a href='{0}'>{1}</a> </html>".format(link, link))
    message = Mail(from_email=from_mail, subject='Your AchSo! video export is ready',
                   to_email=to_mail, content=content)
    resp = sg.client.mail.send.post(request_body=message.get())

    return resp


