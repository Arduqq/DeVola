python sample.py -i finesse.jpg -s 100000 -H
python voronoi.py-s -i finesse.jpg -c halton.txt -o finessev_100000.jpg
python splat.py  -i finesse.jpg -c halton.txt -o finesses_100000.jpg

python sample.py -i direction.jpg -s 100000 -H
python voronoi.py -s -i direction.jpg -c halton.txt -o directionv_100000.jpg
python splat.py  -i direction.jpg -c halton.txt -o directions_100000.jpg

python sample.py -i details.jpg -s 100000 -H
python voronoi.py  -s -i details.jpg -c halton.txt -o directionv_100000.jpg
python splat.py  -i details.jpg -c halton.txt -o directions_100000.jpg

python sample.py -i details.jpg -s 350000 -H
python voronoi.py -s  -i details.jpg -c halton.txt -o directionv_350000.jpg
python splat.py  -i details.jpg -c halton.txt -o directions_350000.jpg
