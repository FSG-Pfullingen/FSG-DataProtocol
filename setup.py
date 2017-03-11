import os
from shutil import copyfile

if __name__ == "__main__":
    if not os.path.isfile("./FSGDP.py"):
        print "This is not a file!"
        exit()
    print "Copying files..."
    try:
        copyfile("./FSGDP.py", "/usr/lib/python2.7/FSGDP.py")
        print "Finished!"
    except:
        print "Could not copy files! (Maybe you need to run this program as administrator?)"
