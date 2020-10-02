import subprocess
import os
from config.settings import Settings as cfg
from flask import Flask, jsonify
import argparse

PORT = 8010
paramChanged = False
paramValue = None
mainPID = None

app = Flask(__name__)


@app.route('/detectionList')
def detectionList():  # найти станадртную реализацию
    detections = {}
    with open(cfg.CLASSES_FILE, 'rt') as file:
        classes = file.read().rstrip('\n').split('\n')

    for obj in classes:
        for availableObj in cfg.AVAILABLE_OBJECTS:
            if obj == availableObj:
                detections.update({obj: True})
            elif obj != availableObj and obj not in detections.keys():
                detections.update({obj: False}) # сыграл на принципе работы апдейт
    return jsonify(detections)


def killProcess(pid):
    subprocess.Popen('taskkill /F /PID {0}'.format(pid), shell=True)


def runProgram():
    global paramChanged, mainPID
    #while True:  # цикл №0  ломает все
    if paramChanged:
        killProcess(mainPID)
        paramChanged = False  # ахахха эвент драйвер от сани
        # изменить конфиг в енв
        changeStringInFileTo()
    else:
        path = os.path.join(cfg.APP_PATH, "mainImage.py")
        pid = subprocess.Popen(["python", path]).pid
        mainPID = pid


def changeStringInFileTo(): # TODO переписать
    def detectLine():
        stringWithParam = 0
        with open(filepath, 'r') as f:
            for line in f.readlines():
                paramName = re.findall(r'\w=', paramValue)
                if paramName[0] in line:
                    break
                stringWithParam += 1
        return stringWithParam

    import re
    filepath = os.path.join(cfg.APP_PATH, ".env")

    if not paramValue:
        raise Exception("None param value")
    stringWithParam = detectLine()
    with open(filepath, 'w') as f:
        for i in range(stringWithParam):
            f.readline()
        f.writelines(paramValue)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--no-run-detections', action='store_true', default=False, help='Решил, что будет возможность запускать сервер отдельно от распознавалки')
    args = parser.parse_args()

    if not args.no_run_detections:
        runProgram()
    app.run(port=PORT, host="localhost")

