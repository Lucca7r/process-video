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

def process_quadro(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return gray_frame

def process_video(input_video_path, output_video_path, batch_size, num_threads):
    inicial = time.time()

    video = cv2.VideoCapture(input_video_path)

    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height), isColor=False)

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
            processed_frames = [(frame_index, process_quadro(frame)) for frame_index, frame in frames]
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

process_video('./videos/Resident_Evil_2.mp4', './out/output1.mp4', 100, 2)