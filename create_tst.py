#create a small test set of 100 to debugging the train code
import os
import sys
from subprocess import Popen
f = open("valid_list.txt", "r")
ind=0
for x in f:
  ind = ind +1
  if ind > 200:
     break
  print(x)
  xx=x.split('.')[0]
  Popen(['nohup', '/media/student/code1/keras-yolo3/create_link.sh', '/media/student/voc2012/VOCdevkit/VOC2012/tst_image/'+xx+'.jpg','/media/student/voc2012/VOCdevkit/VOC2012/JPEGImages/'+xx+'.jpg'])
  Popen(['nohup', '/media/student/code1/keras-yolo3/create_link.sh', '/media/student/voc2012/VOCdevkit/VOC2012/tst_ann/'+xx+'.xml','/media/student/voc2012/VOCdevkit/VOC2012/Annotations/'+xx+'.xml'])
