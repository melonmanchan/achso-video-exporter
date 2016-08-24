import sendgrid
import config as config
from utils import parse_iso_date

from sendgrid.helpers.mail import  Mail, Content

sg = sendgrid.SendGridAPIClient(apikey=config.SENDGRID_API_KEY)
from_mail = sendgrid.Email(config.SENDGRID_FROM_MAIL)


def render_download_link(link):
    """
    Renders a regular old HTML anchor link element.

    Args:
        link (string): The URL of the link to be rendered.

    Returns:
        string: The HTML anchor element.

    """
    return "<a href='{0}'>{1}</a>".format(link, link)


def render_list_elements(elements):
    """
    Renders a HTML unordered list inner content from annotation export results.

    Args:
        elements (array): Array of dictionaries with a title and date key.

    Returns:
        The HTML string output.

    """
    output = ""
    for el in elements:
        output += "<li>{0} (Last updated at {1})</li>".format(el["title"], parse_iso_date(el["date"]))
    return output


def render_list(data):
    """
    Renders a HTML unordered list from annotation export results.

    Args:
        data (array): Array of dictionaries with a title and date key.

    Returns:
        The HTML string output.
    """
    return "<ul>{0}</ul>".format(render_list_elements(data))


def render_success(data):
    """
    Renders the email section containing info on succesful video exports.

    Args:
        data (array): Array of dictionaries with a title and date key.

    Returns:
        The HTML string output.

    """
    if len(data["succeeded"]) == 0:
        return ""
    else:
        return "<h2>The download contains the following videos: </h2>{0}".format(render_list(data["succeeded"]))


def render_failure(data):
    """
    Renders the email section containing info on failed video exports.

    Args:
        data (array): Array of dictionaries with a title and date key.

    Returns:
        The HTML string output.

    """
    if len(data["failed"]) == 0:
        return ""
    else:
        return "<h2>Unfortunately, exporting the following videos failed: </h2>{0}".format(render_list(data["failed"]))


def render_mail_content(data):
    """
    Renders the export email containing the export download link and such, ready to be sent to the recipient.

    Args:
        data (array): Array of dictionaries with a title and date key.

    Returns:
        Content: A SendGrid Content object containing the mail.

    """
    content = """<html>
                         <h1>Your videos are ready</h1>
                         <p>Hello! Your download link is {0}. This download will expire in 30 days from now</p>
                         {1}
                         {2}
                  </html>""".format(render_download_link(data["url"]), render_success(data), render_failure(data))

    return Content("text/html", content)


def send_download_link(to, export_results):
    """
    Sends an email containing the export download link to a user

    Args:
        to (string): The email of the recipient.
        export_results (array): A dictionary containing two keys, succeeded and failed, which both contain an array of objects
                                with the video title and last updated timestamp.

    Returns:
        (Response): SendGrid response object.

    """
    to_mail = sendgrid.Email(to)
    content = render_mail_content(export_results)
    message = Mail(from_email=from_mail, subject='Your AchSo! video export is finished',
                   to_email=to_mail, content=content)
    resp = sg.client.mail.send.post(request_body=message.get())

    return resp


