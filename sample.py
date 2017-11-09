#!/usr/bin/python3

from __future__ import division
import cv2
import sys
import time
import numpy as np
from math import ceil, sqrt
from fractions import gcd
from random import randrange
from optparse import OptionParser

def is_unique(x,y,container):
  for i in container:
    if (i[0] == y) and (i[1] == x):
      return False
  return True 

def random_sample(img, samples, img_out):
  size = img.shape
  bound_x, bound_y = int(size[0]), int(size[1])
  points = []
  for i in range(0,samples):
    x = randrange(bound_x)
    y = randrange(bound_y)
    points.append([y,x,img[x,y][0], img[x,y][1], img[x,y][2]])
    img_out[x,y] = img[x,y]
  cv2.imwrite('out_random.jpg',img_out)
  return points

def random_sample_unique(img, samples, img_out):
  size = img.shape
  bound_x, bound_y = int(size[0]), int(size[1])
  points = []
  for i in range(0,samples):
    x = randrange(bound_x)
    y = randrange(bound_y)
    if is_unique(x,y,points):
      points.append([y,x,img[x,y][0], img[x,y][1], img[x,y][2]])
      img_out[x,y] = img[x,y]
  cv2.imwrite('out_randomu.jpg',img_out)
  return points

def rectangular_sample(img, samples, img_out):
  size = img.shape
  points = []
  k = gcd(size[0],size[1])
  reduced_x, reduced_y = size[0]/k, size[1]/k
  aspect = reduced_x / reduced_y
  count_x = ceil(sqrt(samples)*aspect)
  count_y = ceil(sqrt(samples)/aspect)

  x_spacing = int(max(ceil(size[0]/count_x), 1))
  y_spacing = int(max(ceil(size[1]/count_y), 1))

  for y in range(0, size[1], y_spacing):
    for x in range(0, size[0], x_spacing):
      points.append([y,x,img[x,y][0], img[x,y][1], img[x,y][2]])
      img_out[x,y] = img[x,y]
  cv2.imwrite('out_randomrect.jpg',img_out)
  return points

def equilateral_sample(img, samples, img_out):
  size = img.shape
  points = []
  bound_x, bound_y = int(size[0]), int(size[1])

  count_x = ceil(sqrt(samples))

  x_spacing = max(ceil(bound_x/count_x), 1)
  x_offset = x_spacing/2
  y_spacing = sqrt(x_spacing**2 - (x_spacing/2)**2)

  xmax = bound_x 
  ymax = bound_y
  y = 0
  odd_row = False

  while y < ymax:
    if odd_row:
      x = -x_offset
    else:
      x = 0
    while x < xmax:
      x = int(x)
      y = int(y)
      points.append([y,x,img[x,y][0], img[x,y][1], img[x,y][2]])
      img_out[x,y] = img[x,y]
      x += x_spacing
    off_row = not odd_row
    y += y_spacing
  cv2.imwrite('out_equi.jpg',img_out)
  return points


def halton_sample(img, samples, img_out, p=2, q=3):
  size = img.shape
  points = []
  i = 1
  for i in range(1, samples+1):
    fx = 1
    fy = 1
    ix = i
    iy = i
    rx = 0
    ry = 0

    # Calculate the ith p- and q-values
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
    if is_unique(x,y,points):
      points.append([y,x,img[x,y][0], img[x,y][1], img[x,y][2]])
      img_out[x,y] = img[x,y]
  cv2.imwrite('out_halton.jpg',img_out)
  return points
'''
  points.append([0, 0 ,img[0,0][0], img[0,0][1], img[0,0][2]])
  points.append([size[1], 0 ,img[0,size[1]][0], img[0,size[1]][1], img[0,size[1]][2]])
  points.append([size[1], size[0] ,img[size[0],size[1]][0], img[size[0],size[1]][1], img[size[0],size[1]][2]])
  points.append([0, size[0] ,img[size[0],0][0], img[size[0],0][1], img[size[0],0][2]])
'''
if __name__ == '__main__':
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)

    parser.add_option("-i", "--input",type="string", dest="input", help="import image to IMG", metavar="IMG")
    parser.add_option("-s", "--samples", type="int", dest="samples", help="amount of sampled pixel from IMG", default=1000)
    parser.add_option("-R", "--random", action="store_true", dest="random", help="use random sampling")
    parser.add_option("-U", "--randomu", action="store_true", dest="randomu", help="use unique random sampling")
    parser.add_option("-H", "--halton", action="store_true", dest="halton", help="use halton sampling")
    parser.add_option("-Q", "--quadratic", action="store_true", dest="rectangular", help="use rectangular sampling")
    parser.add_option("-E", "--equilateral", action="store_true", dest="equilateral", help="use equilateral sampling")

    (options, args) = parser.parse_args()
    if options.input:
      img = cv2.imread(options.input)
      win = "Voronoi Diagram"
    if options.samples:
      samples = options.samples
    img_sample = np.zeros(img.shape, dtype = img.dtype)
    if options.random:
      points_r = random_sample(img, samples, img_sample)
      output_r = open('random.txt', 'w')
      for item in points_r:
        output_r.write('{} {} {} {} {}\n'.format(*item))
    if options.randomu:
      points_ru = random_sample_unique(img, samples, img_sample)
      output_ru = open('randomu.txt', 'w')
      for item in points_ru:
        output_ru.write('{} {} {} {} {}\n'.format(*item))
    if options.halton:
      points_h = halton_sample(img, samples, img_sample)
      output_h = open('halton.txt', 'w')
      for item in points_h:
        output_h.write('{} {} {} {} {}\n'.format(*item))
    if options.rectangular:
      points_re = rectangular_sample(img, samples, img_sample)
      output_re = open('rect.txt', 'w')
      for item in points_re:
        output_re.write('{} {} {} {} {}\n'.format(*item))
    if options.equilateral:
      points_e = equilateral_sample(img, samples, img_sample)
      output_e = open('equi.txt', 'w')
      for item in points_e:
        output_e.write('{} {} {} {} {}\n'.format(*item))
    
       