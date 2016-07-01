import sendgrid
import config as config
from sendgrid.helpers.mail import  Mail, Content

sg = sendgrid.SendGridAPIClient(apikey=config.SENDGRID_API_KEY)
from_mail = sendgrid.Email(config.SENDGRID_FROM_MAIL)


def render_download_link(link):
    return "<a href='{0}'>{1}</a>".format(link, link)


def render_list_elements(elements):
    output = ""
    for el in elements:
        output += "<li>{0}</li>".format(el)
    return output


def render_list(data):
    return "<ul> </ul>".format(render_list_elements(data))


def render_mail_content(data):
    content = """"<html>
                         <h1>Your videos are ready</h1>
                         <p>Hello! Your download link is {0}</>
                         <h2>The download contains the following videos:</h2>
                         {1}
                  </html>""".format(render_download_link(data["url"]), render_list_elements(data["succeeded"]))

    return Content("text/html", content)


def send_download_link(to, export_results):
    to_mail = sendgrid.Email(to)
    content = render_mail_content(export_results)
    message = Mail(from_email=from_mail, subject='Your AchSo! video export is ready',
                   to_email=to_mail, content=content)
    resp = sg.client.mail.send.post(request_body=message.get())

    return resp


