from time import sleep
import cv2 as cv
import argparse
import sys
import numpy as np
import os.path
from glob import glob
import camera



class helmet_detection():
    def __init__(self):
        # Initialize the parameters
        self.confThreshold = 0.5  #Confidence threshold
        self.nmsThreshold = 0.4   #Non-maximum suppression threshold
        self.inpWidth = 416       #Width of network's input image
        self.inpHeight = 416      #Height of network's input image
        # Load names of classes
        classesFile = "obj.names";
        self.classes = None
        with open(classesFile, 'rt') as f:
            self.classes = f.read().rstrip('\n').split('\n')

        # Give the configuration and weight files for the model and load the network using them.
        modelConfiguration = "yolov3-obj.cfg";
        modelWeights = "yolov3-obj_2400.weights";

        self.net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
        self.net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

    # Get the names of the output layers
    def getOutputsNames(self):
        # Get the names of all the layers in the network
        layersNames = self.net.getLayerNames()
        # Get the names of the output layers, i.e. the layers with unconnected outputs
        return [layersNames[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

    # Draw the predicted bounding box
    def drawPred(self, frame, conf, left, top, right, bottom):
        # Draw a bounding box.
        cv.rectangle(frame, (left, top), (right, bottom), (0, 255, 255), 3)
        label = '%.2f' % conf
        # Get the label for the class name and its confidence
        labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.3, 1)
        top = max(top, labelSize[1])

    # Remove the bounding boxes with low confidence using non-maxima suppression
    def postprocess(self, frame, outs):
        frameHeight = frame.shape[0]
        frameWidth = frame.shape[1]
        classIds = []
        confidences = []
        boxes = []
        # Scan through all the bounding boxes output from the network and keep only the
        # ones with high confidence scores. Assign the box's class label as the class with the highest score.
        for out in outs:
            for detection in out:
                scores = detection[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if confidence > self.confThreshold:
                    center_x = int(detection[0] * frameWidth)
                    center_y = int(detection[1] * frameHeight)
                    width = int(detection[2] * frameWidth)
                    height = int(detection[3] * frameHeight)
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)
                    classIds.append(classId)
                    confidences.append(float(confidence))
                    boxes.append([left, top, width, height])

        # Perform non maximum suppression to eliminate redundant overlapping boxes with
        # lower confidences.
        indices = cv.dnn.NMSBoxes(boxes, confidences, self.confThreshold, self.nmsThreshold)
        count_person = 0 # for counting the classes in this loop.
        for i in indices:
            i = i[0]
            box = boxes[i]
            left = box[0]
            top = box[1]
            width = box[2]
            height = box[3]
            #this function in  loop is calling drawPred so, try pushing one test counter in parameter , so it can calculate it.
            self.drawPred(frame, confidences[i], left, top, left + width, top + height)
            #increase test counter till the loop end then print...

    def get_detection(self, frame, copy_frame=None):
        if copy_frame is None:
            copy_frame = frame

        # Create a 4D blob from a frame.
        blob = cv.dnn.blobFromImage(frame, 1 / 255, (frame.shape[0], frame.shape[1]), [0, 0, 0], 1, crop=False)

        # Sets the input to the network
        self.net.setInput(blob)

        # Runs the forward pass to get output of the output layers
        outs = self.net.forward(self.getOutputsNames())

        # Remove the bounding boxes with low confidence
        self.postprocess(copy_frame, outs)

        # Put efficiency information.
        # The function getPerfProfile returns the overall time for inference(t) and
        # the timings for each of the layers(in layersTimes)
        t, _ = self.net.getPerfProfile()
        label = 'Inference time: %.2f ms' % (t * 1000.0 / cv.getTickFrequency())
        cv.putText(copy_frame, label, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))

        return copy_frame, outs

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', default=0,
                        help='Input test video path or web-cam number.')
    args = parser.parse_args()

    cam = camera.VideoCamera(args.path)
    helmet_detection = helmet_detection()

    # Set window
    winName = 'Helmet detection'
    cv.namedWindow(winName, cv.WINDOW_NORMAL)

    while True:
        # Get frame from Camera module
        frame = cam.get_frame()
        frame = cv.resize(frame, dsize=(640, 480), interpolation=cv.INTER_AREA)
        frame, outs = helmet_detection.get_detection(frame=frame, copy_frame=frame)

        # show the frame
        cv.imshow(winName, frame)
        key = cv.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break