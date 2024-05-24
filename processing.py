import cv2
import time
import multiprocessing

def format_time(seconds):
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d:%02d" % (hours, minutes, seconds)

def process_quadro(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return gray_frame

def read_frames(frame_queue):
    video = cv2.VideoCapture('./videos/Resident_Evil_2.mp4')
    while True:
        ret, frame = video.read()
        if ret:
            frame_queue.put(frame)
        else:
            break
    # Sinaliza o fim da leitura
    for _ in range(4):  # Envia um sinal de fim para cada processo
        frame_queue.put(None)
    video.release()

def process_frames(frame_queue, output_queue):
    while True:
        frame = frame_queue.get()
        if frame is None:  # Sinal de fim
            break
        processed_frame = process_quadro(frame)
        output_queue.put(processed_frame)
    # Sinaliza o fim do processamento
    output_queue.put(None)

def process_video(input_video_path, output_video_path):
    inicial = time.time()

    video = cv2.VideoCapture(input_video_path)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS)
    video.release()

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height), isColor=False)

    frame_queue = multiprocessing.Queue(maxsize=10)
    output_queue = multiprocessing.Queue(maxsize=10)

    # Iniciar processos
    reader_process = multiprocessing.Process(target=read_frames, args=(frame_queue,))
    reader_process.start()

    num_processes = 4
    processes = []
    for _ in range(num_processes):
        process = multiprocessing.Process(target=process_frames, args=(frame_queue, output_queue))
        process.start()
        processes.append(process)

    # Escrever os quadros processados
    processed_frames = 0
    while processed_frames < num_processes:
        processed_frame = output_queue.get()
        if processed_frame is None:
            processed_frames += 1
        else:
            out.write(processed_frame)

    # Aguardar o término dos processos
    reader_process.join()
    for process in processes:
        process.join()

    out.release()

    final = time.time()
    print("Tempo de processamento: ", format_time(final - inicial))


if __name__ == '__main__':
    process_video('./videos/Resident_Evil_2.mp4', './out/output1.mp4')