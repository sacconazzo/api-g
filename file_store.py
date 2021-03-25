
import shutil
import os


def main():
    source = "/volumeUSB1/usbshare"
    dest1 = "/volume2/video"
    
    files = os.listdir(source)

    for f in files:
        print(files)
        shutil.move(source+'/'+f, dest1+'/'+f)


if __name__ == "__main__":
    main()
