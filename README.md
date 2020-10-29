# OpenImages & Yolo dataset pipeline
Create custom object detection datasets for [YOLO](https://github.com/AlexeyAB/darknet) using the [OpenImages](https://storage.googleapis.com/openimages/web/download.html) dataset and [Yolo_mark](https://github.com/AlexeyAB/Yolo_mark) bounding box editor.


## Install (Linux)
1. First clone this repository
```
git clone https://github.com/d3-worgan/oi-dataset-pipe.git
cd oi-dataset-pipe
```

2. Setup a python environment, preferably with conda e.g.
```
conda create -y -n oi_model python=3.6
conda activate oi_model
pip install tqdm
pip install awscli
```

3. Then run the setup script to download the OpenImages labels, meta-data and the Yolo_mark editor
```
python setup.py
```

## Usage
### 1. Download the initial dataset
1. Selecting from the list in the ```class-descriptions-boxable.csv```, specify the class names to download in 
the ```classes.txt``` file. E.g. 
```classes.txt```:
```
Human head
Glasses
```

2. Then download the images and corresponding annotations by running a command like:
```
python pull-dataset.py --mode train --classes classes.txt
```

Limit the number of annotations and images to download using the ```--max_annotations``` option. 
```
python pull-dataset.py --mode train --classes.txt --max_annotations 10
```

Pull dataset also has options for selecting more specific data from OpenImages e.g. (see --help for more info)
```
python pull-dataset.py --mode train --classes.txt --max_annotations 10 --occluded
```


### 2. Validate and fix the annotations
OpenImages is partly produced by automation and so in much of the cases the labels are poor or missing. 
For this reason we need to manually go through the data set and fix / add the labels if necessary.

1. Load the data we just downloaded into Yolo_mark
```
python load_mark.py --mode train
```

2. Then run Yolo_mark and go through each  image and fix them
```
cd Yolo_mark
sh linux_mark.sh
```

3. When the labels are finished move the data back to root directory
```
mv x64/Release/data/img/* ../dataset/train/
```

### 3. Repeat steps 1 and 2 for the validation and test sets (if required)
E.g.
```
cd ../
python pull-dataset.py --mode validation --classes classes.txt
python load_mark.py --mode validation
cd Yolo_mark
sh linux_mark.sh
mv x64/Release/data/img/* ../dataset/validation/

cd ../
python pull-dataset.py --mode test --classes classes.txt
python load_mark.py --mode test
cd Yolo_mark
sh linux_mark.sh
mv x64/Release/data/img/* ../dataset/test/
```

### 4. Finalise the dataset and prepare for training with darknet
Now that we have the data and the labels have been validated, we can finalise that 
dataset and generate a standard configuration for training with yolo.

```
cd ../
python finalise.py --name mydataset
```

The mydataset directory can now be passed to Darknet for training a custom model.
