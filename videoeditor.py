from moviepy.editor import *
from annotations import get_annotation_duration, get_annotations_added_duration, get_subtitle, get_marker


def bake_annotations(video_file, end_point, annotations):
    clip = VideoFileClip(video_file)
    annotated_video = generate_annotation_markings(clip, annotations)
    final_video = generate_video_pauses(annotated_video, annotations)
    final_video_audio = generate_pause_audio(clip.audio, annotations)
    final_video.set_audio(final_video_audio)
    final_video.write_videofile("video-out/" + end_point)


def generate_annotation_markings(video_clip, annotations):
    composite_clips = [video_clip]
    one_frame_time = 1 / video_clip.fps

    for annotation in annotations:
        txt_clip = get_subtitle(annotation, one_frame_time)
        marker = get_marker(annotation, one_frame_time, video_clip)
        composite_clips.append(txt_clip)
        composite_clips.append(marker)

    return CompositeVideoClip(composite_clips)


def generate_video_pauses(video_clip, annotations):
    """Takes in a regular video clip, and bakes in annotation pauses"""
    for annotation in reversed(annotations):
        pause_time = get_annotation_duration(annotation)
        current_annotation_time = annotation["time"] / 1000.0
        video_clip = video_clip.fx(vfx.freeze, t=current_annotation_time, freeze_duration=pause_time)

    return video_clip


def generate_pause_audio(original_audio, annotations):
    audio_clip = original_audio
    last_pause_time = 0
    audio_parts = []

    for annotation in annotations:
        pause_time = get_annotation_duration(annotation)
        current_annotation_time = annotation["time"] / 1000.0

        audio_part = audio_clip.subclip(last_pause_time, current_annotation_time)
        audio_part = audio_part.set_start(last_pause_time)
        audio_part = audio_part.set_end(current_annotation_time)
        audio_parts.append(audio_part)

        last_pause_time = current_annotation_time + pause_time

    comp = CompositeAudioClip(audio_parts)

    return comp

