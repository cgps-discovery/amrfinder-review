import os
import shutil

# specify the directory you want to move files from
source_dir = 'organisms/'
# specify the directory you want to move files to
dest_dir = 'testing_ori'
if not os.path.exists(dest_dir): 
    os.mkdir(dest_dir)

for taxid in os.listdir(source_dir):
    source = os.path.join(source_dir, taxid, 'amrfinder.csv')
    # rename the file
    destination = os.path.join(dest_dir, f'amrfinder-{taxid}.csv')
    if os.path.exists(source):
        # move the file to the new directory
        shutil.copy(source, destination)