from moviepy.editor import *


def bake_annotations(video_file, end_point,  annotations):
    clip = VideoFileClip(video_file)
    composite_clips = [clip]
    for annotation in annotations:
        txt_clip = TextClip(annotation["text"], color="white", fontsize=70)
        txt_clip = txt_clip.set_position(("center", "bottom"))
        txt_clip = txt_clip.set_duration(0.5)
        txt_clip = txt_clip.set_start(float(annotation["time"]) / 1000.0)
        composite_clips.append(txt_clip)

    final_video = CompositeVideoClip(composite_clips)
    final_video.write_videofile("video-out/" + end_point)
