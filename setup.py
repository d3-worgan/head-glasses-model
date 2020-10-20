import os
import subprocess


"""
git clone https://github.com/AlexeyAB/Yolo_mark.git
cd Yolo_mark
cmake .
make
cd ..
```
"""
subprocess.run(['git', 'clone', 'https://github.com/AlexeyAB/Yolo_mark.git'])
os.chdir('Yolo_mark')
subprocess.run(['cmake', '.'])
subprocess.run('make')
os.chdir('../')


"""
2. Download the OpenImages label and meta-data
```
wget https://storage.googleapis.com/openimages/v5/class-descriptions-boxable.csv
wget https://storage.googleapis.com/openimages/v6/oidv6-train-annotations-bbox.csv
wget https://storage.googleapis.com/openimages/v5/validation-annotations-bbox.csv
wget https://storage.googleapis.com/openimages/v5/test-annotations-bbox.csv
```
"""
subprocess.run(['wget', 'https://storage.googleapis.com/openimages/v5/class-descriptions-boxable.csv'])
subprocess.run(['wget', 'https://storage.googleapis.com/openimages/v6/oidv6-train-annotations-bbox.csv'])
subprocess.run(['wget', 'https://storage.googleapis.com/openimages/v5/validation-annotations-bbox.csv'])
subprocess.run(['wget', 'https://storage.googleapis.com/openimages/v5/test-annotations-bbox.csv'])