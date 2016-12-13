from utils import newlinify_string
from moviepy.editor import *
import os

marker_image = ImageClip(os.path.join(os.path.dirname(__file__), "./AS_annotation_small.png"))

ANNOTATION_INITIAL_PAUSE_TIME = 1.0
"""float: The minimum default pause time for an annotation. """


def get_subtitle_offset(annotation, seen_annotations, clip, font_size):
    """
    Gets the Y offset for a subtitle, which depends on the amount of other subtitles in the same frame, starting from the bottom of the screen.

    Args:
        annotation (dict): A singular annotation object
        seen_annotations (dict): A dictionary with annotation appearance times as the keys, and the number of times they appear
                                as the value.
        video_clip (VideoClip): The video clip where the annotation will be shown.

    Returns:
        int: The location of the subtitle on the Y axis in pixels
    """
    if not annotation["time"] in seen_annotations:
        return (clip.h - font_size) 
    else:
        return (clip.h - font_size * (seen_annotations[annotation["time"]] + 1))


def add_to_subtitle_offset(annotation, seen_annotations, value):
    """
    Adds an annotation to the seen_annotations dictionary for handling subtitles in the same frame.

    Args:
        annotation (dict): A singular annotation object.
        seen_annotations (dict): A dictionary with annotation appearance times as the keys, and the number of times they appear
                                as the value.
        value (int): The value the key in seen_annotations should be incremented by.

    """
    if not annotation["time"] in seen_annotations:
        seen_annotations[annotation["time"]] = value
    else:
        seen_annotations[annotation["time"]] += value


def get_annotations_added_duration(annotations):
    """
    Calculates the total added video length from all the annotations.

    Args:
        annotations (array): An array of annotation dictionaries.

    Returns:
        float: The added video length.
    """
    if (len(annotations)) == 0:
        return ANNOTATION_INITIAL_PAUSE_TIME

    duration = 0
    for annotation in annotations:
        duration += get_annotation_duration(annotation)
    return duration


def get_annotation_duration(annotation):
    """
    Calculates for how long a screen should be paused (Dependant on the length of the annotation text)

    Args:
        annotation (dict): A singular annotation object

    Returns:
        float: The time the annotation pause should last
    """
    return ANNOTATION_INITIAL_PAUSE_TIME + len(annotation["text"]) * 0.2


def sort_annotations_by_time(annotations):
    """
    Sorts an array of annotation dictionaries by the time that they appear in the video.

    Args:
        annotation (array): An array of annotation dictionaries.

    Returns:
        array: The sorted array.
    """
    return sorted(annotations, key=lambda k: k["time"])


def get_marker_absolute_pos(marker_position, clip):
    """
    Gets the position where the annotation marker image should reside at by a relative value.
    Args:
        marker_position (dict): A dictionary containing the annotation X and Y relative values.
        clip (VideoClip): The video clip where the marker will be ultimately shown.
    Returns:
        tuple: A tuple of two floats containing the final absolute marker position.
    """
    marker_x = (marker_position["x"] * clip.w) - marker_image.w / 2
    marker_y = (marker_position["y"] * clip.h) - marker_image.h / 2
    return marker_x, marker_y


def calculate_needed_subtitle_height(annotation, seen_annotations, video_clip):
    """
    Adds newlines as needed to an annotation subtitle so it fits nicely on the video without overlapping anything.

    Args:
        annotation (dict): A single annotation dictionary.
        seen_annotations (dict): A dictionary with annotation appearance times as the keys, and the number of times they appear
                                as the value.
        video_clip (VideoClip): The video clip where the annotation will be shown.

    Returns:
        string: The annotation subtitle with possible added line breaks.
    """
    width = video_clip.w
    text = annotation["text"].encode('utf-8')
    if len(text) > width / 40:
        text, lines_inserted = newlinify_string(text, int(width / 40))
        add_to_subtitle_offset(annotation, seen_annotations, lines_inserted - 1)

    return text


def get_subtitle(annotation, sub_duration, video_clip, seen_annotations):
    """
    Creates a MoviePy TextClip object from an annotation dictionary, adds it to seen annotations.

    Args:
        annotation (dict): A single annotation dictionary.
        sub_duration (float): The amount of time the subtitle should be shown.
        video_clip (VideoClip): The video clip where the annotation will be shown.
        seen_annotations (dict): A dictionary with annotation appearance times as the keys, and the number of times they appear
                                as the value.

    Returns:
        TextClip: A MoviePy TextClip object, ready to be displayed on the video.
    """
    if len(annotation["text"]) == 0:
        return None

    font_size = int((video_clip.h / 15))

    annotation_txt = calculate_needed_subtitle_height(annotation, seen_annotations, video_clip)

    txt_clip = TextClip(annotation_txt, color="white", fontsize=font_size, font='Sans Serif')
    txt_clip = txt_clip.set_position(("center", get_subtitle_offset(annotation, seen_annotations, video_clip, font_size)))
    txt_clip = txt_clip.set_start(float(annotation["time"]) / 1000.0)
    txt_clip = txt_clip.set_duration(sub_duration)

    return txt_clip


def get_marker(annotation, marker_duration, video_clip):
    """
    Creates a MoviePy ImageClip from an annotation dictionary

    Args:
        annotation (dict): A single annotation dictionary.
        marker_duration (float): The amount of time the marker should be shown.
        video_clip (VideoClip): The video clip where the annotation marker will be shown.

    Returns:
        A MoviePy ImageClip object, ready to be displayed on the video.

    """
    position = annotation["position"]
    marker = marker_image.copy()
    marker = marker.set_position(get_marker_absolute_pos(position, video_clip))
    marker = marker.set_start(float(annotation["time"]) / 1000.0)
    marker = marker.set_duration(marker_duration)

    return marker


def is_annotation_json_valid(annotations):
    for annotation in annotations:
        if not all(k in annotation for k in ("time", "position")):
            return False
    return True

