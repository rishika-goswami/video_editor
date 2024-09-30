from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, vfx

def custom_slide_out(clip, duration=1, side="right"):
    """Create a custom slide-out effect"""
    w, h = clip.size
    
    if side == "right":
        return clip.fx(vfx.slide_in, duration=duration, side="left").fx(vfx.time_mirror)
    elif side == "left":
        return clip.fx(vfx.slide_in, duration=duration, side="right").fx(vfx.time_mirror)
    elif side == "top":
        return clip.fx(vfx.slide_in, duration=duration, side="bottom").fx(vfx.time_mirror)
    elif side == "bottom":
        return clip.fx(vfx.slide_in, duration=duration, side="top").fx(vfx.time_mirror)

def edit_video(main_video_path, clip_path, timestamp, intro_effect, outro_effect):
    # Load the main video and the clip to insert
    main_video = VideoFileClip(main_video_path)
    clip_to_insert = VideoFileClip(clip_path)
    
    # Split the main video at the timestamp
    part1 = main_video.subclip(0, timestamp)
    part2 = main_video.subclip(timestamp)
    
    # Apply intro transition effect
    if intro_effect == "fade":
        clip_to_insert = clip_to_insert.fx(vfx.fadeout, duration=1)
    '''elif intro_effect == "slide":
        clip_to_insert = CompositeVideoClip([clip_to_insert.fx(vfx.slide_in, duration=1, side="right")])'''
    
    # Apply outro transition effect
    if outro_effect == "fade":
        clip_to_insert = clip_to_insert.fx(vfx.fadeout, duration=1)
    '''elif outro_effect == "slide":
        clip_to_insert = CompositeVideoClip([custom_slide_out(clip_to_insert, duration=1, side="right")])'''
    
    # Concatenate all parts
    final_video = concatenate_videoclips([part1, clip_to_insert, part2])
    
    # Write the result to a file
    final_video.write_videofile("output_video.mp4")
    
    # Close all clips to free up system resources
    main_video.close()
    clip_to_insert.close()
    final_video.close()

# Example usage
edit_video("C:/Rishika_PC/Projects/Video Editor/SampleIP.mp4", "C:/Rishika_PC/Projects/Video Editor/sample_effect.mp4", 10, "fade", "fade")