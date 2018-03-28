#!/usr/bin/python
 
from __future__ import division
import cv2
import sys
import time
import os
import numpy as np
from clint.textui import progress, puts, colored
from optparse import OptionParser
from matplotlib import pyplot as plt
from fractions import gcd
from math import ceil, sqrt
from fractions import gcd
from random import randrange

def inRect(rect, point) :
    if point[0] < rect[0] :
        return False
    elif point[1] < rect[1] :
        return False
    elif point[0] > rect[2] :
        return False
    elif point[1] > rect[3] :
        return False
    return True

def avgRGB(a,b,c):
  return np.average((a,b,c),axis=0)

def process(sampler):
  puts(colored.green("[SUCCESS] Sampling successfull"))
  sampler.points.save()
  puts(colored.green("[SUCCESS] Saved coordinates in " + \
    colored.blue(str(sampler.input_name[:-4]) + "_" + sampler.current_sampling 
                + ".txt")))
  sampler.interpolate()
  puts(colored.green("[SUCCESS] Interpolation successfull"))
  puts(colored.green("[SUCCESS] Saved images in " + \
    colored.blue(str(sampler.input_name[:-4]) + "_" + sampler.current_sampling 
                + "_(voronoi|delaunay).txt")))

class InterpolationSet:
#     ======
  data = []                                                    # Initialize list
  colors = []
  subdiv = cv2.Subdiv2D((0, 0, 0, 0))

  def __init__(self,data,w,h):
#     ===================
    self.data = dict(data)
    self.subdiv = cv2.Subdiv2D((0, 0, w, h))

  def save(self):                     # Writes the sampled points in a text file 
#     ==========
    data_list = self.data.items()
    output = open(str(len(data_list)+1) + '_halton.txt', 'w')
    for item in data_list:
      output.write('{} {} {} {} {}\n' \
        .format(item[0][0],item[0][1],item[1][0],item[1][1],item[1][2]))

  def initSubdiv(self):
    with progress.Bar(label=colored.yellow("INIT SUBDIV     "), \
      expected_size=len(self.data)+1) as bar:
      i = 1
      data_list = self.data.items()
      for item in data_list:
        self.subdiv.insert(item[0])
        self.colors.append(item[1])
        i+=1
        bar.show(i)

# Generates a Voronoi diagram
  def drawVoronoi(self,img):
#     =====================
    (facets, centers) = self.subdiv.getVoronoiFacetList([])
    correspondingCenters = centers.tolist()
    overlay = img.copy()                                  # create alpha channel
    size = img.shape
    opacity = 0.7                                                # splat opacity
    with progress.Bar(label=colored.yellow("VORSPLATTING    "), 
                      expected_size=len(facets)+1) as bar:
      for i in xrange(0,len(facets)):          # iterate over every Voronoi cell
        ifacet_arr = []
        for f in facets[i]:
          ifacet_arr.append(f)
        ifacet = np.array(ifacet_arr, np.int)  # Colour cell according to center
        color = self.data[(int(correspondingCenters[i][0]), \
                          int(correspondingCenters[i][1]))]
        cv2.fillConvexPoly(overlay, ifacet, \
          (int(color[0]),int(color[1]),int(color[2])), cv2.LINE_AA, 0)
                                                                     # Splatting
                                       # Adding a transparent circle to overlay
        cv2.circle(overlay, (centers[i][0], centers[i][1]), 4, \
          (int(color[0]),int(color[1]),int(color[2])), -1, cv2.LINE_AA, 0)
                                                   # Connecting overlay to image
        cv2.addWeighted(overlay, opacity, img, 1 - opacity, 0, img)
        bar.show(i+2)

# Generates a Delaunay triangulation
  def drawDelaunay(self,img):
#     ======================
    triangles = self.subdiv.getTriangleList()
    size = img.shape
    r = (0, 0, size[1], size[0])
    i = 0
    with progress.Bar(label=colored.yellow("DELAUNAY        "), 
                      expected_size=len(triangles)) as bar:
      for t in triangles:                      # iterate every triangle possible
        pt1 = (int(t[0]), int(t[1]))
        pt2 = (int(t[2]), int(t[3]))
        pt3 = (int(t[4]), int(t[5]))
        if inRect(r, pt1) and inRect(r, pt2) and inRect(r, pt3):
          c = (self.data[pt1],self.data[pt2],self.data[pt3]) 
          poly = np.array([pt1,pt2,pt3], np.int)
          avColor = avgRGB(c[0],c[1],c[2])                    # averaging colors
          avColor = (int(avColor[0]),int(avColor[1]),int(avColor[2]))
          cv2.fillConvexPoly(img, poly, avColor, cv2.LINE_AA, 0);
          c1 = self.data[pt1]
          c1 = (int(c1[0]),int(c1[1]),int(c1[2]))
          c2 = self.data[pt2]
          c2 = (int(c2[0]),int(c2[1]),int(c2[2]))
          c3 = self.data[pt3]
          c3 = (int(c2[0]),int(c2[1]),int(c2[2]))
          i += 1
          bar.show(i)


