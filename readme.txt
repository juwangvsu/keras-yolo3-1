predict.py 				----- use trained weight file in keras format to detect object
yolo3_one_file_to_detect_them_all.py  ----------  use trained darknet weight file format to detect object
train.py				-------   train yolov3 network, and generate .h5 weight file (keras format)
yolo.py					-------   yolo3 network impl with keras
voc.py					--------  process xml annotation file in voc format

data files:
voc.h5				--- pretrained weights with voc data set
yolo.h5				--- converted from yolov3.weights, pretrained weights with coco data set
yolov3-voc_9000.h5   		--- converted from yolov3-voc_9000.weights, trained with voc under darknet
zoo/config_voc.json		--- used by train.py and predict.py as configuration file

voc2012_newtrain.h5 		--- the weight file to be loaded to start/cont train and predict 
				    link to log_voc/voc2012_newtrain.h5
				    to test other h5 for train and predict, simply change this link

log_voc/voc2012_newtrain.h5	--- link to log_voc/epxxxx.h5 a most recent h5

---------1/20/2020 diff among msi, homepc, rose ----------------
	train.py:	initial_epoch = the next epoch number we want to save
	zoo/config_voc.json:
		batch_size=2/8/12
		nb_epoch = the number of epochs to run

---------1/20/2020 test trained_weights_final.h5 from keras-yolo3-another/keras-yolo3----
	initially fail to load_model(), fixed at that package.
		generated box still not the same as that package. 
		possibly the box dimension scale.
		see dog2_here.jpg (detect at this package) and dog2_there.jpg (detect at that package)a
			use the same trained_weights_final.h5
		TBT

---------1/15/2020 code modify ------------------------
clean up output:
	yolo.py , 	comment tf.Print() lines
	generator.py	comment resizing line
			every 10 batch it resize to a different size, why?
	train.py	ModelCheckpoint
			fit_generator verbose=1 to show progress
			each epoch will run 2140 step @batchsize=8, homepc
				8 minutes 
				8563 steps @batchsize=2, msi, 46 minutes!!
				rose batch=12, 1428 steps, 12 minutes

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
		to continue from prev train and save h5 file be numbered accordingly
		        train.py : initial_epoch= next epoch number, 
			config_voc.json:nb_epochs =
			  a number > initial_epoch, otherwise it will skip train

results:
	log_voc2012
	voc2012_newtrain.h5

training performance:
	batchsize prop to loss value. msi batch=2 loss 6 equi to homepc
		batchsize=8 loss 14, @rose batch=12
	msi: batch=2
	tensorboard, loss drop by 25 in 2k, at 70k stall at 10
		the 70k is probably step number, not epoch number
		1/16, loss drop to 7.3486
			each epoch 40 min

	continue train at rose.a
		batch=12, loss start at 17, start from msi epoch 45.
			each epoch 15 min
	continue train at homepc.
			each epoch 7 min
		1/15 batch=8, loss 25 in 40k
		1/16 loss drop to 15.03
		1/17 loss drop to 11.8, mAP: 0.6318 ep092-loss11.635.h5
		1/17 training another 100 epoch, ep1xx-loss....h5
		1/18 100 epoch, mAP: 0.6172, ep2088-loss9.125.h5
		1/18 100 epoch, mAP: 0.6139, ep400-loss8.517.h5
		1/20 lr=1e-4, start from ep402-loss8.373.h5,
			ep404-loss15.096.h5
			ep500-loss12.357.h5
evaluate:	mAP
	full set: ---- config_voc.json---"valid"---"cache_name":           "voc_train.pkl"
:	valid set: --- config_voc.json---"valid"---"cache_name":           "voc_valid.pkl"
	to make evaluate work with voc2012, the val_image and val_ann folder are created
	(1) generate the valid list of file from the train cmd, the modified train cmd will
		automatically generate valid_list.txt which contain the list of filename for valid.
        (2) run
	    python create_valid.py
		to create symbal link inside val_image and val_ann that point to the actual file
		results: media/student/voc2012/VOCdevkit/VOC2012/val_ann/2012_004300.xml and more 
	(3) run
		python3 evaluate.py -c zoo/config_voc.json
		  eval file list frist come from cache .pkl file
		  if no cache, then come from the ann_dir specified in config file's valid section
		  train data set: VOC2012/JPEGImages/ 17125 files, 
		  valid data set: VOC2012/val_image/  4700 files.
	
		ep402-loss8.373.h5: (homepc)
			against val data set  , mAP: 0.6072
			against train data set, mAP: 0.89072

		ep500-loss12.357.h5: (homepc)
			against val data set  , mAP: 0.8830

		voc2012_newtrain.h5:
			mAP: 0.4640
			mAP_voc2012_msi_rst.txt
		voc.h5:
			against train data set, mAP: 0.8943
			against valid data set, mAP: 0.894
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

----------checkpoint issues bugs ------------------
when using checkpoint3, the saved .h5 not work with predict.py,
	size a little smaller than voc.h5 (the stocked one)
	comment off save_weight_only=True result in 700 mb h5 file, still not work
	with predict.py
go back to checkpoint (CustomizedCheckpoint) to see it if is right.

	correct h5:
	voc.h5				247378264	
	voc2012/voc2012_newtrain.h5	247383344
	ep402-loss8.373.h5		247383344 (start from ep400-loss8.517.h5, save model with checkpoint)
	
	incorrect h5 (saved from checkpoint3):	
	ep400-loss8.517.h5		247273184 (homepc)

resolved: use checkpoint

-----------predict test detect on a image---------------
test with local trained ep079-loss5.444.h5  (msi)
	result box ok.

test with  trained_weights_final.h5 from keras-yolo3-another/keras-yolo3
	fail to load
	fixed 1/20/2020 by save correct model during keras-yolo3-another/keras-yolo3/train.py
	the saved model and weight in this package is infer_model, not train_model, which is correct
		see readme.txt there

test with pretrained voc.h5 
	download voc.h5
	python3 predict.py -c zoo/config_voc.json -i dog2.jpg 
	eog output/dog2.jpg 
	result box good

test with pretrained yolov3-voc_9000.h5 
	result box not good. but the same .h5 tested in code1/keras-yolo3-another/keras-yolo3
	looks good. the original yolov3-voc_9000.weights tested in darknet also as godd as 
	code1/keras-yolo3-another/keras-yolo3, could be a drawing issue

test with pretrained yolo.h5 
	result box not good, might coz yolo.h5 is from yolov3.weights trained with coco

test with backend.h5 result in bad box
	1/19/2020 new h5 file load fail with predict.py, anything to do with the use of
	different checkpoint?

test with yolo3.weights directly
	python3 yolo3_one_file_to_detect_them_all.py -w yolov3.weights -i dog2.jpg
	loading weights layer by layer very slow. output good.
	output dog2_detected.jpg
