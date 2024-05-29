import cv2
import time
import threading
import queue

def format_time(seconds):
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d:%02d" % (hours, minutes, seconds)

def aplicar_sepia(frame):
    sepia_filter = cv2.transform(frame, cv2.COLOR_BGR2BGRA)
    sepia_filter[:, :, 0] = 0.272 * frame[:, :, 2] + 0.534 * frame[:, :, 1] + 0.131 * frame[:, :, 0]
    sepia_filter[:, :, 1] = 0.349 * frame[:, :, 2] + 0.686 * frame[:, :, 1] + 0.168 * frame[:, :, 0]
    sepia_filter[:, :, 2] = 0.393 * frame[:, :, 2] + 0.769 * frame[:, :, 1] + 0.189 * frame[:, :, 0]
    return sepia_filter

def aplicar_negativo(frame):
    return cv2.bitwise_not(frame)

def process_quadro(frame, filter_type):
    if filter_type == 'pb':
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    elif filter_type == 'sepia':
        return aplicar_sepia(frame)
    elif filter_type == 'negativo':
        return aplicar_negativo(frame)
    else:
        raise ValueError("Tipo inválido de filtro. Use 'pb', 'sepia', ou 'negativo'.")

def process_video(input_video_path, output_video_path, batch_size, num_threads, filter_type):
    inicial = time.time()

    video = cv2.VideoCapture(input_video_path)

    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS)

    is_color = filter_type != 'gray'
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height), isColor=is_color)

    frame_queue = queue.Queue(maxsize=2000)
    output_queue = queue.PriorityQueue(maxsize=2000)

    def read_frames():
        frame_index = 0
        while True:
            ret, frame = video.read()
            if ret:
                frame_queue.put((frame_index, frame))
                frame_index += 1
            else:
                break
        for _ in range(num_threads):
            frame_queue.put((None, None))

    def process_frames(batch_size):
        while True:
            frames = []
            for _ in range(batch_size):
                frame_index, frame = frame_queue.get()
                if frame is None:
                    break
                frames.append((frame_index, frame))
            if not frames:
                break
            processed_frames = [(frame_index, process_quadro(frame, filter_type)) for frame_index, frame in frames]
            for processed_frame in processed_frames:
                output_queue.put(processed_frame)
        output_queue.put((-1, None))

    threading.Thread(target=read_frames).start()
    for _ in range(num_threads):
        threading.Thread(target=process_frames, args=(batch_size,)).start()

    next_frame_index = 0
    buffer = {}
    while True:
        frame_index, processed_frame = output_queue.get()
        if frame_index == -1:
            break
        buffer[frame_index] = processed_frame
        while next_frame_index in buffer:
            out.write(buffer.pop(next_frame_index))
            next_frame_index += 1

    video.release()
    out.release()

    final = time.time()
    print("Tempo de processamento: ", format_time(final - inicial))


process_video('./videos/trailerHomemAranha.mp4', './out/output1.mp4', 100, 2, 'negativo')
