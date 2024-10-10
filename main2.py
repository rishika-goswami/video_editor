from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips, concatenate_audioclips
import argparse

def create_looping_clip(input_path, duration):
    """Create a looping clip from video or image that matches the desired duration"""
    if input_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        clip = ImageClip(input_path)
    else:
        clip = VideoFileClip(input_path)
    
    audio = clip.audio
    original_duration = clip.duration if isinstance(clip, VideoFileClip) else float('inf')
    if original_duration < duration:
        # Calculate how many times we need to loop
        loops = int(duration // original_duration) + 1
        looped_clip = clip.loop(n=loops)
        final_clip = looped_clip.subclip(0, duration)
        try:
            looped_audio = audio.loop(n=loops)
            final_audio = looped_audio.subclip(0, duration)
        except:
            final_audio = None
    else:
        final_clip = clip.subclip(0, duration)
        try:
            final_audio = audio.subclip(0, duration)
        except:
            final_audio = None


    return final_clip, final_audio

def insert_clip(main_video_path, insert_path, timestamp, duration, output_path):
    """Insert a video clip or image into the main video at specified timestamp"""
    try:
        # Load the main video
        main_video = VideoFileClip(main_video_path)
        main_audio = main_video.audio
        
        # Create the clip to insert
        insert_clip, insert_audio = create_looping_clip(insert_path, duration)
        
        # Ensure the timestamp is valid
        if timestamp < 0 or timestamp > main_video.duration:
            raise ValueError(f"Timestamp must be between 0 and {main_video.duration}")
        
        # Create the composite video
        composite = concatenate_videoclips([main_video.subclip(0, timestamp),
                                            insert_clip,
                                            main_video.subclip(timestamp)],method="compose")
        try:
            composite_audio = concatenate_audioclips([main_audio.subclip(0, timestamp),
                                                insert_audio,
                                                main_audio.subclip(timestamp)])
        except:
            pass
        # Write the output file
        try:
            composite.set_audio(composite_audio)
        except:
            pass
        composite.write_videofile(output_path, codec='libx264',audio_codec='aac')

        
        # Close all clips
        main_video.close()
        insert_clip.close()
        composite.close()
        
        print(f"Video successfully created: {output_path}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Insert a video clip or image into another video.')
    parser.add_argument('main_video', help='Path to the main video file')
    parser.add_argument('insert_media', help='Path to the video clip or image to insert')
    parser.add_argument('timestamp', type=float, help='Timestamp (in seconds) to insert the media')
    parser.add_argument('duration', type=float, help='Duration (in seconds) for the inserted media')
    parser.add_argument('output', help='Path for the output video file')
    
    args = parser.parse_args()
    
    insert_clip(args.main_video, args.insert_media, args.timestamp, args.duration, args.output)

if __name__ == "__main__":
    main()