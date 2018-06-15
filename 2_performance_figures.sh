mkdir -p figure/performance
python3 render.py -n -c configs/1*/1*/*.res.json -o figure/performance/das_sampling_frequency.pdf
python3 render.py -n -c configs/1*/2*/*.res.json -o figure/performance/das_number_of_elements.pdf
python3 render.py -n -c configs/1*/3*/*.res.json -o figure/performance/das_number_of_rows.pdf
python3 render.py -n -c configs/2*/1*/*.res.json -o figure/performance/sa_sampling_frequency.pdf
python3 render.py -n -c configs/2*/2*/*.res.json -o figure/performance/sa_number_of_elements.pdf
python3 render.py -n -c configs/2*/3*/*.res.json -o figure/performance/sa_number_of_rows.pdf
