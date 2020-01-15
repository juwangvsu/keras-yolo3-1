import os
import sys
from subprocess import Popen
f = open("valid_list.txt", "r")
for x in f:
  print(x)
  xx=x.split('.')[0]
  Popen(['nohup', '/media/student/code1/keras-yolo3/create_link.sh', '/media/student/voc2012/VOCdevkit/VOC2012/val_image/'+xx+'.jpg','/media/student/voc2012/VOCdevkit/VOC2012/JPEGImages/'+xx+'.jpg'])
  Popen(['nohup', '/media/student/code1/keras-yolo3/create_link.sh', '/media/student/voc2012/VOCdevkit/VOC2012/val_ann/'+xx+'.xml','/media/student/voc2012/VOCdevkit/VOC2012/Annotations/'+xx+'.xml'])
