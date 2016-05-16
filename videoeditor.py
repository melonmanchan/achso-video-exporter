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
    final_video.write_videofile("video-out/" + end_point, audio=False)


def generate_pauses(video_clip, annotations):
    """Takes in a regular video clip, and bakes in annotation pauses"""
    pause_time = 0.4
    last_pause_time = 0
    annotation_amount = len(annotations)

    clip_duration = video_clip.duration + (annotation_amount * pause_time)
    print("total video duration: " + str(clip_duration))
    video_clips = []

    for index, annotation in enumerate(annotations):
        current_annotation_time = annotation["time"] / 1000.0

        pause_frame = video_clip.to_ImageClip(current_annotation_time)
        pause_frame = pause_frame.set_start(current_annotation_time)
        pause_frame = pause_frame.set_end(current_annotation_time + pause_time)

        video_part = video_clip.subclip(last_pause_time, current_annotation_time)
        video_part = video_part.set_start(last_pause_time)
        video_part = video_part.set_end(current_annotation_time)

        last_pause_time = current_annotation_time + pause_time

        print("part clip start: " + str(video_part.start))
        print("part clip end " + str(video_part.end))
        print("part clip duration " + str(video_part.duration))

        print("annotation clip start: " + str(pause_frame.start))
        print("annotation clip end " + str(pause_frame.end))
        print("annotation clip duration " + str(pause_frame.duration))

        video_clips.append(video_part)
        video_clips.append(pause_frame)

        if index == (annotation_amount - 1):
            last_part = video_clip.subclip(last_pause_time, video_clip.duration)
            last_part = last_part.set_start(last_pause_time)
            last_part = last_part.set_end(clip_duration)
            print("appending end")
            print("end start: " + str(last_part.start))
            print("end end: " + str(last_part.end))
            print("end duration: " + str(last_part.duration))
            video_clips.append(last_part)

    return CompositeVideoClip(video_clips).set_duration(clip_duration)
