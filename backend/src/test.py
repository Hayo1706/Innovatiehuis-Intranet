import os

source_path = ".\endpoints"

for root, dirs, files in os.walk(source_path, topdown=True):
    dir = root.replace(source_path, "")
    for name in files:
        print(os.path.join(dir, name))
    for name in dirs:
        print(os.path.join(dir, name))