import os
import subprocess
import shutil


# Get the desired name from user or default to dataset_final
datasetname = "custom_dataset"
names_file = f"{datasetname}.names"
config_file = f"{datasetname}.cfg"
data_file = f"{datasetname}.data"

# Find key directories
root_directory = os.getcwd()
yolo_mark_data = os.path.join(root_directory, 'Yolo_mark', 'x64', 'Release', 'data')
dataset_directory = os.path.join(root_directory, 'dataset')
assert os.path.exists(yolo_mark_data), f"{yolo_mark_data} invalid path"
assert os.path.exists(dataset_directory), f"Invalid path to the dataset directory"

# Copy template config files to dataset e.g. yolov4.cfg & .names file
shutil.copy(os.path.join(yolo_mark_data, 'obj.names'), os.path.join(dataset_directory, names_file))
assert os.path.exists(os.path.join(dataset_directory, names_file))

os.chdir('dataset')
subprocess.run(['wget', 'https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4.cfg'])
shutil.move(os.path.join(dataset_directory, 'yolov4.cfg'), os.path.join(dataset_directory, config_file))
assert os.path.exists(os.path.join(dataset_directory, config_file))

subprocess.run(['wget', 'https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/coco.data'])
shutil.move(os.path.join(dataset_directory, 'coco.data'), os.path.join(dataset_directory, data_file))
assert os.path.exists(os.path.join(dataset_directory, data_file))

# Figure out some standard parameters for training the dataset (see https://github.com/AlexeyAB/darknet#how-to-train-to-detect-your-custom-objects)
num_classes = len(open(os.path.join(dataset_directory, names_file)).readlines())
max_batches = num_classes * 2000
number_of_images = len(next(os.walk(os.path.join(dataset_directory, 'train')))[2]) / 2
if number_of_images > max_batches:
    max_batches = number_of_images
linestep1 = max_batches * 0.8
linestep2 = max_batches * 0.9
filters = (num_classes + 5) * 3

# search through the config and adjust the parameters
with open(config_file, 'r') as file:
  filedata = file.read()
# filedata = filedata.replace('batch=64', 'batch=64')
filedata = filedata.replace('subdivision=8', 'subdivisions=16')
filedata = filedata.replace('max_batches = 500200', f'max_batches = {max_batches}')
filedata = filedata.replace('steps=400000,450000', f'steps={linestep1},{linestep2}')
filedata = filedata.replace('classes=80', f'classes={num_classes}')
filedata = filedata.replace('filters=255', f'filters={filters}')
with open(config_file, 'w') as file:
  file.write(filedata)

# fix the paths to work if the dataset is copied into the darknet/datasets/datasetname directory
with open(data_file, 'r') as file:
  filedata = file.read()
filedata = filedata.replace('classes= 80', f'classes={num_classes}')
filedata = filedata.replace('names = data/coco.names', f'names = datasets/{datasetname}/{names_file}')
filedata = filedata.replace('train  = /home/pjreddie/data/coco/trainvalno5k.txt', f'train  = datasets/{datasetname}/train_paths.txt')
filedata = filedata.replace('valid  = coco_testdev', f'valid = datasets/{datasetname}/validation_paths.txt')
with open(data_file, 'w') as file:
  file.write(filedata)

# Maybe generate the image path files for train and test here unless we need to specify absolute paths
# in which case we need to generate in the final training location.