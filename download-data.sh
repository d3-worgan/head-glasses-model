export PATH="/home/danielworgan91/.local/bin":$PATH
echo 'export PATH="/home/danielworgan91/.local/bin":$PATH' >> ~/.bashrc

# Download data from the open images dataset

# Set up python pip
sudo curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo apt-get install python3-distutils
python3 get-pip.py

pip install tqdm
pip install awscli

wget https://storage.googleapis.com/openimages/2018_04/class-descriptions-boxable.csv
wget https://storage.googleapis.com/openimages/2018_04/train/train-annotations-bbox.csv
wget https://storage.googleapis.com/openimages/2018_04/validation/validation-annotations-bbox.csv
wget https://storage.googleapis.com/openimages/2018_04/test/test-annotations-bbox.csv

# Make sure classes .txt has correct classes
python3 download-multi.py --mode test --classes classes.txt
python3 download-multi.py --mode train --classes classes.txt

python3 fix-yolo-annotations.py --classes classes.txt --location test
python3 fix-yolo-annotations.py --classes classes.txt --location train




