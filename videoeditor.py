from moviepy.editor import *
from annotations import get_annotation_duration


def bake_annotations(video_file, end_point, annotations):
    clip = VideoFileClip(video_file)
    paused_video = generate_pauses(clip, annotations)
    subtitled_video = generate_subtitles(paused_video, annotations)
    subtitled_video.write_videofile("video-out/" + end_point)


def generate_subtitles(video_clip, annotations):
    composite_clips = [video_clip]

    for annotation in annotations:
        txt_clip = TextClip(annotation["text"], color="white", fontsize=70)
        txt_clip = txt_clip.set_position(("center", "bottom"))
        txt_clip = txt_clip.set_start(float(annotation["time"]) / 1000.0)
        txt_clip = txt_clip.set_duration(get_annotation_duration(annotation))
        composite_clips.append(txt_clip)

    return CompositeVideoClip(composite_clips).set_duration(video_clip.duration)


def generate_pauses(video_clip, annotations):
    """Takes in a regular video clip, and bakes in annotation pauses"""
    for annotation in reversed(annotations):
        pause_time = get_annotation_duration(annotation)
        current_annotation_time = annotation["time"] / 1000.0
        video_clip = video_clip.fx(vfx.freeze, t=current_annotation_time, freeze_duration=pause_time)

    return video_clip
