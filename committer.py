#!/usr/bin/python3
import sys, getopt, datetime, subprocess
import numpy as np
from scipy.misc import imread

def print_help():
    print("committer.py -i <image-file> -d <start-date>")
    print("  > start date")
    print("     date format: %Y-%m-%d")
    print("     pick the date in the upper left corner of the graph (take that from previous year if neccessary)")
    print("  > image file")
    print("     use relative path to image file")
    print("     image should have 7(H)x54(W) pixels, commits appear on black pixels")


def commitcnt2str(ccnt):
    return "#" if ccnt > 0 else "-"


def commit_count(px):
    return 0 if px > 0 else 1


def print_image(img):
    for line in img:
        print("".join([commitcnt2str(commit_count(px)) for px in line]))


def main(argv):
    imgfile = None
    start_date = None

    try:
        opts, args = getopt.getopt(argv, "hi:d:", ["image-file=", "start-date"])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print_help()
        elif opt in ("-i", "--image-file"):
            imgfile = arg
        elif opt in ("-d", "--start-date"):
            start_date = datetime.datetime.strptime(arg+' 12:00 +0100', '%Y-%m-%d %H:%M %z')

    print("Taking image {} to create commits starting at {}".format(imgfile, start_date))


    img = imread(imgfile, flatten=True)
    imgnp = np.array(img)
    print("Image:")
    #print(imgnp.T)
    print_image(img)
    
    run_date = start_date
    for col in imgnp.T:
        for px in col:
            ccnt = commit_count(px)
            for run in range(ccnt):
                # touch a file for commit
                with open("pfeil", "a") as f:
                    f.write(".")

                # git add the file
                subprocess.call("git add pfeil", shell=True)
                # git commit the file
                subprocess.call("git commit -m {} --date=\"{}\"".format(run_date.__format__('%Y-%m-%d') + str(run),
                                                                        run_date.__format__('%a %b %d %H:%M %Y %z')), shell=True)

            # move to next day
            run_date += datetime.timedelta(days=1)


if __name__ == "__main__":
    main(sys.argv[1:])
