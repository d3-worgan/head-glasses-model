import os
import argparse
import shutil

parser = argparse.ArgumentParser(description='Load data into the Yolo_mark annotation editor')
parser.add_argument("--source", help="Which set of data to load into Yolo_mark. E.g. train, validation, test", required=True)
args = parser.parse_args()
source = args.source

print(f"Loading Yolo_mark with {source}")
root_d = os.getcwd()
print(f"cwd is {root_d}")

source_d = os.path.join(root_d, 'dataset', source)
print(f"Target data location {source_d}")

ymark_d = os.path.join(root_d, 'Yolo_mark', 'x64', 'Release', 'data')
ymark_img_d = os.path.join(ymark_d, 'img')
print(f"img dir is {ymark_img_d}")

# First clear the Yolo_mark directory
f_img_dir = next(os.walk(ymark_img_d))[2]
print(f"files is {f_img_dir}")
for f in f_img_dir:
    print(f)
    os.remove(os.path.join(ymark_img_d, f))

# Then copy the specified data into Yolo_mark
f_source_d = next(os.walk(source_d))[2]
for f in f_source_d:
    print(f)
    shutil.move(os.path.join(source_d, f), os.path.join(ymark_img_d, f))

# Fix the .names file with the correct names
shutil.copy(os.path.join(root_d, 'classes.txt'), os.path.join(ymark_d, 'obj.names'))