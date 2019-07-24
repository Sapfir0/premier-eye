import numpy as np
import cv2 
import sys, os

import settings as cfg
import neural_network.maskCNN as mask

def main():
    cap = cv2.VideoCapture(cfg.VIDEO_SOURCE) # 0 - вебка
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    out = cv2.VideoWriter(cfg.OUTPUT_VIDEO, cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
    
    video_capture = cv2.VideoCapture(cfg.VIDEO_SOURCE) 

    while video_capture.isOpened():
        success, frame = video_capture.read()
        if not success:
            break
        
        #работа как с изображением
        r, rgb_image, elapsed_time2 = mask.detectByMaskCNN(frame)
        countedObjMask, masked_image = mask.visualize_detections(rgb_image, r['masks'], r['rois'], r['class_ids'], r['scores'])


        out.write(masked_image)
        cv2.imshow('Video', masked_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Очищаем всё после завершения.
    out.release()
    video_capture.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    main()