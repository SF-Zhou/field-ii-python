# Field.II.Python

## Features

1. execute Field II in Python;
2. support parallel simulation;
3. support config files;
4. support delay-and-sum and synthetic aperture algorithm.

## Environments

1. make sure that MATLAB R2015b or later has been installed;
2. install Python 3.4 or 3.5;
3. install requirements `pip3 install -r requirements.txt`;
4. install MATLAB engines;
5. open several MATLAB sessions and share them;
6. run unittest `python3 -m pytest`.

### Install MATLAB engines

1. cd MATLAB path, for me it's `/Applications/MATLAB_R2016b.app/`;
2. cd `./extern/engines/python`;
3. run `python3 setup.py install`, `sudo` if need;
4. run `python3 -c "import matlab.engine"` for test.

### Open Several MATLAB Sessions

Run this command several times, change MATLAB path if need.

```shell
nohup /Applications/MATLAB_R2016b.app/bin/matlab &
disown
```

## Execute

```shell
python3 zombie.py MultiScat configs/multi_scat.json
```

Default config files are in `configs` folder, and default workers are in simulate module.
