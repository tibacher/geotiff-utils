# Python Toolkit for large GeoTiff Files


This is a small collection of Python scripts for operations like: compression, masking, and more...


The scripts where tested on python 3.8 and 3.10.


## Installation
Please make sure to have python installed. Do so by using the following command in your (system commandline), which checks the version of your python installation.
```python --version```


To run the script you need to install the dependencies first. To install them use the following command in the directory of this repository. The command needs to find the file `requirements.txt`.

```pip install -r requirements.txt```


### Virtual Environnement

You can also consider installing the requirements in a python virtual environnement.



## Usage

### Compression of large GeoTiffs
The script `scripts/compress_geotiff.py` compresses large geotiff files even on small computers. The Output is stored in the same directory as input.

```python scripts/compress_geotiff.py /path/to/input_file.tif output_filename.tif```

options:
  `-h`, `--help`           show this help message and exit



## Build Exe

Install the pip package `pyinstaller` the run the following command:

```pyinstaller compress_geotiff.spec```







