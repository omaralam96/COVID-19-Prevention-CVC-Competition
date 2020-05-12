import cv2
import numpy as np
import datetime
import pytesseract 
from os import path
from openpyxl import load_workbook
from openpyxl.workbook import Workbook
##path for pytesseract responsible for OCR 
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
##mask label , glove label, emp_id,emp_name,profile_pic to be sent to gui
mask_label=""
glove_label=""
emp_Id=""
emp_Name=""
emp_Time=""
profile_pic = cv2.imread("images/prof.png")
##counter for ocr after detecting ID card of employee
counter_frames = 1
##show employee info for certain time after detecting his/her ID
reset_emp_info = 0
##variables to detect that the ID of employee is detected
done =0
detected =0
##ID of employee detected
text = ""
##threshold for gloves
gloves_threshold = 35000
##Detectors for face ,mouth, nose 
face_cascade = cv2.CascadeClassifier("detector_xml/haarcascade_frontalface_default.xml")
mouth_cascade = cv2.CascadeClassifier('detector_xml/haarcascade_mcs_mouth.xml')
nose_cascade = cv2.CascadeClassifier('detector_xml/haarcascade_mcs_nose.xml')
##Dictionary for employee IDs and names
names_dict = {"1501075":"Martin Joseph","1500935":"Omar Hesham","1500920":"Omar mohamed","1501333":"Mahmoud Ibrahim"}

# font for cv2.text. 
font = cv2.FONT_HERSHEY_SIMPLEX 
# org 
org = (50, 30) 
# fontScale 
fontScale = 0.6
# colors used in BGR 
color_pass = (0, 255, 0)
color_orange = (52,177,235)
  
# Line thickness of 2 px 
thickness = 2
##counter for ok to pass after detecting employee wearing gloves and face mask 
counter_pass =1
counter_pass_threshold =10
##flag for alternating from safety check to ID scanning
flag_thread = 0
###########################################################################
##Id checking and recording in excel sheet
def text_checking():
    global text,done,detected
    wb =  load_workbook(filename = "Attendance.xlsx")
    sheet = wb.active                

    text = text.replace("-", "")
    text = text.replace(".", "")
    text = text.replace(' ', "")
    text = text.rstrip()
    ##if ID is found in employee dictionary
    if text in names_dict :
        done =1
        detected=0
        now = datetime.datetime.now()
        cells =sheet["A"]            
        for cell in cells:
           if text ==cell.value:
               break
        else:
            ##recording attendance in Attendance.xlsx
            new_Attendance= [text,str(now.hour)+":"+str(now.minute)+":"+str(now.second),str(now.day)+"/"+str(now.month)+"/"+str(now.year)]
            sheet.append(new_Attendance)  
            wb.save(filename="Attendance.xlsx")                        
