echo "samples: 1000"
python3 sample.py -RUHEQ -i image.jpg -s 1000

python voronoi.py -s -i image.jpg -c random.txt -o 1000_r.jpg
python voronoi.py -s -i image.jpg -c randomu.txt -o 1000_ru.jpg
python voronoi.py -s -i image.jpg -c rect.txt -o 1000_q.jpg
python voronoi.py -s -i image.jpg -c halton.txt -o 1000_h.jpg
python voronoi.py -s -i image.jpg -c equi.txt -o 1000_e.jpg

echo "samples: 5000"
python3 sample.py -RUHEQ -i image.jpg -s 5000

python voronoi.py -s -i image.jpg -c random.txt -o 5000_r.jpg
python voronoi.py -s -i image.jpg -c randomu.txt -o 5000_ru.jpg
python voronoi.py -s -i image.jpg -c rect.txt -o 5000_q.jpg
python voronoi.py -s -i image.jpg -c halton.txt -o 5000_h.jpg
python voronoi.py -s -i image.jpg -c equi.txt -o 5000_e.jpg

echo "samples: 10000"
python3 sample.py -RUHEQ -i image.jpg -s 10000

python voronoi.py -s -i image.jpg -c random.txt -o 10000_r.jpg
python voronoi.py -s -i image.jpg -c randomu.txt -o 10000_ru.jpg
python voronoi.py -s -i image.jpg -c rect.txt -o 10000_q.jpg
python voronoi.py -s -i image.jpg -c halton.txt -o 10000_h.jpg
python voronoi.py -s -i image.jpg -c equi.txt -o 10000_e.jpg

echo "samples: 50000"
python3 sample.py -RUHEQ -i image.jpg -s 50000

python voronoi.py -s -i image.jpg -c random.txt -o 50000_r.jpg
python voronoi.py -s -i image.jpg -c randomu.txt -o 50000_ru.jpg
python voronoi.py -s -i image.jpg -c rect.txt -o 50000_q.jpg
python voronoi.py -s -i image.jpg -c halton.txt -o 50000_h.jpg
python voronoi.py -s -i image.jpg -c equi.txt -o 50000_e.jpg

echo "samples: 100000"
python3 sample.py -RUHEQ -i image.jpg -s 100000

python voronoi.py -s -i image.jpg -c random.txt -o 100000_r.jpg
python voronoi.py -s -i image.jpg -c randomu.txt -o 100000_ru.jpg
python voronoi.py -s -i image.jpg -c rect.txt -o 100000_q.jpg
python voronoi.py -s -i image.jpg -c halton.txt -o 100000_h.jpg
python voronoi.py -s -i image.jpg -c equi.txt -o 100000_e.jpg

echo "samples: 300000"
python3 sample.py -RUHEQ -i image.jpg -s 30000

python voronoi.py -s -i image.jpg -c random.txt -o 300000_r.jpg
python voronoi.py -s -i image.jpg -c randomu.txt -o 300000_ru.jpg
python voronoi.py -s -i image.jpg -c rect.txt -o 300000_q.jpg
python voronoi.py -s -i image.jpg -c halton.txt -o 300000_h.jpg
python voronoi.py -s -i image.jpg -c equi.txt -o 300000_e.jpg0

echo "Done."