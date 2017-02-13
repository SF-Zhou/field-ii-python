# [Field.II.Python](https://github.com/SF-Zhou/Field.II.Python)

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

## Simulate

```shell
python3 simu.py configs/multi_scat.json
```

Default config files are in `configs` folder. And the final signal result will be stored in **save_path** configured in config file, filename is `signal`.

**multi_scat.json** config:

```json
{
  "save_path": "data/multi_scat",
  "worker": "MultiScat",
  "transducer_frequency": 5e6,
  "sampling_frequency": 4e7,
  "element_count": 128,
  "element_width": 2.798e-4,
  "element_height": 4e-3,
  "kerf": 2.5e-05,
  "focus": [0.0, 0.0, 3.3e-2],
  "line_count": 64,
  "row_count": 1024,
  "data_length": 2048,
  "dynamic_range": 20,
  "z_start": 5e-3,
  "z_size": 40e-3,
  "point_count": 6,
  "light_points": [
    [-2e-3, 0e-3, 15e-3],
    [ 2e-3, 0e-3, 15e-3],
    [-4e-4, 0e-3, 25e-3],
    [ 4e-4, 0e-3, 25e-3],
    [-2e-3, 0e-3, 35e-3],
    [ 2e-3, 0e-3, 35e-3]
  ]
}
```

## Calculation

Firstly, make sure the **cpp_method** has been built successfully.

```shell
cd cpp_method
make
cd ..  # return repo root path
```

Execute beamforming of C++ version:

```
cpp_method/bin/beamforming -c configs/multi_scat.json -m synthetic_aperture -t 5
```

* -c: config file path
* -m: calculation method
* -t: running times

There is also another C++ version without console output to improve accuracy of time measuring: `cpp_method/bin/measure`.

The final image data will be stored in **save_path** configured in config file, filename is `image.{method}`.

## Show Image

```shell
python3 show.py configs/multi_scat.json delay_and_sum
```

