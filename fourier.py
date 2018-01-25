#!/usr/bin/python
 
import cv2
import sys
import time
import numpy as np
from optparse import OptionParser
from matplotlib import pyplot as plt

if __name__ == '__main__':
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)

    parser.add_option("-i", "--input",type="string", dest="input", help="import image to IMG", metavar="IMG_I")
    parser.add_option("-o", "--output", type="string", dest="output", help="export transform to specified file name", default='out.jpg')
    (options, args) = parser.parse_args()

    if options.input:
      try:
        img = cv2.imread(options.input,0)
        img_orig = img.copy();
      except AttributeError:
        print("[ERROR] .jpg file not found in root directory.")
        sys.exit(0)
    if options.output:
      img_out = options.output
    else:
      img_out = "out.jpg"

    dft = cv2.dft(np.float32(img), flags = cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)
    magnitude_spectrum = 20*np.log(cv2.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))

    plt.subplot(111),plt.imshow(magnitude_spectrum, cmap = 'gray')
    plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
    plt.show()
    cv2.waitKey(0)