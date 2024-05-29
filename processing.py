import cv2
import threading
import queue
import time

# Fila de entrada e saída
input_queue = queue.Queue(maxsize=10)
output_queue = queue.Queue(maxsize=10)


def format_time(seconds):
    return time.strftime("%H:%M:%S", time.gmtime(seconds))

def process_video(input_video_path, output_video_path, filter_type):
    inicial = time.time()
    video = cv2.VideoCapture(input_video_path)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS)
    out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    
    def read_frames():
        while True:
            ret, frame = video.read()
            if not ret:
                break
            input_queue.put(frame)
        input_queue.put(None)

    def process_frames():
        while True:
            frame = input_queue.get()
            if frame is None:
                break

            if filter_type == 'gray':
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                processed_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)
            elif filter_type == 'negative':
                processed_frame = 255 - frame

            output_queue.put(processed_frame)
        output_queue.put(None)

    threading.Thread(target=read_frames).start()
    threading.Thread(target=process_frames).start()
    threading.Thread(target=process_frames).start()
    threading.Thread(target=process_frames).start()
    threading.Thread(target=process_frames).start()

    while True:
        processed_frame = output_queue.get()
        if processed_frame is None:
            break
        out.write(processed_frame)

    video.release()
    out.release()

    final = time.time()
    print("Tempo de processamento: ", format_time(final - inicial))

# Para usar o filtro cinza
process_video('./videos/Resident_Evil_2.mp4', './out/output2.mp4', 'negative')
