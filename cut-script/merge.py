from moviepy.editor import VideoFileClip, concatenate_videoclips
import os

def merge_videos(video_paths, output_path):
    clips = [VideoFileClip(video_path) for video_path in video_paths]
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_path, audio=True)  # Assumindo que queremos manter o áudio



video_segments = ['./cut/parte_1.mp4', './cut/parte_2.mp4', './cut/parte_3.mp4', './cut/parte_4.mp4', './cut/parte_5.mp4', './cut/parte_6.mp4', './cut/parte_7.mp4', './cut/parte_8.mp4']
output_path = './videos/Resident_Evil_2_reconstructed.mp4'