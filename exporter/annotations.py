from moviepy.editor import *
import os

marker_image = ImageClip(os.path.join(os.path.dirname(__file__), "./AS_annotation_small.png"))

ANNOTATION_INITIAL_PAUSE_TIME = 1.0


def get_annotations_added_duration(annotations):
    if (len(annotations)) == 0:
        return ANNOTATION_INITIAL_PAUSE_TIME

    duration = 0;
    for annotation in annotations:
        duration += get_annotation_duration(annotation)
    return duration


def get_annotation_duration(annotation):
    return ANNOTATION_INITIAL_PAUSE_TIME + len(annotation["text"]) * 0.4


def sort_annotations_by_time(annotations):
    return sorted(annotations, key=lambda k: k["time"])


def get_marker_absolute_pos(marker_position, clip):
    marker_x = (marker_position["x"] * clip.w) - marker_image.w / 2
    marker_y = (marker_position["y"] * clip.h) - marker_image.h / 2
    return marker_x, marker_y


def get_subtitle(annotation, sub_duration):
    if len(annotation["text"]) == 0:
        return None

    txt_clip = TextClip(annotation["text"], color="white", fontsize=70, font='Sans Serif')
    txt_clip = txt_clip.set_position(("center", "bottom"))
    txt_clip = txt_clip.set_start(float(annotation["time"]) / 1000.0)
    txt_clip = txt_clip.set_duration(sub_duration)

    return txt_clip


def get_marker(annotation, marker_duration, video_clip):
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

