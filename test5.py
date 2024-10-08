import sys
import subprocess

try:
    import ffmpeg
except ImportError:
    print("Error: ffmpeg-python module not found.")
    print("Please install it using: pip install ffmpeg-python")
    print("If you've just installed it, you might need to restart your Python environment.")
    sys.exit(1)

def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False

def insert_clip_with_transitions(main_video_path, clip_path, timestamp, loop_duration, intro_effect, outro_effect, output_path):
    if not check_ffmpeg():
        print("Error: FFmpeg is not installed or not in your system PATH.")
        print("Please install FFmpeg and make sure it's accessible from the command line.")
        return

    # Get video information
    try:
        probe = ffmpeg.probe(main_video_path)
    except ffmpeg.Error as e:
        print(f"Error reading video file: {e.stderr.decode()}")
        return

    video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
    width = int(video_info['width'])
    height = int(video_info['height'])
    
    # Prepare the main video streams
    main_video = ffmpeg.input(main_video_path)
    main_audio = main_video.audio
    
    # Prepare the clip to insert
    clip = ffmpeg.input(clip_path)
    
    # Loop the clip for the specified duration
    looped_clip = clip.filter('loop', loop='-1', size=str(int(loop_duration * 30)))  # Assuming 30 fps
    
    # Apply intro transition effect
    if intro_effect == 'fade':
        looped_clip = looped_clip.filter('fade', type='in', duration=1)
    elif intro_effect == 'slide':
        looped_clip = looped_clip.filter('slide', direction='r', duration=1)
    
    # Apply outro transition effect
    if outro_effect == 'fade':
        looped_clip = looped_clip.filter('fade', type='out', duration=1)
    elif outro_effect == 'slide':
        looped_clip = looped_clip.filter('slide', direction='l', duration=1)
    
    # Trim the main video
    part1 = main_video.trim(end=timestamp)
    part2 = main_video.trim(start=timestamp)
    
    # Overlay the looped clip onto the main video
    overlay = ffmpeg.overlay(part2, looped_clip, enable=f'between(t,0,{loop_duration})')
    
    # Concatenate all parts
    final_video = ffmpeg.concat(part1, overlay)
    
    # Add audio
    final = ffmpeg.output(final_video, main_audio, output_path, vcodec='libx264', acodec='aac')
    
    # Run FFmpeg command
    try:
        ffmpeg.run(final, overwrite_output=True)
        print(f"Video edited and saved as {output_path}")
    except ffmpeg.Error as e:
        print('FFmpeg error:', e.stderr.decode())

if __name__ == "__main__":
    print("Video Editor using ffmpeg-python")
    print("================================")
    print("Make sure you have FFmpeg installed and accessible from the command line.")
    print("If you encounter any issues, please check the FFmpeg installation.")
    print()

   

    # Get user input
    main_video_path = "C:/Rishika_PC/Projects/Video Editor/SampleIP.mp4"
    clip_path = "C:/Rishika_PC/Projects/Video Editor/sample_effect.mp4"
    timestamp = 10.0
    loop_duration = 5.0
    intro_effect = 'slide'
    outro_effect = 'fade'
    output_path = "output_video.mp4"
    # Run the function
    insert_clip_with_transitions(main_video_path, clip_path, timestamp, loop_duration, intro_effect, outro_effect, output_path)