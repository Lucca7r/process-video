import cv2
import time
import threading
import queue

def format_time(seconds):
    return time.strftime("%H:%M:%S", time.gmtime(seconds))

def process_quadro(frame):
    # converter o quadro para escala de cinza
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return gray_frame

def process_video(input_video_path, output_video_path):
    inicial = time.time()

    # abrir o vídeo
    video = cv2.VideoCapture(input_video_path)

    # obter informações do vídeo
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS)

    # codec para o arquivo de saída
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height), isColor=False)

    frame_queue = queue.Queue(maxsize=10)
    output_queue = queue.Queue(maxsize=10)

    def read_frames():
        while True:
            ret, frame = video.read() # ret indica se foi lido um quadro com sucesso
            if ret:
                frame_queue.put(frame)
            else:
                break
        # sinaliza que todos os quadros foram lidos
        frame_queue.put(None)  

    def process_frames():
        while True:
            frame = frame_queue.get() # area crítica (bloqueia se a fila estiver vazia)
            if frame is None:
                break
            processed_frame = process_quadro(frame)
            output_queue.put(processed_frame) # colocar o quadro processado na fila
        # sinaiza que o quadro foi processado
        output_queue.put(None)  
        

    # iniciar as threads
    threading.Thread(target=read_frames).start()
    threading.Thread(target=process_frames).start()
    threading.Thread(target=process_frames).start()
    threading.Thread(target=process_frames).start()
    threading.Thread(target=process_frames).start()
    threading.Thread(target=process_frames).start()
    
    # aguardar o término das threads
    while True:
        processed_frame = output_queue.get()
        if processed_frame is None:
            break
        out.write(processed_frame)

    video.release()
    out.release()

    final = time.time()
    print("Tempo de processamento: ", format_time(final - inicial))

process_video('./out/parte_1.mp4', './out/output1.mp4')