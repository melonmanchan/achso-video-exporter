from moviepy.editor import *

marker_image = ImageClip("AS_annotation.png")

def get_annotations_added_duration(annotations):
    duration = 0
    for annotation in annotations:
        duration += get_annotation_duration(annotation)
    return duration


def get_annotation_duration(annotation):
    return (len(annotation["text"]) * 0.4)


def sort_annotations_by_time(annotations):
    return sorted(annotations, key=lambda k: k["time"])


def get_marker_absolute_pos(marker_position, clip):
    marker_x = marker_position["x"] * clip.w
    marker_y = marker_position["y"] * clip.h
    return marker_x, marker_y


def get_subtitle(annotation, sub_duration):
    txt_clip = TextClip(annotation["text"], color="white", fontsize=70)
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

