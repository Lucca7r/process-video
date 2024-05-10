import cv2
import time


def format_time(seconds):
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d:%02d" % (hours, minutes, seconds)

    # Converte para cinza
def process_quadro(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return gray_frame

def process_video(input_video_path, output_video_path):
    inicial = time.time()
    # abrir video
    video = cv2.VideoCapture(input_video_path)
    

    # pega altura e largura do video e fps 
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS)

    # definir codec para o video de saida 
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height), isColor=False)

    while(video.isOpened()):
        ret, frame = video.read()
        if ret==True:
            # processar o quadro
            processed_frame = process_quadro(frame)

            # escrever o quadro processado no video de saida
            out.write(processed_frame)
        else:
            break

    # liberar os objetos
    video.release()
    out.release()
    
    # tempo final
    final = time.time()
    print("Tempo de processamento: ", format_time(final - inicial))

# processar o video e a saida sera salva em output.mp4
process_video('./videos/alokk.mp4', './out/output1.mp4')