import os
import argparse
import shutil

parser = argparse.ArgumentParser(description='Load data into the Yolo_mark annotation editor')
parser.add_argument("--mode", help="Which set of data to load into Yolo_mark. E.g. train, validation, test", required=True)
args = parser.parse_args()
run_mode = args.mode

print(f"Loading Yolo_mark with {run_mode}")
root_d = os.getcwd()
print(f"cwd is {root_d}")

source_d = os.path.join(root_d, 'dataset', run_mode)
print(f"Target data location {source_d}")
assert os.path.exists(source_d), f"There is no data for the {run_mode} set in /open_images."

ymark_d = os.path.join(root_d, 'Yolo_mark', 'x64', 'Release', 'data')
ymark_img_d = os.path.join(ymark_d, 'img')
print(f"img dir is {ymark_img_d}")
assert os.path.exists(ymark_img_d), f"{ymark_img_d} is invalid, install the yolo mark."
# First clear the Yolo_mark directory
f_img_dir = next(os.walk(ymark_img_d))[2]
for f in f_img_dir:
    os.remove(os.path.join(ymark_img_d, f))
assert len(next(os.walk(ymark_img_d))[2]) == 0, f"The yolo_mark image directory should be empty"

# Then copy the specified data into Yolo_mark
f_source_d = next(os.walk(source_d))[2]
for f in f_source_d:
    shutil.move(os.path.join(source_d, f), os.path.join(ymark_img_d, f))

# Fix the .names file with the correct names
shutil.copy(os.path.join(root_d, 'classes.txt'), os.path.join(ymark_d, 'obj.names'))
