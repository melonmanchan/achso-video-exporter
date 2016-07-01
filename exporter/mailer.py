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
    return "<ul>{0}</ul>".format(render_list_elements(data))


def render_success(data):
    if len(data["succeeded"]) == 0:
        return ""
    else:
        return "<h2>The download contains the following videos: </h2>{0}".format(render_list(data["succeeded"]))


def render_failure(data):
    if len(data["failed"]) == 0:
        return ""
    else:
        return "<h2>Unfortunately, exporting the following videos failed: </h2>{0}".format(render_list(data["failed"]))


def render_mail_content(data):
    print(data)
    content = """"<html>
                         <h1>Your videos are ready</h1>
                         <p>Hello! Your download link is {0}</>
                         {1}
                         {2}
                  </html>""".format(render_download_link(data["url"]), render_success(data), render_failure(data))

    return Content("text/html", content)


def send_download_link(to, export_results):
    to_mail = sendgrid.Email(to)
    content = render_mail_content(export_results)
    message = Mail(from_email=from_mail, subject='Your AchSo! video export is finished',
                   to_email=to_mail, content=content)
    resp = sg.client.mail.send.post(request_body=message.get())

    return resp


