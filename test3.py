import cv2
from scenedetect import detect, ContentDetector
from scenedetect.video_splitter import split_video_ffmpeg
import os

def detect_scenes(video_path):
    scene_list = detect(video_path, ContentDetector())
    return scene_list

def get_video_duration(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps
    cap.release()
    return duration

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
        start, end = scene[0].get_seconds() if hasattr(scene[0], 'get_seconds') else scene[0], scene[1].get_seconds() if hasattr(scene[1], 'get_seconds') else scene[1]
        if start <= timestamp < end:
            target_scene = (i, (start, end))
            break

    if target_scene is None:
        print(f"No scene found at timestamp {timestamp}. Using nearest scene.")
        nearest_scene = min(enumerate(scenes), key=lambda x: min(abs(timestamp - x[1][0].get_seconds() if hasattr(x[1][0], 'get_seconds') else x[1][0]), 
                                                                 abs(timestamp - x[1][1].get_seconds() if hasattr(x[1][1], 'get_seconds') else x[1][1])))
        target_scene = nearest_scene

    scene_index, (start, end) = target_scene
    print(f"Inserting clip at scene {scene_index}, between {start:.2f}s and {end:.2f}s")

    # Read the main video
    main_video = cv2.VideoCapture(main_video_path)
    clip = cv2.VideoCapture(clip_path)

    # Get video properties
    fps = main_video.get(cv2.CAP_PROP_FPS)
    width = int(main_video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(main_video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Write main video up to the timestamp
    frame_count = 0
    while True:
        ret, frame = main_video.read()
        if not ret or frame_count / fps >= timestamp:
            break
        out.write(frame)
        frame_count += 1

    # Write clip
    while True:
        ret, frame = clip.read()
        if not ret:
            break
        frame = cv2.resize(frame, (width, height))
        out.write(frame)

    # Write the rest of the main video
    while True:
        ret, frame = main_video.read()
        if not ret:
            break
        out.write(frame)

    # Release everything
    main_video.release()
    clip.release()
    out.release()

    print(f"Video edited and saved as {output_path}")

# Example usage
insert_clip("C:/Rishika_PC/Projects/Video Editor/SampleIP.mp4", 
            "C:/Rishika_PC/Projects/Video Editor/sample_effect.mp4", 
            10, 
            "output_video.mp4")