import cv2

    # Converte para cinza
def process_quadro(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return gray_framew

def process_video(input_video_path, output_video_path):
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

# processar o video e a saida sera salva em output.mp4
process_video('alokk.mp4', 'output.mp4')