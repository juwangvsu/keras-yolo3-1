predict.py 				----- use trained weight file in keras format to detect object
yolo3_one_file_to_detect_them_all.py  ----------  use trained darknet weight file format to detect object
train.py				-------   train yolov3 network, and generate .h5 weight file (keras format)
yolo.py					-------   yolo3 network impl with keras
voc.py					--------  process xml annotation file in voc format
---------1/15/2020 code modify ------------------------
clean up output:
	yolo.py , 	comment tf.Print() lines
	generator.py	comment resizing line
			every 10 batch it resize to a different size, why?
	train.py	ModelCheckpoint
			fit_generator verbose=1 to show progress
			each epoch will run 1713 step @batchsize=8, homepc
				8 minutes 
				8563 steps @batchsize=2, msi, 46 minutes!!

how does the generator work? how many time it is called per epochs?
	in keras-yolo-another, we can see the progress of image processed,
	why not shown here?

checkpoint callback:
	multiple customized checkpoint callbacks ok, called in sequence.
	[[checkpoint2, checkpoint2, ] will write to a new .h5, and
		then move the symbolic link to point to the current one.
	CustomModelCheckpoint2: move the link log_voc/voc2012_newtrain.h5 to the newone.		
	CustomModelCheckpoint: save new weight to voc2012_newtrain.h5, notice that voc2012_newtrain.h5 is a link to log_voc/voc2012_newtrain.h5
	ModelCheckpoiint: save a new .h5 every some epoch

---------1/14-15/2020 -test training with voc2012 as README. -------------------
http://host.robots.ox.ac.uk/pascal/VOC/voc2012/VOCtrainval_11-May-2012.tar
/media/student/voc2012
zoo/config_voc.json
 If the validation set is empty

to start a retrain clean, make sure delete voc_train.pkl, which might contain cache for some data and configuration info 

train cmd:
	python3 train.py -c zoo/config_voc.json
		on homepc, batchsize=8
		make sure rm voc_train.pkl
		if change dataset , train.py code checkpoint
		initial_epoch=20 continue from prev train, saved h5 file will
			be numbered accordingly, change config_voc.json:nb_epochs			> initial_epoch otherwise it will skip train
results:
	log_voc2012
	voc2012_newtrain.h5

training performance:
	msi: batch=2
	tensorboard, loss drop by 25 in 2k, at 70k stall at 10
		the 70k is probably step number, not epoch number
		1/16, loss drop to 7.3486

	continue train at homepc.
	1/15	homepc batch=8, loss 25 in 40k
		1/16 loss drop to 15.03
		1/17 loss drop to 11.8, mAP: 0.6318 ep092-loss11.635.h5
		1/17 training another 100 epoch, ep1xx-loss....h5
		1/18 100 epoch, mAP: 0.6172, ep2088-loss9.125.h5
eval:
	to make evaluate work with voc2012, the val_image and val_ann folder are created
	(1) generate the valid list of file from the train cmd, the modified train cmd will
		automatically generate valid_list.txt which contain the list of filename for valid.
        (2) run
	    python create_valid.py
		to create symbal link inside val_image and val_ann that point to the actual file
		results: media/student/voc2012/VOCdevkit/VOC2012/val_ann/2012_004300.xml and more 
	(3) run
		python3 evaluate.py -c zoo/config_voc.json
		voc2012_newtrain.h5:
			mAP: 0.4640
			mAP_voc2012_msi_rst.txt
		voc.h5:
			mAP: 0.8943
			mAP_voch5_rst.txt	
----------test training with voc2007 -------------------
train use config_voc_local.json
if folder/path/filename error, need to delete cache file for next run
	rm voc_train.pkl
download backend.h5
:
bugs: gpu run out of memory, trying the same trick for tensorflow-yolo-3
	change batch = 4 in config file
	so far still out of memory

--------------------------
test with pretrained voc.h5 or yolov3.weights weights
	download voc.h5
	python3 predict.py -c zoo/config_voc.json -i dog2.jpg 
	eog output/dog2.jpg 
test with backend.h5 result in bad box

test with yolo3.weights directly
	python3 yolo3_one_file_to_detect_them_all.py -w yolov3.weights -i dog2.jpg
	loading weights layer by layer very slow. output good.
	output dog2_detected.jpg
