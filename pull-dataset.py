import argparse
import csv
import subprocess
import os
from tqdm import tqdm
import multiprocessing
from multiprocessing import Pool as thread_pool


# Finds and downloads specifed classes from open images dataset 
cpu_count = multiprocessing.cpu_count()

parser = argparse.ArgumentParser(description='Download Class specific images from OpenImagesV4')
parser.add_argument("--mode", help="Dataset category - train, validation or test", required=True)
parser.add_argument("--classes", help="Specify names like cat,dog, or specify a .txt file with class names", required=True)
parser.add_argument("--max_annotations", help="Specify a max number of annotations for each class", required=False, type=int, default=10)
parser.add_argument("--csv", help="Location of the class-descriptions-boxable.csv", required=False, type=str, default='./class-descriptions-boxable.csv')
parser.add_argument("--nthreads", help="Number of threads to use", required=False, type=int, default=cpu_count*2)
parser.add_argument("--occluded", help="Include occluded images", required=False, type=int, default=1)
parser.add_argument("--truncated", help="Include truncated images", required=False, type=int, default=1)
parser.add_argument("--groupOf", help="Include groupOf images", required=False, type=int, default=1)
parser.add_argument("--depiction", help="Include depiction images", required=False, type=int, default=1)
parser.add_argument("--inside", help="Include inside images", required=False, type=int, default=1)

args = parser.parse_args()

run_mode = args.mode
threads = args.nthreads
class_descriptions = args.csv
max_annotations = args.max_annotations

print(f"Threads used {threads}")

# Load the names of the requested classes
classes = []
if "." in args.classes:
    # Load from specified txt file
    if args.classes.split(".")[1] == "txt":
        with open(args.classes) as f:
            for name in f:
                classes.append(name.rstrip())
else:
    # Load names from args
    for class_name in args.classes.split(','):
        classes.append(class_name)

print("Classes to search for:")
for name in classes:
    print(name)

print("Loading class download labels")
# Load the class descriptions
with open(class_descriptions, mode='r') as infile:
    reader = csv.reader(infile)
    download_labels = {rows[1]:rows[0] for rows in reader}

subprocess.run(['rm', '-rf', run_mode])
subprocess.run([ 'mkdir', run_mode])

pool = thread_pool(threads)
commands = []
num_annotations = 0

# Iterate class names specified by the user
for ind in range(0, len(classes)):
    class_name = classes[ind]
    print(f"Class {ind}: {class_name}")
        
    # Grab each label from the annotations file for the current class
    command = f"grep {download_labels[class_name.replace('_', ' ')]} ./{run_mode}-annotations-bbox.csv"
    print(command)
    class_annotations = subprocess.run(command.split(), stdout=subprocess.PIPE).stdout.decode('utf-8')
    class_annotations = class_annotations.splitlines()
    print(f"{len(class_annotations)} for {class_name}")

    for i in range(max_annotations):
        annotation = class_annotations[i].split(',')
        
        #IsOccluded,IsTruncated,IsGroupOf,IsDepiction,IsInside
        if (args.occluded==0 and int(annotation[8])>0):
            print("Skipped %s",annotation[0])
            continue
        if (args.truncated==0 and int(annotation[9])>0):
            print("Skipped %s",annotation[0])
            continue
        if (args.groupOf==0 and int(annotation[10])>0):
            print("Skipped %s",annotation[0])
            continue
        if (args.depiction==0 and int(annotation[11])>0):
            print("Skipped %s",annotation[0])
            continue
        if (args.inside==0 and int(annotation[12])>0):
            print("Skipped %s",annotation[0])
            continue

        num_annotations = num_annotations + 1

        # Add the image to the list of images to download later
        command = f"aws s3 --no-sign-request --only-show-errors cp s3://open-images-dataset/{run_mode}/{annotation[0]}.jpg {run_mode}/{annotation[0]}.jpg"
        if command not in commands:
            commands.append(command)
        
        # Append the annotation to the corresponding image label
        with open(f'{run_mode}/{annotation[0]}.txt', 'a') as f:
            f.writelines(f"{ind} {(float(annotation[5]) + float(annotation[4]))/2} {((float(annotation[7]) + float(annotation[6])) / 2)} {float(annotation[5]) - float(annotation[4])} {float(annotation[7]) - float(annotation[6])}\n")

        if i == len(class_annotations):
            break

print(f"Annotation Count: {num_annotations}")
commands = list(set(commands))
print("Number of images to be downloaded : " + str(len(commands)))

list(tqdm(pool.imap(os.system, commands), total = len(commands) ))

pool.close()
pool.join()
