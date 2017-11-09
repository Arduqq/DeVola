# Image recovery using voronoi diagrams
## Usage
```
python sample.py -h
Sample a given image using different sample methods. Right now you can sample using rectangular, equilateral, random and halton-based sampling methods. The output will be a text file looking like this:
```
[x-coordinate] [y-coordinate] [red] [green] [blue]
[x-coordinate] [y-coordinate] [red] [green] [blue]
[x-coordinate] [y-coordinate] [red] [green] [blue]
[x-coordinate] [y-coordinate] [red] [green] [blue]
```
```
python voronoi.py -h
```
Create a voronoi diagram using the sampled coordinates.

```
python fourier.py -h
```
Calculate the Fourier transform of the generated image.


## TODO
- [ ] Delaunay WIP!
- [ ] quality assessement
- [ ] statistics, metrics etc.
