#!/usr/bin/python
 
import cv2
import sys
import time
import numpy as np
import random
from optparse import OptionParser
 
# Check if a point is inside a rectangle
def rect_contains(rect, point):
  if point[0] < rect[0] :
    return False
  elif point[1] < rect[1]:
    return False
  elif point[0] > rect[2]:
    return False
  elif point[1] > rect[3]:
    return False
  return True
 
# Draw a point
def draw_point(img, p, color ) :
    cv2.circle( img, p, 0, color, -1, cv2.LINE_AA, 0 )
 
 
 
# Draw voronoi diagram
def draw_voronoi(img, subdiv, colors):
  (facets, centers) = subdiv.getVoronoiFacetList([])
 
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
 
 
if __name__ == '__main__':
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)

    parser.add_option("-i", "--input",type="string", dest="input", help="import image to IMG", metavar="IMG_I")
    parser.add_option("-c", "--coords",type="string", dest="coords", help="import coordinates from .txt", metavar="TXT_I")
    parser.add_option("-o", "--output", type="string", dest="output", help="export diagram to specified file name", default='out.jpg')
    parser.add_option("-s", "--silent", action="store_true", dest="silent", help="no windows")
    (options, args) = parser.parse_args()

    if options.input:
      try:
        # Read in the image.
        img = cv2.imread(options.input)
        # Keep a copy around
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
    win_voronoi = "Voronoi Diagram"

    points_color = (0, 0, 255)
    
     
    # Rectangle to be used with Subdiv2D
    size = img.shape
    rect = (0, 0, size[1], size[0])
     
    # Create an instance of Subdiv2D
    #        an empty Delaunay subdivision
    subdiv = cv2.Subdiv2D(rect)
 
    # Create an array of points.
    points = []
    colors = []
     
    # Read in the points from a text file
    try:
      with open(coords) as file :
        print("Reading coordinates ...")
        for line in file :
          x, y, r, g, b = (line.split() + [None]*99)[:5]
          points.append((int(x), int(y)))
          colors.append((int(r), int(g), int(b)))
        print("Done.")
    except IOError:
      print(".txt file not found in root directory.")
      sys.exit(0)
    except TypeError:
      print(".txt might be invalid.")
      print("x-coordinate] [y-coordinate] [red-value] [green-value] [blue-value]")
      sys.exit(0)
 
    animate = False
    # Insert points into subdiv
    print("Processing points ...")
    img_voronoi = np.zeros(img.shape, dtype = img.dtype)
    for p in points :
      subdiv.insert(p)
      # Show animation
      if animate :
        img_copy = img_voronoi.copy()
        # Draw delaunay triangles
        draw_voronoi(img_copy, subdiv, colors)
        cv2.imshow(win_voronoi, img_copy)
        cv2.waitKey(2)
    print("Done.")

    # Draw Voronoi diagram
    print("Drawing voronoi diagram ...")
    start_v = time.time()
    draw_voronoi(img_voronoi,subdiv,colors)
    print("Done.")
 
    # Show results
    print("Saving images ...")
    cv2.imwrite(img_out,img_voronoi)
    print("Done.")
    print("(Press ESC to terminate.)")
    end = time.time()
    if not options.silent:
      cv2.imshow(win_voronoi,img_voronoi)
      cv2.waitKey(0)
      print("============ Time ============")
      print("total: " + str(end - start) + "seconds")
      print("voronoi: " + str(end - start_v) + "seconds")
      print("==============================")