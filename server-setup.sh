# Prepare a server for downloading the open images dataset

# Set up python pip
sudo curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo apt-get install python3-distutils
python3 get-pip.py 
sudo nano ~/.bashrc

# Add path to pip 
"/home/danielworgan91/.local/bin"

sudo reboot

# On reboot...
pip install tqdm

cd /home/data-drive/download

pip install awscli

wget https://storage.googleapis.com/openimages/2018_04/class-descriptions-boxable.csv
wget https://storage.googleapis.com/openimages/2018_04/train/train-annotations-bbox.csv
wget https://storage.googleapis.com/openimages/2018_04/validation/validation-annotations-bbox.csv
wget https://storage.googleapis.com/openimages/2018_04/test/test-annotations-bbox.csv

python3 multhithread-downloader.py