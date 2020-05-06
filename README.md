<p align="center">
<img  src = images/cvc.png>
</p>

# COVID-19-Prevention

## Content
* [Description](#Description)

* [Installation](#Installation)

* [Usage](#Usage) 

* [Our Team](#Our-team)


- - - 
## Description

Our Project’s idea is to mimic the fingerprint systems that is found in companies to record the arrival and leaving time of employees but instead of using fingers to avoid the spread of corona virus, we will use two cameras as follow:


*   First camera:

> Its task is to maintain appropriate **Social distance**.

<p align="center"><img  src = images/socialDistance.png width="200" ></p>

*   Second camera

> 1.   Its first task is face mask detection which aim to detect faces and detect whether the mouth and nose of each entering employee are properly covered with face mask or not.

<p align="center"><img  src = images/face.jpg width="200" ></p>

>2.   Its second task is to detect if the employee is wearing gloves or not 

<p align="center"><img  src = images/gloves_and_mask.jpg width="200" ></p>

>3.  If the employee follows safety rules mentioned above, then the third task is OCR system which aim to detect ID of an employee entering the company. And record in sheet his/her arrival time

<p align="center"><img  src = images/fingerprint.jpg width="200" ></p>

- - - 
## Installation

### Steps to install

1. Clone the repository. 
2. Install the required packages.
>pip install -r requirements.txt
3. Install [pytesseract](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20200328.exe) for OCR detection
4. Insert in ***model*** folder, download [yolo weights](https://pjreddie.com/media/files/yolov3.weights
)
- - - 
## Usage
>click on **main.exe**


*   Social distancing

<p align="center"><img  src = images/Social_distance_demo.gif ></p>

*   Fingerprint system

<p align="center"><img  src = images/Login_Demo.gif ></p>
- - - 

## Our-team


1.   Omar Hesham Hanfy
2.   Omar Mohamed Alam
3.   Martin Joseph William
4.   Mark Youssef Shouhdy
5.   Mahmoud Ibrahim Mohamed



