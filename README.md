# social-aware-sensor-package
This code was written in order to recognize multiple faces expressions with 360 dualfisheye cameras.
I used theta S camera - capturing 360 dualfisheye images with 15 fps.

I used ffmpeg to convert dualfisheye image to rectangular image.
the mapping file was created by "projection.c" program which creates the files
"fisheye_grid_ymap.pgm" and "fisheye_grid_xmap.pgm"
you can find the program at the link:
https://github.com/raboof/dualfisheye2equirectangular
you can create a mapping file for several cameras and resolutions.

in order to analayze expressions you need to get the affectiva ros node
https://www.affectiva.com/

face detection algorithem was taken from https://realpython.com/face-recognition-with-python/

## ***Running The Program***

***run:***
 
```
python run.py
```
In order to read the data - echo from /omer_data topic

```
rostopic echo /omer_data
```

## ***Explanation of the code***

### ***face_publisher.py:***

Capture dualfisheye photos, converting them to rectangular, display the fixed picture, recognize faces and publish them as image messages to ros topic "/usb_cam/image/raw".


### ***Affectiva ros node (not mine):***

Subscribing to image message in topic "/usb_cam/image/raw", recognize emotions and expression, publish them to ***"/affdex_data"*** topic as ***"affdex_msgs"*** messages


### ***aff_sub.py:***

subscribing to affectiva message ***"/affdex_data"*** and find Person index of each person in the room. then publish  the original affectiva data + Person Index + location + location of looking - as String messages to ***"/omer_data"*** topic.
In addition, the code plotting graphs of one emotion depends on time to all the faces.



### ***The topic "/omer_data":***

Data:
- Time: from start running the code in seconds
- Person ID: index number of the recognized person
- location: x from 0 to 1920 of the person
- LookAt: x from 0 to 1920 of where the person is looking

Emotions:
between 0 and 100, except for valence (-100 and 100)
- 0: Joy
- 1: Anger
- 2: Disgust
- 3: Contempt
- 4: Engagement
- 5: Fear
- 6: Sadness
- 7: Surprise
- 8: Valence

Expressions: 
between 0 and 100
- 0: Attention
- 1: BrowFurrow
- 2: BrowRaise
- 3: ChinRaise
- 4: EyeClosure
- 5: InnerBrowRaise
- 6: LipCornerDepressor
- 7: LipPress
- 8: LipPucker
- 9: LipSuck
- 10: MouthOpen
- 11: NoseWrinkle
- 12: Smile
- 13: Smirk
- 14: UpperLipRaise
- 15: jawDrop
- 16: lipStretch
- 17: dimpler
- 18: cheekRaise
- 19: eyeWiden
- 20: lidTighten

Measurements
face orientation
- 0: InterocularDistance
- 1: Yaw
- 2: Roll
- 3: Pitch

Face_points
elements of face points based on FACS units
- 0 Right Top Jaw
- 1 Right Jaw Angle
- 2 Gnathion 
- 3 Left Jaw Angle 
- 4 Left Top Jaw 
- 5 Outer Right Brow Corner 
- 6 Right Brow Center 
- 7 Inner Right Brow Corner 
- 8 Inner Left Brow Corner 
- 9 Left Brow Center 
- 10 Outer Left Brow Corner 
- 11 Nose Root 
- 12 Nose Tip 
- 13 Nose Lower Right Boundary 
- 14 Nose Bottom Boundary 
- 15 Nose Lower Left Boundary 
- 16 Outer Right Eye 
- 17 Inner Right Eye
- 18 Inner Left Eye
- 19 Outer Left Eye
- 20 Right Lip Corner
- 21 Right Apex Upper Lip
- 22 Upper Lip Center
- 23 Left Apex Upper Lip
- 24 Left Lip Corner
- 25 Left Edge Lower Lip
- 26 Lower Lip Center
- 27 Right Edge Lower Lip
- 28 Bottom Upper Lip
- 29 Top Lower Lip
- 30 Upper Corner Right Eye
- 31 Lower Corner Right Eye
- 32 Upper Corner Left Eye
- 33 Lower Corner Left Eye 

rqt graph:

![screenshot from 2018-10-23 10 46 31](https://user-images.githubusercontent.com/36948734/47344754-d8d20c80-d6b1-11e8-8069-468994990e3c.png)


© Omer Gabay
