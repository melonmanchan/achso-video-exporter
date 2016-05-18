from moviepy.editor import *
from annotations import get_annotation_duration, get_subtitle, get_marker


marker_image = ImageClip("AS_annotation.png")

def bake_annotations(video_file, end_point, annotations):
    clip = VideoFileClip(video_file)
    annotated_video = generate_annotation_markings(clip, annotations)
    paused_video = generate_pauses(annotated_video, annotations)
    paused_video.write_videofile("video-out/" + end_point)


def generate_annotation_markings(video_clip, annotations):
    composite_clips = [video_clip]
    one_frame_time = 1 / video_clip.fps

    for annotation in annotations:
        txt_clip = get_subtitle(annotation, one_frame_time)
        marker = get_marker(annotation, one_frame_time, video_clip)
        composite_clips.append(txt_clip)
        composite_clips.append(marker)

    return CompositeVideoClip(composite_clips)


def generate_pauses(video_clip, annotations):
    """Takes in a regular video clip, and bakes in annotation pauses"""
    for annotation in reversed(annotations):
        pause_time = get_annotation_duration(annotation)
        current_annotation_time = annotation["time"] / 1000.0
        video_clip = video_clip.fx(vfx.freeze, t=current_annotation_time, freeze_duration=pause_time)

    return video_clip


