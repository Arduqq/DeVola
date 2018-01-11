# **De**launay-**Vo**ronoi-Sp**la**tting
## Functionality
DeVola samples images using a pseudo-random halton sequence while saving the sampled data in a .txt-file. Based on the created samples, we can interpolate the image using Voronoi diagrams and Delaunay triangulation. Splatting is a very simple way of interpolating the image, yet salt-and-pepper-noise should be eliminiated by using the two algorithms as a base for the result. With different sizes and shrink-thresholds the splat sizes can vary to achieve simply beautiful images.

## Usage
```
python devola.py -h
```


## TODO
- [X] Delaunay WIP
- [ ] Better Splat variation
- [ ] quality assessement
- [ ] statistics, metrics etc.
- [ ] GUI
