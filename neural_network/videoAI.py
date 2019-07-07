from imageai.Detection import VideoObjectDetection
import os
import sys
import cv2
import time
import csv

import settings as cfg

counter=0
start_time = time.time()

framesPerSecond=20

def getTime(forFrame):
    def wrapper(frame_number, output_array, output_count):
        start_time = time.time()
        forFrame(frame_number, output_array, output_count)
        print("--- %s seconds ---" % (time.time() - start_time))
    return wrapper


#@getTime
def forFrame(frame_number, output_array, output_count):
    print("FOR FRAME " , frame_number)
    #print("Output for each object : ", output_array)
    print("Уникальные объекты : ", output_count)


def forSeconds(second_number, output_arrays, count_arrays, average_output_count):
    print("SECOND : ", second_number)
    #print("Array for the outputs of each frame ", output_arrays)
    #print("Array for output count for unique objects in each frame : ", count_arrays)
    print("Output average count for unique objects in the last second: ", average_output_count)
    print("------------END OF A SECOND --------------")

def forMinute(minute_number, output_arrays, count_arrays, average_output_count):
    print("MINUTE : ", minute_number)
    #print("Array for the outputs of each frame ", output_arrays)
    #print("Array for output count for unique objects in each frame : ", count_arrays)
    #print("Output average count for unique objects in the last minute: ", average_output_count)
    print("------------END OF A MINUTE --------------")


execution_path = os.getcwd()
detector = VideoObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath( os.path.join(execution_path , "data/resnet50_coco_best_v2.0.1.h5"))
detector.loadModel(detectionSpeed)
customObjects = detector.CustomObjects(person=True, car=True, motorcycle=True, truck=True) #указывает на те объекты, которые мы ищем на кадре

inputVideo = "data/streetLow.mp4" 
if len (sys.argv) > 1:
    inputVideo = sys.argv[1]


def detectMyObjects():
    detections = detector.detectCustomObjectsFromVideo(
        custom_objects=customObjects,
        input_file_path=os.path.join(execution_path , inputVideo), 
        output_file_path=os.path.join(execution_path , "output/" + detectionSpeed + str(minimumPercentageProbability) + "(3)" ),
        frames_per_second=framesPerSecond, 
        #log_progress=True, 
        minimum_percentage_probability=cfg.MINIMUM_PERCENTAGE_PROBABILITY,
        per_second_function=forSeconds,
        per_frame_function=getTime(forFrame),
        per_minute_function=forMinute
        )
    print(detections)


def main():
    detectMyObjects()

if __name__ == "__main__":
    main()




