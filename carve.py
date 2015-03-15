
'''
Jason Dale
'''


import sys
import string
import os

JPEG_HEADER = b'\xff\xd8'
JPEG_FOOTER = b'\xff\xd9'
MAX_OFFSET = 1024*40

def carve(filename):
  count = 0  #used to name output files uniquely
  fd = None  #initialize file descriptor

  # catch exception on reading file
  try:
    filesize = os.path.getsize(filename)
    fd = open(filename,'rb')
  except:
    print("Error opening file:", sys.exc_info()[0])
    sys.exit()

  # start at the top of the file and read in first two bytes
  offset = 0
  data=fd.read(2)
  headers = []
  footers = []
  # loop until we reach the end of the file
  while(offset < filesize):
    if(data == JPEG_HEADER):
      headers.append(offset)
    elif(data == JPEG_FOOTER):
      footers.append(offset)

    offset += 1
    fd.seek(offset)
    data = fd.read(2)

  for h in headers:
    for f in footers:
      if h > f:
        output = open("%d.jpg"%count, "wb")
        fd.seek(h)
        output.write(fd.read((h-f) + 2))
        count +=1

def main():
  carve(sys.argv[1])

if __name__=="__main__":
  main()