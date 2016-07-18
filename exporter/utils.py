import os
import requests
import shutil
import tempfile
import dateutil.parser

from email.utils import parseaddr


def download_file(url, end_point):
    """
    Downloads a file using the Requests library to the specified end point.

    Args:
        url (string): The URL of the file to be dowloaded.
        end_point (string): Place to store the final file.

    Returns:
        string: The location of the downloaded file on the local filesystem.
    """
    r = requests.get(url, stream=True)
    with open(end_point, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return end_point


def is_email_valid(email):
    """
    Validates string as a valid email address
    Args:
        email (string): String to validate as email

    Returns:
       bool: Whether or not email was valid

    """
    return '@' in parseaddr(email)[1]

def create_temp_dir():
    """
    Creates a temporary directory.

    Returns:
        string: The location of the temporary directory.
    """
    return tempfile.mkdtemp(suffix='video-exports-')


def delete_file(file_to_delete):
    """
    Deletes a file on the local filesystem.

    Args:
        file_to_delete (string): The location of the file to delete.
    """
    os.remove(file_to_delete)


def delete_dir(dir_to_delete):
    """
    Deletes a directory on the local filesystem.

    Args:
        dir_to_delete (string): The location of the directory to delete.
    """
    shutil.rmtree(dir_to_delete)


def zip_up_dir(folder_to_zip, zip_endpoint):
    """
    Creates a .zip file from a directory.
 
    Args:
        folder_to_zip (string): The location of the directory to create a zip file from.
        zip_endpoint (string): The place to put the finished zip.

    Returns:
        string: The location of the final .zip file.
    """
    shutil.make_archive(zip_endpoint, 'zip', folder_to_zip)
    return zip_endpoint + '.zip'


def is_video_json_valid(json_payload):
    """
    Validates a video dictionary JSON from the client.

    Args:
        json_payload (dict): A JSON payload received from the client.

    Returns:
        bool: Whether or not the video JSON format was valid.
    """
    if not json_payload["videoUri"] or not json_payload["title"]:
        return False
    return True


def parse_iso_date(date):
    """
    Parses and returns a human-readable date from a ISO datetime.

    Args:
        date (string): ISO datetime.

    Returns:
        The date in a more human-readable format.
    """
    if date is None:
        return "an unknown time"

    parsed = dateutil.parser.parse(date)

    return parsed.strftime("%Y.%m.%d %H:%M:%S")


def newlinify_string(string, insert_newline_at):
    """
    Inserts a line break to a string every x characters.

    Args:
        string (string): String to newlinify.
        insert_newline_at (int): Number of characters after which a newline should be inserted at.

    Returns:
        string: The newlinified string.
        int: The amount of newlines added to the input.
    """
    lines = []
    lines_inserted = 0
    for i in xrange(0, len(string), insert_newline_at):
        lines_inserted += 1
        lines.append(string[i:i + insert_newline_at])

    return '\n'.join(lines), lines_inserted

