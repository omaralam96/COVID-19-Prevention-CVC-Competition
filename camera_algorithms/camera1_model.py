
import time
import itertools
import cv2
import numpy as np
from operator import itemgetter

class PeopleDetector:
    def __init__(self, yolocfg='camera_algorithms/yolo_weights/yolov3.cfg',
                 yoloweights='camera_algorithms/yolo_weights/yolov3.weights',
                 labelpath='camera_algorithms/yolo_weights/coco.names',
                 confidence=0.8,#0.5.
                 nmsthreshold=0.4):
        self._yolocfg = yolocfg
        self._yoloweights = yoloweights
        self._confidence = confidence
        self._nmsthreshold = nmsthreshold
        self._labels = open(labelpath).read().strip().split("\n")
        self._colors = np.random.randint(
            0, 255, size=(len(self._labels), 3), dtype="uint8")
        self._net = None
        self._layer_names = None
        self._boxes = []
        self._confidences = []
        self._classIDs = []
        self._centers = []
        self._layerouts = []
        self._MIN_DIST = 200    #500
        self._MIN_AREA= 10000  #Area is calculated for Background Removal 
        self.mal_position=0
        self._mindistances = {}

    def load_network(self):
        self._net = cv2.dnn.readNetFromDarknet(
            self._yolocfg, self._yoloweights)
        self._net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self._net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        self._layer_names = [self._net.getLayerNames()[i[0] - 1]
                             for i in self._net.getUnconnectedOutLayers()]
        print("yolov3 loaded successfully\n")

    def predict(self, image):
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
                                     [0, 0, 0], 1, crop=False)
        self._net.setInput(blob)
        start = time.time()
        self._layerouts = self._net.forward(self._layer_names)
        end = time.time()
        print("yolo took {:.6f} seconds".format(end - start))
        return(self._layerouts)

    def process_preds(self, image, outs):
        (frameHeight, frameWidth) = image.shape[:2]
        for out in outs:
            for detection in out:
                scores = detection[5:]
                classId = np.argmax(scores)
                if classId != 0:  # filter person class
                    continue
                confidence = scores[classId]
                area= int(detection[3] * frameHeight)*int(detection[2] * frameHeight)        
                #the area is to remove people from back ground of queue [BACKGROUND REMOVAL]
                if confidence > self._confidence and area > self._MIN_AREA:
                    center_x = int(detection[0] * frameWidth)
                    center_y = int(detection[1] * frameHeight)
                    width = int(detection[2] * frameWidth)
                    height = int(detection[3] * frameHeight)
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)
                    self._classIDs.append(classId)
                    self._confidences.append(float(confidence))
                    self._boxes.append([left, top, width, height])
                    self._centers.append((center_x, center_y))
        indices = cv2.dnn.NMSBoxes(
            self._boxes, self._confidences, self._confidence, self._nmsthreshold)
        for i in indices:
            i = i[0]
            box = self._boxes[i]
            left = box[0]
            top = box[1]
            width = box[2]
            height = box[3]
            self.draw_pred(image, self._classIDs[i], self._confidences[i], left,
                           top, left + width, top + height)
        return self._centers,len(indices),self.mal_position

    def clear_preds(self):
        self._boxes = []
        self._confidences = []
        self._classIDs = []
        self._centers = []
        self._layerouts = []
        self._mindistances = {}
        self.mal_position=0

    def draw_pred(self, frame, classId, conf, left, top, right, bottom):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 7)
        self.find_min_distance(self._centers,frame) 
        

        
    def find_min_distance(self, centers , frame):

        #NON_MAX Suppersion
        centers=sorted(self._centers, key=itemgetter(0))
        new_centers=[]
        i=0
        while i <= (len(centers)-1):
        
            if( i==0 and len(centers)>1 and abs(centers[0][0]-centers[1][0])>30):
                new_centers.append(centers[i])
                
               
            elif(i==len(centers)-1):
                    new_centers.append(centers[i])
           
            elif(abs(centers[i][0]-centers[i+1][0])>30):
                     new_centers.append(centers[i])

            i=i+1  
   
        flag_centers=[0]*len(new_centers)

        ##Checking For Min_Distance and Calculate Number of Mal_Positioned
        i=0
        while i < (len(new_centers)-1):
            if(abs(new_centers[i][0]-new_centers[i+1][0])<self._MIN_DIST):
                flag_centers[i]=1
                flag_centers[i+1]=1
                cv2.line(frame, (new_centers[i]), (new_centers[i+1]), (0, 0, 255), 5)
            i=i+1   
        self.mal_position=flag_centers.count(1)        
        
        

               