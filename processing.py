import threading
import cv2
import time
import queue

def process_quadro(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return gray_frame

def process_chunk(chunk, output_queue):
    for frame in chunk:
        processed_frame = process_quadro(frame)
        output_queue.put(processed_frame)

def process_video_threaded(input_video_path, output_video_path, num_threads):
    start_time = time.time()

    # abrir video
    video = cv2.VideoCapture(input_video_path)

    # pega altura e largura do video e fps 
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS)

    # definir codec para o video de saida 
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height), isColor=False)

    # criar uma fila para armazenar os quadros processados
    output_queue = queue.Queue()

    # criar uma lista para armazenar os threads
    threads = []

    # dividir o vídeo em chunks e criar um thread para cada chunk
    chunk = []
    while(video.isOpened()):
        ret, frame = video.read()
        if ret:
            chunk.append(frame)
            if len(chunk) == num_threads:
                t = threading.Thread(target=process_chunk, args=(chunk, output_queue))
                t.start()
                threads.append(t)
                chunk = []
        else:
            break

    # processar o último chunk se ele não estiver vazio
    if chunk:
        t = threading.Thread(target=process_chunk, args=(chunk, output_queue))
        t.start()
        threads.append(t)

    # esperar todos os threads terminarem
    for t in threads:
        t.join()

    # escrever os quadros processados no vídeo de saída
    while not output_queue.empty():
        out.write(output_queue.get())

    # liberar os objetos
    video.release()
    out.release()

    end_time = time.time()
    print("Tempo de processamento: ", end_time - start_time)

# processar o video e a saida sera salva em output.mp4
process_video_threaded('./videos/Resident_Evil_2.mp4', './out/output1.mp4', 6)