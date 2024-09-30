import cv2
from scenedetect import detect, ContentDetector
from scenedetect.video_splitter import split_video_ffmpeg

def detect_scenes(video_path):
    scenes = detect(video_path, ContentDetector())
    return scenes

def insert_clip(main_video_path, clip_path, timestamp, output_path):
    scenes = detect_scenes(main_video_path)
    
    print(f"Detected {len(scenes)} scenes")
    for i, scene in enumerate(scenes):
        print(f"Scene {i}: {scene[0].get_seconds()} - {scene[1].get_seconds()}")
    
    # Find the scene that contains the timestamp
    target_scene = None
    for scene in scenes:
        if scene[0].get_seconds() <= timestamp < scene[1].get_seconds():
            target_scene = scene
            break
    
    if target_scene is None:
        print(f"No scene found at timestamp {timestamp}")
        print("Falling back to splitting at exact timestamp")
        target_scene = (timestamp, timestamp + 0.001)  # Create a tiny scene at the timestamp
    
    # Split the main video
    split_video_ffmpeg(main_video_path, [target_scene], output_file_template="temp_$SCENE_NUMBER.mp4")
    
    # Read the clip to insert
    clip = cv2.VideoCapture(clip_path)
    
    # Read the parts of the main video
    part1 = cv2.VideoCapture("temp_0.mp4")
    part2 = cv2.VideoCapture("temp_1.mp4")
    
    # Get video properties
    fps = part1.get(cv2.CAP_PROP_FPS)
    width = int(part1.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(part1.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    # Write part1
    while True:
        ret, frame = part1.read()
        if not ret:
            break
        out.write(frame)
    
    # Write clip
    while True:
        ret, frame = clip.read()
        if not ret:
            break
        frame = cv2.resize(frame, (width, height))
        out.write(frame)
    
    # Write part2
    while True:
        ret, frame = part2.read()
        if not ret:
            break
        out.write(frame)
    
    # Release everything
    part1.release()
    part2.release()
    clip.release()
    out.release()
    
    print(f"Video edited and saved as {output_path}")

# Example usage
insert_clip("C:/Rishika_PC/Projects/Video Editor/SampleIP.mp4", 
            "C:/Rishika_PC/Projects/Video Editor/sample_effect.mp4", 
            10, 
            "output_video.mp4")