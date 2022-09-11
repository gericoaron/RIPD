import cv2 as open_cv
import numpy as np
import logging
from drawing_utils import draw_contours
from colors import COLOR_GREEN, COLOR_WHITE, COLOR_BLUE
import cv2
from datetime import datetime
import pyttsx3
import threading
import telepot
import time
from os import mkdir
import win32gui
import win32con
from win10toast import ToastNotifier
import time
from PIL import Image
from tkinter import *
import os
from timeit import default_timer


#defining python desktop notifier
toaster = ToastNotifier()


#set directory of recorded video to footages folder
try:
    mkdir('footages')
except FileExistsError:
    pass

#defining the voice alert when motion is detected
def thread_voice_alert(engine):
    engine.say("Motion Detected")
    engine.runAndWait()
    
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)


#Motion Detection
class MotionDetector:
    LAPLACIAN = 1.4
    DETECT_DELAY = 1
        

    def __init__(self, video, coordinates, start_frame):
        self.video = video #('rtsp://192.168.254.108/live/ch00_1') #change to rtsp protocol for live performance ('rtsp://192.168.254.103:8080/h264_ulaw.sdp')
        self.coordinates_data = coordinates
        self.start_frame = start_frame
        self.contours = []
        self.bounds = []
        self.mask = []

        
       
    def detect_motion(self):
        capture = open_cv.VideoCapture(self.video)
        capture.set(open_cv.CAP_PROP_POS_FRAMES, self.start_frame)

        
        # #Object Detection ---------------------------------------------------------------
        # whT = 320
        # confThreshold =0.5
        # nmsThreshold= 0.2
        
        # #### LOAD MODEL
        # ## Coco Names
        # classesFile = "coco.names"
        # classNames = []
        # with open(classesFile, 'rt') as f:
        #     classNames = f.read().rstrip('\n').split('\n')

        # #print(classNames)
        # ## Model Files
        # modelConfiguration = 'yolov3.cfg'
        # modelWeights = 'yolov3.weights'
        # net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
        # net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        # net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        
        # def findObjects(outputs,img):
        #     hT, wT, cT = img.shape
        #     bbox = []
        #     classIds = []
        #     confs = []
        #     for output in outputs:
        #         for det in output:
        #             scores = det[5:]
        #             classId = np.argmax(scores)
        #             confidence = scores[classId]
        #             if confidence > confThreshold:
        #                 w,h = int(det[2]*wT) , int(det[3]*hT)
        #                 x,y = int((det[0]*wT)-w/2) , int((det[1]*hT)-h/2)
        #                 bbox.append([x,y,w,h])
        #                 classIds.append(classId)
        #                 confs.append(float(confidence))
        
        #     indices = cv2.dnn.NMSBoxes(bbox, confs, confThreshold, nmsThreshold)
        
        #     for i in indices:
        #         i = i[0]
        #         box = bbox[i]
        #         x, y, w, h = box[0], box[1], box[2], box[3]
        #         # print(x,y,w,h)
        #         cv2.rectangle(img, (x, y), (x+w,y+h), (255, 255 , 255), 2)
        #         cv2.putText(img,f'{classNames[classIds[i]]} {int(confs[i]*100)}%',
        #                 (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

        # #Object Detection ---------------------------------------------------------------

    #Adjusting the size of the camera

        #capture.set(open_cv.CAP_PROP_FRAME_WIDTH,1920)
        #capture.set(open_cv.CAP_PROP_FRAME_HEIGHT,1080)
        #capture.set(3,300)
        #capture.set(4,300)
        #width = capture.get(3)
        #height = capture.get(4)

    #prompt question before opening camera vision
        print("*"*80+"\n"+" "*30+"Welcome to Concepction Illegal Parking Detection System\n"+"*"*80)
        ask = int(input('do you want to Start cctv ?\n1. Yes\n2. No\n>>> '))
        if ask ==1:
            exit
            print("--Help:  1. press esc/q key to exit cctv")
        elif ask ==2:
            print("ba bye! be safe & secure!")
            capture.release()
            open_cv.destroyAllWindows()

    #automatically record and save to footages folder
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        date_time = time.strftime("recording %H-%M-%d %m %y") #set current time as video name
        output = cv2.VideoWriter('footages/'+date_time+'.avi',fourcc,20.0,(1600,900))
        
    #coordinates
        coordinates_data = self.coordinates_data
        logging.debug("coordinates data: %s", coordinates_data)

        for p in coordinates_data:
            coordinates = self._coordinates(p)
            logging.debug("coordinates: %s", coordinates)

            rect = open_cv.boundingRect(coordinates)
            logging.debug("rect: %s", rect)

            new_coordinates = coordinates.copy()
            new_coordinates[:, 0] = coordinates[:, 0] - rect[0]
            new_coordinates[:, 1] = coordinates[:, 1] - rect[1]
            logging.debug("new_coordinates: %s", new_coordinates)

            self.contours.append(coordinates)
            self.bounds.append(rect)
            
            mask = open_cv.drawContours(
                np.zeros((rect[3], rect[2]), dtype=np.uint8),
                [new_coordinates],
                contourIdx=-1,
                color=255,
                thickness=-1,
                lineType=open_cv.LINE_8)
                
            mask = mask == 255
            self.mask.append(mask)
            logging.debug("mask: %s", self.mask)

        statuses = [False] * len(coordinates_data)
        times = [None] * len(coordinates_data)

        img_counter = 0
        
        while capture.isOpened():
            result, frame, = capture.read()

        #additional code for object detection

            # #blob function for object detect
            # blob = cv2.dnn.blobFromImage(frame, 1 / 255, (whT, whT), [0, 0, 0], 1, crop=False)
            # net.setInput(blob)
            # layersNames = net.getLayerNames()
            # outputNames = [layersNames[i[0]-1] for i in net.getUnconnectedOutLayers()]
            # outputs = net.forward(outputNames)
            # findObjects(outputs,frame)

        #time
            t = time.ctime()
            cv2.rectangle(frame,(5,5,100,20),(255,255,255),cv2.FILLED)
            cv2.putText(frame,"Camera 1",(20,20),
                        cv2.FONT_HERSHEY_DUPLEX,0.5,(5,5,5),2)            
            cv2.putText(frame,t,(120,20),
                        cv2.FONT_HERSHEY_DUPLEX,0.5,(5,5,5),1)
            
            #additional code for fourcc

            if result:
                vidout=cv2.resize(frame,(1600,900)) #create vidout funct. with res=300x300
                output.write(vidout) #write frames of vidout function
                

            if frame is None:
                break

            if not result:
                raise CaptureReadError("Error reading video capture on frame %s" % str(frame))

            blurred = open_cv.GaussianBlur(frame.copy(), (5, 5), 3)
            grayed = open_cv.cvtColor(blurred, open_cv.COLOR_BGR2GRAY)
            new_frame = frame.copy()
            logging.debug("new_frame: %s", new_frame)
            
            position_in_seconds = capture.get(open_cv.CAP_PROP_POS_MSEC) / 10000.0
            
            for index, c in enumerate(coordinates_data):
                status = self.__apply(grayed, index, c)
                
                if times[index] is not None and self.same_status(statuses, index, status):
                    times[index] = None

                    #calling the function voice alert everytime motion detects
                    
                    t = threading.Thread(target=thread_voice_alert, args=(engine,))
                    t.start()
                    

                    #auto capture
                    time_stamp = int(time.time())
                    fcm_photo = "C:/Users/manga/Documents/RIPD/Illegal_Parking/motion captured/AutoCapture_Motion_{}.png".format(img_counter)
                    cv2.imwrite(fcm_photo, frame)
                    print("{} written!".format(fcm_photo))
                    img_counter += 1

                    #convert .png to ico file for toaster notification custom icon
                    file_name = 'images/malogo.ico'

                    toaster.show_toast("RPID Notification", "Motion Detected", threaded=True, icon_path=file_name, duration = 2)

                    

                    continue
                    
                
                if times[index] is not None and self.status_changed(statuses, index, status):
                   
                    if position_in_seconds - times[index] >= MotionDetector.DETECT_DELAY:
                        
                        

                        statuses[index] = status
                        times[index] = None

                        
                                
                            
                        
                    continue
                    
                if times[index] is None and self.status_changed(statuses, index, status):
                   
                    times[index] = position_in_seconds
                
                    
                

            for index, p in enumerate(coordinates_data):
                coordinates = self._coordinates(p)

                color = COLOR_GREEN if statuses[index] else COLOR_BLUE
                draw_contours(new_frame, coordinates, str(p["id"] + 1), COLOR_WHITE, color)
            
                
                
            #show time good on (webcam)
            t = time.ctime()
            cv2.rectangle(new_frame,(5,5,100,20),(255,255,255),cv2.FILLED)
            cv2.putText(new_frame,"Camera 1",(20,20),
                        cv2.FONT_HERSHEY_DUPLEX,0.5,(5,5,5),2)
            cv2.putText(frame,t,(120,20),
                        cv2.FONT_HERSHEY_DUPLEX,0.5,(5,5,5),1)

            #screenshotspace good for (webcam)
            k = cv2.waitKey(1)

            if k%256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break

            
            elif k%256 == 32:

                #manual capture

                time_stamp = int(time.time())
                fcm_photo = "C:/Users/manga/Documents/RIPD/Illegal_Parking/manual captured/ManualCapture{}.png".format(img_counter)
                cv2.imwrite(fcm_photo, new_frame)
                print("{} written!".format(fcm_photo))
                img_counter += 1

                

                #telegram function
                token = '2075301639:AAEMfBNirC8XigaE78DFB2CsbTjoWVuRSlY' # telegram token
                receiver_id = 1890127935 # https://api.telegram.org/bot<TOKEN>/getUpdates 

                bot = telepot.Bot(token)

                bot.sendMessage(receiver_id, 'Manual Captured!') # send a activation message to telegram receiver id
                bot.sendPhoto(receiver_id, photo=open(fcm_photo, 'rb'))
                print(f'{time_stamp}.png has sent'.format(img_counter))

                #calling notifier function
                file_name = 'images/malogo.ico'  

                toaster.show_toast("RPID Notification","Manual Shot!", threaded=True, icon_path=file_name, duration = 2)

            cv2.imshow('Real-Time Illegal Parking Detection', new_frame)
            
            if k == ord("q"):
                break

        
        engine.stop()
        capture.release()
        output.release()
        open_cv.destroyAllWindows()

        
    #applying coordinator process
    def __apply(self, grayed, index, p):
        coordinates = self._coordinates(p)
        logging.debug("points: %s", coordinates)

        rect = self.bounds[index]
        logging.debug("rect: %s", rect)

        roi_gray = grayed[rect[1]:(rect[1] + rect[3]), rect[0]:(rect[0] + rect[2])]
        laplacian = open_cv.Laplacian(roi_gray, open_cv.CV_64F)
        logging.debug("laplacian: %s", laplacian)

        coordinates[:, 0] = coordinates[:, 0] - rect[0]
        coordinates[:, 1] = coordinates[:, 1] - rect[1]

        status = np.mean(np.abs(laplacian * self.mask[index])) < MotionDetector.LAPLACIAN
        
        logging.debug("status: %s", status)
        
        

        return status

    @staticmethod
    def _coordinates(p):
        return np.array(p["coordinates"])

    @staticmethod
    def same_status(coordinates_status, index, status):
        return status == coordinates_status[index]
        
    @staticmethod
    def status_changed(coordinates_status, index, status):
        return status != coordinates_status[index]
        

class CaptureReadError(Exception):
    pass
