import os
import threading
import cv2
import time


def format_time(seconds):
    return time.strftime("%H:%M:%S", time.gmtime(seconds))

# Cria um semáforo com o número máximo de threads
num_threads = 8  # Altere este valor para o número de threads que você deseja usar
semaphore = threading.Semaphore(num_threads)

def convert_to_bw(video_path, output_path):
    # Adquire o semáforo
    semaphore.acquire()

    # Carrega o vídeo
    cap = cv2.VideoCapture(video_path)

    # Obtém as informações do vídeo
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Cria o objeto de gravação de vídeo
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height), isColor=False)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Converte a imagem para preto e branco
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Grava a imagem no arquivo de saída
        out.write(gray)

    # Libera os recursos
    cap.release()
    out.release()
    
    # Libera o semáforo
    semaphore.release()

def process_videos(video_paths, output_dir):
    inicio = time.time()    
    threads = []
    for i, video_path in enumerate(video_paths):
        output_path = os.path.join(output_dir, f"bw_parte_{i+1}.mp4")
        thread = threading.Thread(target=convert_to_bw, args=(video_path, output_path))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
    fim = time.time()
    
    print("Tempo de processamento: ", format_time(fim - inicio))
    
# Exemplo de uso
video_paths = ["./cut/parte_1.mp4", "./cut/parte_2.mp4", "./cut/parte_3.mp4", "./cut/parte_4.mp4", "./cut/parte_5.mp4", "./cut/parte_6.mp4", "./cut/parte_7.mp4", "./cut/parte_8.mp4"]
output_dir = "./out"
process_videos(video_paths, output_dir)