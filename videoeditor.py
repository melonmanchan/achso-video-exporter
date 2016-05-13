from moviepy.editor import *


def bake_annotations(video_file, end_point,  annotations):
    clip = VideoFileClip(video_file)
    composite_clips = [clip]
    #for annotation in annotations:
    #    txt_clip = TextClip(annotation["text"], color="white", fontsize=70)
    #    txt_clip = txt_clip.set_position(("center", "bottom"))
    #    txt_clip = txt_clip.set_duration(0.5)
    #    txt_clip = txt_clip.set_start(float(annotation["time"]) / 1000.0)
    #    composite_clips.append(txt_clip)

    #final_video = CompositeVideoClip(composite_clips)
    final_video = generate_pauses(clip, annotations)
    final_video.write_videofile("video-out/" + end_point)


def generate_pauses(video_clip, annotations):
    """Takes in a regular video clip, and bakes in annotation pauses"""
    pause_time = 0.5
    clip_duration = video_clip.duration + (len(annotations) * pause_time)
    last_annotation_time = 0
    video_pause_frame_count = int(video_clip.fps * pause_time)
    video_clips = []
    for annotation in annotations:

        annotation_frames = []
        current_annotation_time = annotation["time"] / 1000.0
        video_clips.append(video_clip.subclip(t_start=last_annotation_time, t_end=last_annotation_time + pause_time))
        pause_frame = video_clip.to_ImageClip(current_annotation_time)
        pause_frame.set_duration(pause_time)

        #for _ in range(video_pause_frame_count):
            #annotation_frames.append(pause_frame)

        # video_clips.append(ImageSequenceClip(sequence=[pause_frame], durations=[pause_time]))
        video_clips.append(pause_frame)

        last_annotation_time = current_annotation_time

    return concatenate_videoclips(video_clips)
