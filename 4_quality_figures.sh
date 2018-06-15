mkdir -p figure/quality
python3 quality.py -n -c configs/3.image.quallity/1.*/1.*/*.res.json configs/3.image.quallity/1.*/2.*/*.res.json -o figure/quality/das_lateral.pdf

python3 quality.py -n -c configs/3.image.quallity/1.*/3.*/*.res.json configs/3.image.quallity/1.*/4.*/*.res.json -o figure/quality/sa_lateral.pdf

python3 quality.py -n -c configs/3.image.quallity/2.*/1.*/*.res.json configs/3.image.quallity/2.*/2.*/*.res.json -o figure/quality/das_contrast.pdf

python3 quality.py -n -c configs/3.image.quallity/2.*/3.*/*.res.json configs/3.image.quallity/2.*/4.*/*.res.json -o figure/quality/sa_contrast.pdf
