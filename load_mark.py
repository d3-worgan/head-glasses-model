import os
import argparse


parser = argparse.ArgumentParser(description='Download Class specific images from OpenImagesV4')
parser.add_argument("--source", help="Which set of data to load into Yolo_mark. E.g. train, validation, test", required=True)
args = parser.parse_args()
source = args.source

print(f"Loading Yolo_mark with {source}")
root_d = os.getcwd()
print(f"cwd is {root_d}")

source_d = os.path.join(root_d, source)
print(f"Target data location {source_d}")

ymark_d = os.path.join(root_d, 'Yolo_mark', 'x64', 'Release', 'data', 'img')
print(f"img dir is {ymark_d}")


# First clear the Yolo_mark directory
f_img_dir = next(os.walk(ymark_d))[2]
print(f"files is {f_img_dir}")
for f in f_img_dir:
    print(f)
    os.remove(os.path.join(ymark_d, f))

# Then copy the specified data into Yolo_mark
f_source_d = next(os.walk(source_d))[2]
for f in f_source_d:
    print(f)
    os.rename(os.path.join(source_d, f), os.path.join(ymark_d, f))

# Fix the .names file with the correct names


"""
rm x64/Release/data/img/*
mv train/* Yolo_mark/x64/Release/data/img/
cp classes.txt Yolo_mark/x64/Release/data/obj.names
sed -i "s/\(num_lines_in_file_1 = \)100/\1$(wc -l < file1.txt)/" file2.txt
"""