# USAGE
# python detect.py --images images

# import the necessary packages
from __future__ import print_function
import imutils
import cv2
from operator import itemgetter
# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

font = cv2.FONT_HERSHEY_SIMPLEX

# improve detection accuracy by decreasing width
min_Distance=120 #70

po=0
n_total=0
n_mal=0
position=[0]*100
color=[0]*100
last_count=0

def queue(frame):
    
#    frame=cv2.flip(frame,1)
    
    image = imutils.resize(frame, width=min(400, frame.shape[1]))
    orig = image.copy()
    global po;
    global n_total,n_mal,position,color,last_count;
    po=po+1
    rects=[]     
    
    
    if po%15==0 :
        po=po+1;
        # detect people in the image
        (rects, weights) = hog.detectMultiScale(image, winStride=(1, 1),
        		padding=(8, 8), scale=1.25)
        
        #sorting according to distance x axis
        rects=sorted(rects, key=itemgetter(0))
        id=[]
        new_rects=[]    
        i=0
        
        #NON_MAX SUPPRESSING
        while i <= (len(rects)-1):
        
            if( i==0 and len(rects)>1 and abs(rects[0][0]-rects[1][0])>30):
                new_rects.append(rects[i])
                
               
            elif(i==len(rects)-1):
                    new_rects.append(rects[i])
           
            elif(abs(rects[i][0]-rects[i+1][0])>30):
                     new_rects.append(rects[i])
                   
               
            i=i+1     
        
        rects=new_rects
        last_count=len(rects);
        print("NEW_COUNT = "+str( len(rects)))
        n_total=len(rects)
        n_mal=0
        
        
        #Drawing Red Circles on people of Unsafe Position and
        # green circles on people in safe position
        if(len(rects)==1):
            position[0]=(int(rects[0][0]+rects[0][2]/2));
            color[0]=(0, 255, 0);
            cv2.circle(orig,(int(rects[0][0]+rects[0][2]/2),160),5,(0, 255, 0),10)
        for i in range(len(rects)-1):
            position[i]=(int(rects[i][0]+rects[0][i]/2));
            if( i==0):
               
#                color[0]=(0, 255, 0);
                cv2.circle(orig,(int(rects[i][0]+rects[i][2]/2),160),5,(0, 255, 0),10) 
            distance=rects[i+1][0]-rects[i][0]
            print(distance)
            if distance< min_Distance:
#                color[i]=(0, 0, 255);
               
                cv2.circle(orig,(int(rects[i+1][0]+rects[i+1][2]/2),160),5,(0, 0, 255),10)
                id.append(i)
                n_mal=n_mal+1
            else:
#                color[i]=(0, 255, 0);
                cv2.circle(orig,(int(rects[i+1][0]+rects[i+1][2]/2),160),5,(0, 255, 0),10)
               
        id=[]
        frame = cv2.resize(orig,(400,225), interpolation = cv2.INTER_CUBIC)

    
#    if(last_count>=1):
#        cv2.circle(orig,(position[0],160),5,color[0],2)
#    i=0    
#    while i < last_count -1:
#        print("------"+str(position[i]))
#        cv2.circle(orig,(position[i],160),5,color[i],2)
#        i=i+1;
#        
    cv2.line(orig,(0,160),(400,160),(255, 0, 0),1)
    return orig,n_total,n_mal
