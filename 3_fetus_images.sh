python3 main.py vn -c configs/4.fetus/1.DAS.json
python3 main.py vn -c configs/4.fetus/2.SA.json
mkdir -p figure/fetus
mv data/4.fetus/1.DAS/image.NDAS.pdf                       figure/fetus/DAS_fetus.pdf
mv data/4.fetus/1.DAS/image.NRDAS.pdf                      figure/fetus/RDAS_fetus.pdf
mv data/4.fetus/2.SA/image.synthetic_aperture.pdf          figure/fetus/SA_fetus.pdf
mv data/4.fetus/2.SA/image.reversed_synthetic_aperture.pdf figure/fetus/RSA_fetus.pdf
