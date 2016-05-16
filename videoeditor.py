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
    video_clips = [ video_clip ]
    for annotation in annotations:
        current_annotation_time = annotation["time"] / 1000.0
        pause_frame = video_clip.to_ImageClip(current_annotation_time)

        print("starting annotation at " + str(current_annotation_time))
        print("ending annotation at " + str(current_annotation_time + pause_time))

        pause_frame = pause_frame.set_start(current_annotation_time)
        pause_frame = pause_frame.set_end(current_annotation_time + pause_time)
        print(pause_frame.start)
        print(pause_frame.end)
        print(pause_frame.duration)

        video_clips.append(pause_frame)

    return CompositeVideoClip(video_clips).set_duration(clip_duration)
