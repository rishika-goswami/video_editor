import cv2
from scenedetect import detect, ContentDetector
from moviepy.editor import VideoFileClip, concatenate_videoclips

def detect_scenes(video_path):
    scene_list = detect(video_path, ContentDetector())
    return scene_list

def get_video_duration(video_path):
    clip = VideoFileClip(video_path)
    duration = clip.duration
    clip.close()
    return duration

def get_seconds(time_value):
    return time_value.get_seconds() if hasattr(time_value, 'get_seconds') else time_value

def insert_clip(main_video_path, clip_path, timestamp, output_path):
    scenes = detect_scenes(main_video_path)
    print(f"Detected {len(scenes)} scenes.")

    if not scenes:
        print("No scenes detected. Using entire video as one scene.")
        duration = get_video_duration(main_video_path)
        scenes = [(0, duration)]

    # Find the scene that contains the timestamp
    target_scene = None
    for i, scene in enumerate(scenes):
        start, end = get_seconds(scene[0]), get_seconds(scene[1])
        if start <= timestamp < end:
            target_scene = (i, (start, end))
            break

    if target_scene is None:
        print(f"No scene found at timestamp {timestamp}. Using nearest scene.")
        nearest_scene = min(enumerate(scenes), key=lambda x: min(abs(timestamp - get_seconds(x[1][0])), 
                                                                 abs(timestamp - get_seconds(x[1][1]))))
        target_scene = nearest_scene

    scene_index, (start, end) = target_scene
    print(f"Inserting clip at scene {scene_index}, between {start:.2f}s and {end:.2f}s")

    # Load videos with audio
    main_video = VideoFileClip(main_video_path)
    clip_to_insert = VideoFileClip(clip_path)

    # Split the main video
    part1 = main_video.subclip(0, timestamp)
    part2 = main_video.subclip(timestamp)

    # Concatenate videos
    final_video = concatenate_videoclips([part1, clip_to_insert, part2])

    # Write the result
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

    # Close all clips
    main_video.close()
    clip_to_insert.close()
    final_video.close()

    print(f"Video edited and saved as {output_path}")

# Example usage
insert_clip("C:/Rishika_PC/Projects/Video Editor/SampleIP.mp4", 
            "C:/Rishika_PC/Projects/Video Editor/sample_effect.mp4", 
            10, 
            "output_video.mp4")