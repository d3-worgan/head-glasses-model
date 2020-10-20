# OpenImages dataset pipeline
This repo can be used to create custom object detection datasets for YOLO. It uses the OpenImages dataset to grab initial data we need. Unfortunatly the quality of OI is not the best and so manual annotation is required which is processed using Yolo Mark. Finally, once the dataset is clean and correct we can train the model in a darknet docker container either locally or in the cloud.


## Install (Linux)
1. First clone the repository
```
git clone https://github.com/d3-worgan/head-glasses-model.git
cd head-glasses-model
```

2. Setup a python enviornment, preferably with conda e.g.
```
conda create -y -n oi_model python=3.6
conda activate oi_model
pip install tqdm
pip install awscli
```
2. Then run the setup script to download the OpenImages labels, meta-data and the Yolo_mark editor
```
python setup.py
git clone https://github.com/AlexeyAB/Yolo_mark.git
cd Yolo_mark
cmake .
make
cd ..
```


2. Download the OpenImages label and meta-data
```
wget https://storage.googleapis.com/openimages/v5/class-descriptions-boxable.csv
wget https://storage.googleapis.com/openimages/v6/oidv6-train-annotations-bbox.csv
wget https://storage.googleapis.com/openimages/v5/validation-annotations-bbox.csv
wget https://storage.googleapis.com/openimages/v5/test-annotations-bbox.csv
```

## Usage
### 1. Download the initial dataset
1. Selecting from the list in the ```class-descriptions-boxable.csv```, specify the class names to download in the ```classes.txt``` file. The classes.txt should contain an example to overwrite. E.g. ```classes.txt```:
```
Human head
Glasses
```

2. Then run a command like:
```
python pull-dataset.py --mode train --classes.txt
```

To limit the number of data use the ```--max_annotations``` to restrict how much data for each class
```
python pull-dataset.py --mode train --classes.txt --max_annotations 10
```

Pull dataset also has options for selecting more specific data e.g. 
```
python pull-dataset.py --mode train --classes.txt --max_annotations 10 --occluded
```
This will include examples where the object is occluded, see --help for more options.


### 2. Validate and fix the annotations
OpenImages is partly produced by automation and so in much of the cases the labels are poor or missing. For this reason we still need to manually go through the data set and fix the labels.

1. Run this to load the dataset into the Yolo_mark bounding box editor
```
rm x64/Release/data/img/*
mv train/* Yolo_mark/x64/Release/data/img/
cp classes.txt Yolo_mark/x64/Release/data/obj.names
```

2. Then run Yolo_mark and go through each  image and fix them
```
cd Yolo_mark
sh linux_mark.sh
```

3. When the labels are finished move the data back to root directory
```
mv x64/Release/data/img/* ../train/
```

### 3. Repeat steps 1 and 2 for the validation and test sets (if required)

### 4. Now we can train a detection model using darknet