class Sampler:
#     =======
  samples = []
  input_name = "image.jpg"
  img = cv2.imread(input_name)
  img_out = None
  points = None
  samplesize = None
  current_sampling = None


  def __init__(self, s, im):
#     =====================
    self.samples = []
    self.samplesize = s
    self.input_name = im
    self.img = cv2.imread(im)                           # Create image from name
    self.img_out = np.zeros(self.img.shape, dtype=self.img.dtype)  # Black Image
    size = self.img.shape
    self.points = InterpolationSet([],size[1], size[0])

# purely random sampling
  def random(self):
#     ============
    self.current_sampling = "random"
    size = self.img.shape
    bound_x, bound_y = int(size[0]), int(size[1])
    for i in range(0,samples):
      x = randrange(bound_x)
      y = randrange(bound_y)
      toAppend = ((y,x),(self.img[x,y][0], self.img[x,y][1], self.img[x,y][2]))
      self.points.data[(y,x)] = toAppend[1]            # Appends point and color
      self.img_out[x,y] = self.img[x,y]  
    cv2.imwrite(self.input_name[:-4] +'_random.jpg',self.img_out)

 
  def halton(self):
#     ============
    self.current_sampling = "halton"
    p=2 
    q=3
    seen = set()
    size = self.img.shape
    i = 0
    with progress.Bar(label=colored.yellow("RANDOM SAMPLING "), \
                      expected_size=self.samplesize) as bar:
      for i in range(1, self.samplesize):
        fx = 1
        fy = 1
        ix = i
        iy = i
        rx = 0
        ry = 0
    
        while ix > 0:
          fx /= p
          rx += fx * (ix % p)
          ix = ix//p
  
        while iy > 0:
          fy /= q
          ry += fy * (iy % q)
          iy = iy//q
        x = int(rx * size[0])
        y = int(ry * size[1])
        toAppend = ((y,x),(self.img[x,y][0], self.img[x,y][1], self.img[x,y][2]))
        
        self.points.data[(y,x)] = toAppend[1]        # Appends point and color
        self.img_out[x,y] = self.img[x,y]         # Visualize samples in image
        i += 1
        bar.show(i)
    cv2.imwrite(self.input_name[:-4] +'_halton.jpg',self.img_out)

  def grid(self):
#     ==========
    self.current_sampling = "grid"
    size = self.img.shape
    count_x = ceil(sqrt(self.samplesize))
    count_y = ceil(sqrt(self.samplesize))

    x_spacing = int(max(ceil(size[0]/count_x), 1))
    y_spacing = int(max(ceil(size[1]/count_y), 1))
    i = 0
    for y in range(0, size[1], y_spacing):
      for x in range(0, size[0], y_spacing):
        toAppend = ((y,x),(self.img[x,y][0], self.img[x,y][1], self.img[x,y][2]))
        
        self.points.data[(y,x)] = toAppend[1]        
        self.img_out[x,y] = self.img[x,y]
    cv2.imwrite(self.input_name[:-4] + '_grid.jpg',self.img_out)

  def interpolate(self):
#     =====================
    self.points.initSubdiv()
    self.points.drawVoronoi(self.img)
    cv2.imwrite(self.input_name[:-4] + "_" + sampler.current_sampling \
                + "_voronoi.jpg",self.img)
    self.points.drawDelaunay(self.img)
    cv2.imwrite(self.input_name[:-4] + "_" + sampler.current_sampling \
                + "_delaunay.jpg",self.img)

  def __str__(self):
#     =============
    return " Samples: {}\n Input: {}\n Height: {}\n Width: {}\n" \
      .format(self.samplesize, self.input_name, self.img.shape[1], self.img.shape[0])

if __name__ == '__main__':
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)

# Terminal parsing
    parser.add_option("-i", "--input", type="string", dest="input", \
                      help="import image to IMG", metavar="IMG_I", \
                      default = 'image.jpg')
    parser.add_option("-s", "--samples", type="int", dest="samples", \
                      help="amount of sampled pixels from IMG", default=1000)
    parser.add_option("-H", "--halton", action="store_true", dest="halton", \
                      help="use halton sampling")
    parser.add_option("-G", "--grid", action="store_true", dest="grid", \
                      help="use grid sampling")
    parser.add_option("-R", "--random", action="store_true", dest="random", \
                      help="use random sampling")
    (options, args) = parser.parse_args()

    if options.input:
      try:
        img = options.input
      except AttributeError:
        puts(colored.red("[ERROR] .jpg file not found in root directory."))
        sys.exit(0)
    if options.samples:
      samples = options.samples
    
    os.system('clear')
    puts("Initializing " + colored.red("DeVola"))
    puts(colored.red("De")+"launay-"+colored.red("Vo")+"ronoi-Sp"+colored.red("la")+"tting")
    sampler = Sampler(samples, img)
    puts(colored.green("[SUCCESS] Initialized image"))
    print(sampler)

    if options.grid:
      sampler.grid()
      process(sampler)

    if options.halton:
      sampler.halton()
      process(sampler)

    if options.random:
      sampler.random()
      process(sampler)
