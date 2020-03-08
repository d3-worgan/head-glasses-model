import os
import argparse


# Traverses each sub directory and file and writes the path of each .jpg image to 
# a text file (target)

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--directory", required=True, help="Path to base directory")
parser.add_argument("-t", "--target", required=True, help="Name of file to write paths")
args = vars(parser.parse_args())

assert os.path.exists(args["directory"]), "Path to base directory is invalid"
assert "." in args["target"], "Specify a txt file name like, hello.txt"
assert args["target"].split(".")[1] == "txt"

print("Writing jpg paths from " + args["directory"] + " to " + args["target"])
with open(args["target"], 'w+') as t:
    for dirpath, dirnames, files in os.walk(args["directory"]):
        for file_name in files:
            file_path = os.path.join(dirpath, file_name)
            if ".jpg" in file_path:
                print(os.path.join(dirpath, file_name))
                t.write(os.path.join(dirpath, file_name)+"\n")
