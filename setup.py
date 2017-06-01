import os
import sys
from shutil import copyfile

if __name__ == "__main__":
    if not os.path.isfile("./FSGDP.py"):
        print ("No valid FSGDP.py file found!")
        exit()
    print ("Copying files...")
    try:
        version = str(sys.version[:3])
        path = "/usr/lib/python" + version
        copyfile("./FSGDP.py", path + "/FSGDP.py")
        print ("Finished installing to " + path + "!")
    except IOError:
        print ("Didn't work, maybe you need to run this as Administrator")
