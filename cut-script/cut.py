from moviepy.editor import VideoFileClip
from moviepy.video import fx
from moviepy.video.fx.all import blackwhite
import os
import threading
import time

def format_time(seconds):
    return time.strftime("%H:%M:%S", time.gmtime(seconds))

def split_video(video_path, output_dir, num_parts=8):
    clip = VideoFileClip(video_path)
    duration = clip.duration
    part_duration = duration / num_parts

    output_files = []  # Lista para armazenar os caminhos dos arquivos de saída

    for i in range(num_parts):
        start_time = i * part_duration
        end_time = (i + 1) * part_duration
        subclip = clip.subclip(start_time, end_time)
        output_file = os.path.join(output_dir, f"parte_{i+1}.mp4")  # Define o caminho do arquivo de saída
        subclip.write_videofile(output_file, audio=False)  # Salva cada parte no diretório especificado
        output_files.append(output_file)  # Adiciona o caminho do arquivo à lista

    return output_files  # Retorna a lista de caminhos dos arquivos


# Exemplo de uso
video_path = "./videos/Resident_Evil_2.mp4" 
output_dir = "./cut"  
output_files = split_video(video_path, output_dir)

print(output_files)  # Imprime a lista de caminhos dos arquivos
