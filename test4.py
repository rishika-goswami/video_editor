import cv2
import numpy as np

def apply_fade_transition(clip, fade_type, duration, fps):
    """
    Apply fade-in or fade-out effect to the clip.
    """
    num_frames = int(fps * duration)
    if fade_type == 'fadein':
        for i in range(num_frames):
            alpha = i / num_frames
            clip[i] = cv2.convertScaleAbs(clip[i], alpha=alpha)
    elif fade_type == 'fadeout':
        for i in range(num_frames):
            alpha = (num_frames - i) / num_frames
            clip[-i-1] = cv2.convertScaleAbs(clip[-i-1], alpha=alpha)
    return clip

def insert_clip_with_transitions(main_video_path, clip_path, timestamp, intro_transition, outro_transition, transition_duration):
    # Load the main video and the small clip
    main_video = cv2.VideoCapture(main_video_path)
    small_clip = cv2.VideoCapture(clip_path)

    # Ensure that the video files are opened correctly
    if not main_video.isOpened():
        raise ValueError(f"Error opening main video: {main_video_path}")
    if not small_clip.isOpened():
        raise ValueError(f"Error opening small video clip: {clip_path}")

    # Get properties of the main video
    fps = main_video.get(cv2.CAP_PROP_FPS)
    frame_width = int(main_video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(main_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    
    # Create output video writer
    output_path = "output_video.mp4"
    output = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    # Read frames from the main video until the timestamp
    timestamp_frame = int(fps * timestamp)
    for frame_idx in range(timestamp_frame):
        ret, frame = main_video.read()
        if not ret:
            break
        output.write(frame)

    # Apply intro transition (fade-in)
    small_clip_frames = []
    while True:
        ret, frame = small_clip.read()
        if not ret:
            break
        small_clip_frames.append(frame)

    # Check if the small clip contains any frames
    if len(small_clip_frames) == 0:
        raise ValueError(f"Error: Small clip '{clip_path}' contains no frames or could not be read.")

    # Resize the small clip if necessary
    if (frame_width, frame_height) != (small_clip_frames[0].shape[1], small_clip_frames[0].shape[0]):
        small_clip_frames = [cv2.resize(frame, (frame_width, frame_height)) for frame in small_clip_frames]

    # Apply transitions to the small clip
    if intro_transition:
        small_clip_frames = apply_fade_transition(small_clip_frames, intro_transition, transition_duration, fps)
    if outro_transition:
        small_clip_frames = apply_fade_transition(small_clip_frames, outro_transition, transition_duration, fps)

    # Write the modified small clip to the output video
    for frame in small_clip_frames:
        output.write(frame)

    # Continue writing the remaining main video after the timestamp
    while True:
        ret, frame = main_video.read()
        if not ret:
            break
        output.write(frame)

    # Release everything
    main_video.release()
    small_clip.release()
    output.release()

    return output_path

def main():
    # Inputs
    main_video_path = "C:/Rishika_PC/Projects/Video Editor/SampleIP.mp4"
    clip_path = "C:/Rishika_PC/Projects/Video Editor/sample_effect.mp4"
    timestamp = 5.0
    intro_transition = 'fadein'
    outro_transition = 'fadeout'
    transition_duration = 5.0
    
    # Process the video and save the output
    try:
        output_path = insert_clip_with_transitions(main_video_path, clip_path, timestamp, intro_transition, outro_transition, transition_duration)
        print(f"Video saved as {output_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

