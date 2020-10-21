import os
import subprocess
import shutil
import argparse

"""
Prepares the dataset for training in darknet. Produces some basic configuration files.
"""

parser = argparse.ArgumentParser()
parser.add_argument("--name", default="dataset", help="Option to name the dataset")
args = parser.parse_args()

# Get the desired name from user or default to dataset_final
datasetname = args.name
print(f"Finalising {datasetname} dataset")
names_file = f"{datasetname}.names"
config_file = f"{datasetname}.cfg"
data_file = f"{datasetname}.data"

# Find key directories
root_directory = os.getcwd()
assert os.path.exists(os.path.join(root_directory, 'dataset')), f'There is no "dataset" directory to finalise. ' \
                                                                f'Download data first, or have you changed the ' \
                                                                f'directory name?'
yolo_mark_data = os.path.join(root_directory, 'Yolo_mark', 'x64', 'Release', 'data')
shutil.move(os.path.join(root_directory, 'dataset'), os.path.join(root_directory, datasetname))
dataset_directory = os.path.join(root_directory, datasetname)
assert os.path.exists(yolo_mark_data), f"{yolo_mark_data} invalid path"
assert os.path.exists(dataset_directory), f"Invalid path to the dataset directory"

# clean the directory first in case we are renaming it
dataset_directory_contents = next(os.walk(dataset_directory))[2]
for f in dataset_directory_contents:
    if '.cfg' or '.names' or '.data' in f:
        os.remove(os.path.join(dataset_directory, f))
print(f"Cleaned dataset directory")

# Copy template config files to dataset e.g. yolov4.cfg & .names file
shutil.copy(os.path.join(yolo_mark_data, 'obj.names'), os.path.join(dataset_directory, names_file))
assert os.path.exists(os.path.join(dataset_directory, names_file))

os.chdir(datasetname)
subprocess.run(['wget', 'https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4.cfg'])
shutil.move(os.path.join(dataset_directory, 'yolov4.cfg'), os.path.join(dataset_directory, config_file))
assert os.path.exists(os.path.join(dataset_directory, config_file))

subprocess.run(['wget', 'https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/coco.data'])
shutil.move(os.path.join(dataset_directory, 'coco.data'), os.path.join(dataset_directory, data_file))
assert os.path.exists(os.path.join(dataset_directory, data_file))
print(f"Copied config templates")

# Figure out some standard parameters for training the dataset (see https://github.com/AlexeyAB/darknet#how-to-train-to-detect-your-custom-objects)
num_classes = len(open(os.path.join(dataset_directory, names_file)).readlines())
max_batches = num_classes * 2000
number_of_images = len(next(os.walk(os.path.join(dataset_directory, 'train')))[2]) / 2
if number_of_images > max_batches:
    max_batches = number_of_images
linestep1 = max_batches * 0.8
linestep2 = max_batches * 0.9
filters = (num_classes + 5) * 3

print(f"Generated initial configuration parameters")
print(f"num_classes = {num_classes}")
print(f"num_images  = {number_of_images}")
print(f"max_batches = {max_batches}")
print(f"steps       = {int(linestep1)}, {int(linestep2)}")
print(f"filters     = {filters}")

# search through the config and adjust the parameters
print(f"Modified configuration parameters")
with open(config_file, 'r') as file:
  filedata = file.read()
filedata = filedata.replace('subdivision=8', 'subdivisions=16')
filedata = filedata.replace('max_batches = 500500', f'max_batches = {max_batches}')
filedata = filedata.replace('steps=400000,450000', f'steps={int(linestep1)},{int(linestep2)}')
filedata = filedata.replace('classes=80', f'classes={num_classes}')
filedata = filedata.replace('filters=255', f'filters={filters}')
with open(config_file, 'w') as file:
  file.write(filedata)

# fix the paths to work if the dataset is copied into the darknet/datasets/datasetname directory
print(f"Modifying .data file")
with open(data_file, 'r') as file:
  filedata = file.read()
filedata = filedata.replace('classes= 80', f'classes={num_classes}')
filedata = filedata.replace('names = data/coco.names', f'names = datasets/{datasetname}/{names_file}')
filedata = filedata.replace('train  = /home/pjreddie/data/coco/trainvalno5k.txt', f'train  = datasets/{datasetname}/train_paths.txt')
filedata = filedata.replace('valid  = coco_testdev', f'valid = datasets/{datasetname}/validation_paths.txt')
filedata = filedata.replace('backup = /home/pjreddie/backup/', f'backup = datasets/{datasetname}/backup/.txt')
with open(data_file, 'w') as file:
  file.write(filedata)

# Maybe generate the image path files for train and test here unless we need to specify absolute paths
# in which case we need to generate in the final training location.
print(f"Generating image paths for training")
dataset_directory_contents = next(os.walk(dataset_directory))[1]
if 'train' in dataset_directory_contents:
    with open(os.path.join(root_directory, dataset_directory, 'train_paths.txt'), 'w') as t:
        training_data = next(os.walk(os.path.join(dataset_directory, 'train')))[2]
        for f in training_data:
            if ".jpg" in f:
                t.write(f"{os.path.join('datasets', datasetname, 'train', f)}\n")
if 'validation' in dataset_directory_contents:
    with open(os.path.join(root_directory, dataset_directory, 'validation_paths.txt'), 'w') as t:
        validation_data = next(os.walk(os.path.join(dataset_directory, 'validation')))[2]
        for f in training_data:
            if ".jpg" in f:
                t.write(f"{os.path.join('datasets', datasetname, 'validation', f)}\n")

print("Complete")