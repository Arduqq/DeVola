#!/usr/bin/python
 
import cv2
import sys
import time
import numpy as np
from clint.textui import progress, puts, colored
from optparse import OptionParser
from matplotlib import pyplot as plt

def draw_blob(img, points, colors):
  with progress.Bar(label="splatting", expected_size=len(points)) as bar:
    val = 0
    for p,c in zip(points,colors):
      cv2.circle(img, p, np.random.randint(1,2), c, -1, cv2.LINE_AA, 0)
      val += 1
      bar.show(val)

def draw_voronoi(img, subdiv, colors):
  (facets, centers) = subdiv.getVoronoiFacetList([])
  with progress.Bar(label="voronoi  ", expected_size=len(facets)) as bar:
    for i in xrange(0,len(facets)):
      ifacet_arr = []
      for f in facets[i]:
        ifacet_arr.append(f)
           
      ifacet = np.array(ifacet_arr, np.int)
      color = (colors[i][0], colors[i][1], colors[i][2])
      cv2.fillConvexPoly(img, ifacet, color, cv2.LINE_AA, 0);
      ifacets = np.array([ifacet])
      # cv2.polylines(img, ifacets, True, (0, 0, 0), 0, cv2.LINE_AA, 0)
      cv2.circle(img, (centers[i][0], centers[i][1]), 0, (0, 0, 0), -1, cv2.LINE_AA, 0)
      bar.show(i+1)
 

if __name__ == '__main__':
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)

    parser.add_option("-i", "--input",type="string", dest="input", help="import image to IMG", metavar="IMG_I")
    parser.add_option("-c", "--coords",type="string", dest="coords", help="import coordinates from .txt", metavar="TXT_I")
    parser.add_option("-o", "--output", type="string", dest="output", help="export diagram to specified file name", default='out.jpg')
    (options, args) = parser.parse_args()

    if options.input:
      try:
        img = cv2.imread(options.input)
        img_orig = img.copy();
      except AttributeError:
        print("[ERROR] .jpg file not found in root directory.")
        sys.exit(0)
    if options.output:
      img_out = options.output
    else:
      img_out = "out.jpg"
    if options.coords:
      coords = options.coords
    else:
      coords = 'points.txt'

    start = time.time()
    # Define window names
    win_blob = "Splatfest"
    
    size = img.shape
    rect = (0, 0, size[1], size[0])
    subdiv = cv2.Subdiv2D(rect)
     
    # Rectangle to be used with Subdiv2D
    size = img.shape
    rect = (0, 0, size[1], size[0])
    # Create an array of points.
    points = []
    colors = []
     
    # Read in the points from a text file
    try:
      puts("Reading coordinates")
      with open(coords) as file :
        for line in file:
          x, y, r, g, b = (line.split() + [None]*99)[:5]
          points.append((int(x), int(y)))
          colors.append((int(r), int(g), int(b)))
    except IOError:
      print(".txt file not found in root directory.")
      sys.exit(0)
    except TypeError:
      print(".txt might be invalid.")
      print("x-coordinate] [y-coordinate] [red-value] [green-value] [blue-value]")
      sys.exit(0)
 
    animate = False
    # Insert points into subdiv
    img_blob = np.zeros(img.shape, dtype = img.dtype)
    with progress.Bar(label="subdiv   ", expected_size=len(points)) as bar:
      val = 1
      for p in points:
        subdiv.insert(p)
        if animate:
          img_copy = img_blob.copy()
          draw_blob(img_copy, points, colors)
          cv2.imshow(win_blob, img_copy)
          cv2.waitKey(2)
        bar.show(val)
        val += 1

    smoothing = False
    median = False
    fastDenoise =False
    shrink = False

    start_v = time.time()
    
    draw_voronoi(img_blob,subdiv,colors)
    draw_blob(img_blob,points,colors)
 
    # Show results
    if smoothing:
      img_blob = cv2.bilateralFilter(img_blob,9,75,75)
    if fastDenoise:
      img_blob = cv2.fastNlMeansDenoisingColored(img_blob,None,10,10,7,21)
    if median:
      img_blob = cv2.medianBlur(img_blob,21)
    if shrink:
      img_blob = cv2.resize(img_blob, (0,0), fx=0.5, fy=0.5, interpolation = cv2.INTER_AREA)
    cv2.imwrite(img_out,img_blob)
    end = time.time()
    # cv2.imshow(win_blob,img_blob)
    # cv2.waitKey(0)
    puts("[" + colored.green("SUCCESS") + "] Image saved as " + img_out)