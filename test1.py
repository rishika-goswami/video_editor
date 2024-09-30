from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx

def apply_transition(clip, intro_transition, outro_transition, duration):
    """
    Apply intro and outro transitions to the clip.
    """
    if intro_transition == 'fadein':
        clip = clip.fadein(duration)
    if outro_transition == 'fadeout':
        clip = clip.fadeout(duration)
    return clip

def insert_clip_with_transitions(main_video_path, clip_path, timestamp, intro_transition, outro_transition, transition_duration):
    """
    Insert a clip with transitions into a main video at the specified timestamp.
    """
    # Load the main video and the small clip
    main_video = VideoFileClip(main_video_path)
    clip = VideoFileClip(clip_path)

    # Apply intro and outro transitions to the clip
    clip_with_transitions = apply_transition(clip, intro_transition, outro_transition, transition_duration)

    # Ensure the timestamp does not exceed the main video duration
    if timestamp > main_video.duration:
        raise ValueError("Timestamp exceeds the duration of the main video.")

    # Split the main video at the timestamp
    before_clip = main_video.subclip(0, timestamp)
    after_clip = main_video.subclip(timestamp)

    # Handle mismatch in clip aspect ratios
    if clip_with_transitions.size != main_video.size:
        clip_with_transitions = clip_with_transitions.resize(main_video.size)

    # Concatenate the parts together: before -> clip_with_transitions -> after
    final_video = concatenate_videoclips([before_clip, clip_with_transitions, after_clip])

    return final_video

def main():
    # Inputs
    main_video_path = input("Enter the path to the initial video: ")
    clip_path = input("Enter the path to the small video clip: ")
    timestamp = float(input("Enter the timestamp to insert the clip (in seconds): "))
    intro_transition = input("Enter the intro transition effect (e.g., 'fadein'): ")
    outro_transition = input("Enter the outro transition effect (e.g., 'fadeout'): ")
    transition_duration = float(input("Enter the duration of the transitions (in seconds): "))
    
    # Process the video and save the output
    try:
        final_video = insert_clip_with_transitions(main_video_path, clip_path, timestamp, intro_transition, outro_transition, transition_duration)
        output_path = "output_video.mp4"
        final_video.write_videofile(output_path, codec="libx264")
        print(f"Video saved as {output_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
