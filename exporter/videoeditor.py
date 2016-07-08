from moviepy.editor import *
from annotations import get_annotation_duration, get_annotations_added_duration, get_subtitle, get_marker
import uuid


def bake_annotations(video_file, end_point, annotations):
    """
    Adds annotation markers and subtitles to a video, then writes it on the filesystem.

    Args:
        video_file (string): The location of the video file on the file system.
        end_point (string): Where to store the final video file.
        annotations (array): An array of annotation dictionaries.
    """
    clip = VideoFileClip(video_file)
    annotated_video = generate_annotation_markings(clip, annotations)
    final_video = generate_video_pauses(annotated_video, annotations)
    audio = clip.audio.set_duration(clip.audio.duration + get_annotations_added_duration(annotations))
    final_video_audio = generate_pause_audio(audio, annotations)
    final_video.set_audio(final_video_audio)
    final_video.write_videofile(end_point, codec='libx264', audio_codec='aac', temp_audiofile='temp-audio-' + str(uuid.uuid4()) + '.m4a')


def update_seen_annotations(annotation, seen_annotations):
    """
    Increments the amount of times an annotation has appeared in the same frame.

    Args:
        annotation (dict): A single annotation dictionary.
        seen_annotations (dict): A dictionary with annotation appearance times as the keys, and the number of times they appear
                                as the value.
    """
    if not annotation["time"] in seen_annotations:
        seen_annotations[annotation["time"]] = 1
    else:
        seen_annotations[annotation["time"]] += 1


def generate_annotation_markings(video_clip, annotations):
    """
    Does the actual creation of subtitles and markers, and adds them to a MoviePy composition.

    Args:
        video_clip (VideoClip): The video to be exported.
        annotations (array): An array of annotation dictionaries.

    Returns:
        CompositeAudioClip: A finished MoviePy object with all the audios, videos and such as separate components
    """
    seen_annotations = {}
    composite_clips = [video_clip]
    one_frame_time = 1 / video_clip.fps

    for annotation in annotations:
        txt_clip = get_subtitle(annotation, one_frame_time, video_clip, seen_annotations)
        marker = get_marker(annotation, one_frame_time, video_clip)
        if txt_clip is not None:
            composite_clips.append(txt_clip)
        composite_clips.append(marker)

        update_seen_annotations(annotation, seen_annotations)

    return CompositeVideoClip(composite_clips)


def generate_video_pauses(video_clip, annotations):
    """
    Adds pauses to a video clip for the annotations.

    Args:
        video_clip (VideoClip): The video to be exported.
        annotations (array): An array of annotation dictionaries.

    Returns:
        VideoClip: The clip with the annotation pauses included.
    """
    for annotation in reversed(annotations):
        pause_time = get_annotation_duration(annotation)
        current_annotation_time = annotation["time"] / 1000.0
        video_clip = video_clip.fx(vfx.freeze, t=current_annotation_time, freeze_duration=pause_time)

    return video_clip


def generate_pause_audio(original_audio, annotations):
    """
    Adds pauses to a audio clip for the annotations.

    Args:
        original_audio (AudioClip): The original audio to be exported.
        annotations (array): An array of annotation dictionaries.

    Returns:
        AudioClip: The clip with the annotation pauses included.
    """
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

