# RIPD
Real time illegal parking CCTV monitoring assist the barangay personnel in improving the roads in the area. Also, drivers should be thought not to park anywhere they want, because most people who parked anywhere cause accidents in the area due to obstructed vehicles.

# OBJECTIVE
In this work, we present an illegal parking detection system based on a deep learning approach, which aims to facilitate better inspection for illegal parking. Through this system, we will create a motion detection that automatically detects and recognizes motion in a illegal parking spot and sends a real-time alert to the law enforcement.  All vehicles inside restrict zones are determined as illegal parking or considered obstruction by extending the capabilities of this system such as alerting everytime motion is detected inside of a region of interest, fixing the problem of the barangay personnels to manually examine and patrol the area resulting of a waste of time and energy. not only that but this system can improve their security on illegal parking and obstruction problem.

# SOLUTION
Using AI based approach to detect illegal parking of vehicles (Mostly Cars) from an image. The model will receive a region of interest of an still image from the camera vision of through the user of the system, then it will try to predict the motion status inside the drawned ROI set by the user, then when a car goes inside the region of interest the model will automatically capture the event using screenshot and send an alert to the user. 

# OVERVIEW
Some overview of the detection performance tested by a toy decoy from IP camera using RTSP Protocol. Region of interest will stay green when no one parks, However will
turn red when motion is detected (e.g 10 seconds). 

<i>No motion / Parking detected (green roi)</i>

![ManualCapture4](https://user-images.githubusercontent.com/93422550/139554358-3ca26a7f-89eb-4c41-8465-894a30e4ac21.png)

<i>Motion Detected (red roi)</i>

![ManualCapture3](https://user-images.githubusercontent.com/93422550/139554342-11f9c42d-5a34-4316-be98-5fb3a2dd971c.png)

When the model detects motion inside the ROI automatic motion capture will trigger and save it via local storage and a desktop alert will send to the main server(in our case for testing we used laptop), Also autorecord of footage will trigger once the system is opened.

![Screenshot (32)](https://user-images.githubusercontent.com/93422550/139555929-ee1a9897-bf5c-439d-b849-fff8fe3420e3.png)

User also can use manual screenshot function fo the system for gathering evidence that will directly save also to the local storage and send the photo to "telegram application" (mobile/PC) this can solve the problem of printing solid copy evidence and improve their efficiency and effectiveness in monitoring real-time.

![242940177_616341949729960_4038457934568155221_n](https://user-images.githubusercontent.com/93422550/139556008-44781c73-cfbb-41ad-a4df-8b9dd2b512be.jpg)


# <i>Software Important to install</i>

  * Python 3.9.7 
  * Microsoft Visual Studio and C++ Build Tools
  * CUDA and CUDNN for NVIDIA for using GPU (optional)
  * Protoc for Protocol Buffers from the official Github Repo
  * Tensorflow Object Detection API for use with Python (optional)
  
# <i>Links used</i>

  * Visual Studio - https://visualstudio.microsoft.com/vs... 
  * CUDA 10.1 -  https://developer.nvidia.com/cuda-10....
  * CUDNN 7.6.5 -  https://developer.nvidia.com/rdp/cudn... 
  * Protoc - https://github.com/protocolbuffers/pr...
  * Tensorflow Models GitHub - https://github.com/tensorflow/models 

# To Run

  <i> 1. Clone Github Repository to your Local Storage </i>
  
  <i> 2. Install Required Dependencies </i>
        on your command prompt type - pip3 install -r requirements.txt
        
  <i> 3. Read runme.txt </i>
  
  <i> 4. Program flow is as follows (make sure you are running inside "/Illegal_Parking" on cmd): </i>
  
  * User inputs file name for a video, a still image from the video or from the camera vision, and a path for the output file of parking space coordinates.
  * User clicks 4 corners for each spot they want tracked. Presses 'q' when all desired spots are marked.
  * Video begins with the user provided boxes overlayed the video. Occupied spots initialized with red boxes, available spots with green.

<i> Note: if you want to change for testing you need to change or comment out the rtsp here then type and replace with "video" </i>

![Screenshot (34)](https://user-images.githubusercontent.com/93422550/139556348-1344a4ee-d359-462f-9bf3-7f9a1d79e9c0.png)

# <i>Other Tools Used</i>
  * Laptop or PC for local server (High specs is better)
  * IPC or IP camera that supports RTSP and ONVIF Protocol
  * External Monitor for better manual monitoring and managing using free VMS (Video Management Software)
  * VLC media player as my VMS (We prioritize using simple video managing software)
  * ONVIF Device Manager for getting the RTSP link of the IPC
  * Visual Studio Code for coding
  * Wifi Router (Need to have same connection, Server and IPC to work RTSP / ONVIF)
  * Telegram Application for receiving additonal alerts and manual captured photos.


