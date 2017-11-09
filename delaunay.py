#!/usr/bin/python
 
import cv2
import sys
import time
import numpy as np
import random
 
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
 
def trianglize(container):
  triangles = []
  for i in range(0, len(container)-6):
    triangles.append([container[i],container[i+1],container[i+2]])
  return triangles
 
def avg_rgb(a,b,c):
  return np.average((a,b,c),axis=0)


# Draw delaunay triangles
def draw_delaunay(img, points, colors):
  trianglePoints = trianglize(points)
  print(trianglePoints[0])
  triangleColor = trianglize(colors)
  size = img.shape
  r = (0, 0, size[1], size[0])
  for t,c in zip(trianglePoints,triangleColor):
    if rect_contains(r, t[0]) and rect_contains(r, t[1]) and rect_contains(r, t[2]):
      poly = np.array([t[0],t[1],t[2]], np.int)
      cv2.fillConvexPoly(img, poly, avg_rgb(c[0],c[1],c[2]), cv2.LINE_AA, 0);
      # cv2.line(img, pt1, pt2, delaunay_color, 1, cv2.LINE_AA, 0)
      # cv2.line(img, pt2, pt3, delaunay_color, 1, cv2.LINE_AA, 0)
      # cv2.line(img, pt3, pt1, delaunay_color, 1, cv2.LINE_AA, 0)
 
if __name__ == '__main__':
 
    start = time.time()
    # Define window names
    win_delaunay = "Delaunay Triangulation"
 
    # Turn on animation while drawing triangles
    animate = False
     
    # Define colors for drawing.
    delaunay_color = (255,255,255)
    points_color = (0, 0, 255)
    try:
      # Read in the image.
      img = cv2.imread("image.jpg")
     
      # Keep a copy around
      img_orig = img.copy();
    except AttributeError:
      print("[ERROR] image.jpg file not found in root directory.")
      sys.exit(0)
     
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
      with open("points.txt") as file :
        print("Reading coordinates ...")
        for line in file :
          x, y, r, g, b = (line.split() + [None]*99)[:5]
          points.append((int(x), int(y)))
          colors.append((int(r), int(g), int(b)))
        print("Done.")
    except IOError:
      print("points.txt file not found in root directory.")
      sys.exit(0)
    except TypeError:
      print("points.txt might be invalid.")
      print("x-coordinate] [y-coordinate] [red-value] [green-value] [blue-value]")
      sys.exit(0)
 
    # Insert points into subdiv
    print("Processing points ...")
    for p in points :
      subdiv.insert(p)
      # Show animation
      if animate :
        img_copy = img_orig.copy()
        # Draw delaunay triangles
        draw_delaunay(img_copy, points, colors)
        cv2.imshow(win_delaunay, img_copy)
        cv2.waitKey(100)
    print("Done.")
 
    # Draw delaunay triangles
    print("Drawing dalaunay triangulation ...")
    start_d = time.time()
    draw_delaunay(img, points, colors)
 
    # Draw points
    for p in points :
      draw_point(img, p, (0,0,255))
    print("Done.")
 
    # Show results
    print("Saving images ...")
    cv2.imwrite("delaunay.jpg",img)
    print("Done.")
    print("(Press ESC to terminate.)")
    end = time.time()
    cv2.imshow(win_delaunay,img)
    cv2.waitKey(0)
    print("============ Time ============")
    print("global: " + str(end - start) + "seconds")
    print("delaunay: " + str(end - start_d) + "seconds")
    print("==============================")