######################################################################
## main function which is connected to main.py
## responsible for detecting face mask , gloves and ID of employee 
def loginSystem(img):
    global flag_thread,counter_pass,text,names_dict,done,detected,counter_frames,reset_emp_info
    global mask_label,glove_label,emp_Id,emp_Name,emp_Time,profile_pic
    
    # flag_thread = 0 responsible for detecting face mask , gloves
    if flag_thread == 0:
        reset_emp_info += 1
        if reset_emp_info == 20:
            emp_Id,emp_Name,emp_Time = "","",""
            profile_pic = cv2.imread("images/prof.png")

        img_cpy = img.copy()
        ##Dividing screen to show employee where to put his hands and face
        img = cv2.line(img, (200,0), (200,900), color_pass, thickness)
        img = cv2.line(img, (450,0), (450,900), color_pass, thickness)
        cv2.putText(img, 'You hand here', (50,450), font,  fontScale, color_orange, thickness, cv2.LINE_AA)
        cv2.putText(img, 'You face here', (250,450), font,  fontScale, color_orange, thickness, cv2.LINE_AA)
        cv2.putText(img, 'You hand here', (460,450), font,  fontScale, color_orange, thickness, cv2.LINE_AA)
        #####gloves dtection
        gloves_img = img_cpy.copy()
        gloves_img[:, 200:450, [0, 1, 2]] = 0
        #plt.imshow(gloves_img)
        hsv_frame = cv2.cvtColor(gloves_img, cv2.COLOR_BGR2HSV)
        # Blue color
        low_blue = np.array([94, 80, 2])
        high_blue = np.array([126, 255, 255])
        blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detect the faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)
        mouth_rects = []
        nose_rects = []
        # loop on detected faces
        for (x, y, w, h) in faces:
            # Detect the mouth
            mouth_rects = mouth_cascade.detectMultiScale(gray[y+int((h/2)):y+h,x:x+w], 1.3,11)
            # Detect the nose
            nose_rects = nose_cascade.detectMultiScale(gray[y+int(h/3):y+h,x:x+w], 1.3, 4)
            #loop on detected mouths to draw rectangles on them
            for (mx,my,mw,mh) in mouth_rects:
                my = int(my - 0.15*mh)
                cv2.rectangle(img, (x+mx,y+int(h/2)+my), (x+mx+mw,y+int(h/2)+my+mh), (0,0,255), 3)
                break
            #loop on detected noses to draw rectangles on them
            for (nx,ny,nw,nh) in nose_rects:
                cv2.rectangle(img, (x+nx,y+ny+int(h/3)), (x+nx+nw,y+ny+nh+int(h/3)), (255,0,0), 3)
                break
            break
        #number of white pixels in gloves mask to detect gloves
        white_pixels = np.count_nonzero(blue_mask == 255)
        #condition that mouth ,nose are covered with face mask and gloves are worn 
        if(len(faces)>len(mouth_rects) and len(faces)>len(nose_rects)) and white_pixels > gloves_threshold:
            counter_pass +=1
            if counter_pass == counter_pass_threshold:
                flag_thread = 1
                counter_frames = 1
                done =0
                detected =0
        #condition that Nose isn't covered 
        elif(len(faces)>len(mouth_rects) and len(faces)==len(nose_rects)):
            mask_label="Nose isn't covered" 
        #condition that Mouth and nose aren't covered 
        elif len(faces)==len(mouth_rects) and len(faces)==len(nose_rects):
            mask_label="Mouth and nose aren't covered"   
        #condition that Mouth and nose are covered with face mask
        elif(len(faces)>len(mouth_rects) and len(faces)>len(nose_rects)):
            mask_label="Mask position is correct"  
        #condition for detecting gloves                     
        if white_pixels < gloves_threshold:
            glove_label="No gloves detected"
        else:
           glove_label="Gloves detected"
    ######################################
    # flag_thread = 1 responsible for detecting ID using OCR from employee ID card
    elif flag_thread == 1:
        cropped_image = img[70:230,90:340]
        glove_label="Gloves detected"
        mask_label="Mask position is correct" 
        gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        ##showing the user where to show his/her ID on the screen
        if done == 0:
            cv2.rectangle(img, (90, 70), (340, 230), (0, 0, 255), 2) #card
            cv2.putText(img, 'place your card here', (100,100), font,  0.7, (0,0,255), 1, cv2.LINE_AA)
        ##Notify the user when an ID card is detected infront of screen
        if detected ==1 and done == 0:
            cv2.putText(img, 'Scanning....', (120,130), font,  1, (0,255,255), 1, cv2.LINE_AA)
        ##Showing employee information from the system after detection his/her ID
        elif done ==1:
            cv2.rectangle(img, (90, 70), (340, 230), (0, 255, 0), 2) #card
            cv2.putText(img, 'Scanning Done', (100,150), font,  1, (0,255,0), 2, cv2.LINE_AA)
            emp_Id=text
            emp_Name=names_dict[text]
            emp_Time=str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute) 
            profile_pic=cv2.imread("images/"+names_dict[text]+".jpg")
            flag_thread = 0
            counter_pass =1
            reset_emp_info = 0          
        ##Detecting ID card infront of screen using the face of employee in ID
        face_crop = gray[:,150:250]
        faces = face_cascade.detectMultiScale(face_crop, 1.1, 5)
        for (x, y, w, h) in faces:
            x += 160
            cv2.rectangle(img, (x+80, y+70), (x+80+w, y+70+h), (0, 255, 0), 2)
        if len(faces) == 1:
            detected = 1
            counter_frames+=1
            
        ##if there is face detected in the Id scanning starts
        if len(faces) == 1 and counter_frames%30 ==0 and done ==0:
            gray_cropped = gray[y:y+h+50,x-150:x-60]
            
            # Preprocessing the image starts 
            gray_cropped = cv2.resize(gray_cropped, (gray_cropped.shape[0]*3,gray_cropped.shape[1]*3))
            gray = gray_cropped
            _,thresh_ = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
            ret, thresh1 = cv2.threshold(thresh_, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV) 
            
            # Specify structure shape and kernel size. 
            # Kernel size increases or decreases the area 
            # of the rectangle to be detected. 
            # A smaller value like (10, 10) will detect 
            # each word instead of a sentence. 
            rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18)) 
            
            # Appplying dilation on the threshold image 
            dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1) 
            
            # Finding contours 
            contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, 
            												cv2.CHAIN_APPROX_NONE) 
            
            # Creating a copy of image 
            cropped_image = cropped_image[y:y+h+50,x-150:x-60]
            cropped_image = cv2.resize(cropped_image, (cropped_image.shape[0]*3,cropped_image.shape[1]*3))
            im2 = cropped_image.copy() 
            # A text file is created and flushed 
            
            # Looping through the identified contours 
            # Then rectangular part is cropped and passed on 
            # to pytesseract for extracting text from it 
            # Extracted text is then written into the text file 
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                cropped = im2[y:y + h, x:x + w]
                custom_config = r'--oem 3 --psm 6 outputbase digits'
                text = pytesseract.image_to_string(cropped, config=custom_config)
                if len(text) == 7:
                    break
            text_checking()
    return img,mask_label,glove_label,emp_Id,emp_Name,emp_Time,profile_pic

  
