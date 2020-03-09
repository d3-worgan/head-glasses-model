import os
import argparse

# Traverse the folders
# Walking a directory tree and printing the names of the directories and files
# If a txt file is found then replace class names inside with class index

parser = argparse.ArgumentParser(description='Traverse directory of training data and replace class names with relevant index')
parser.add_argument("-c", "--classes", required=True, help="Specify a path to the class names file")
parser.add_argument("-d", "--location", required=True, help="Specify a path to the base directory to traverse")

args = vars(parser.parse_args())

# Load the class names
classes = []
with open(args["classes"], 'r+') as f:
    for line in f:
        line = line.rstrip('\n')
        classes.append(line)
for c in classes:
    print(c)

print("Fixing annotations for ")
# Traverse and replace names
for dirpath, dirnames, files in os.walk(args["location"]):
    print(f'Directory: {dirpath}')
    for file_name in files:
        file_path = os.path.join(dirpath, file_name)
        if '.txt' in file_path:
            #print(file_path)

            # Read info from file
            fin =  open(file_path, 'rt')
            data = fin.read()
            fin.close()

            # Read and extract the class name from the file
            fin =  open(file_path, 'rt')
            line = fin.readline()
            line = line.rstrip('\n')
            #print(line)
            split = line.split(",")

            # Replace class names with indexes
            data = data.replace(split[0], str(classes.index(split[0])))
            #print(split[0] + " is index " + str(classes.index(split[0])) + " in classes.txt")
            fin.close()

            # Overwrite file
            fin = open(file_path, 'wt')
            fin.write(data)
            fin.close()
