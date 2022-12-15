import rasterio as rio
import os
from os import path
import sys


def convert_geotiff(in_path, out_path, kwds):
    """convert_geotiff 
    Compresses a GeoTiff file with JPEG Compression and YCbCr color space.

    Args:
        in_path (str): file to input file (geotiff)
        out_path (str): file to output file (geotiff)
        kwds (args): arguments for the rasterio write operation
    """

    # open the original geotiff
    inds = rio.open(in_path)

    # get the blocks defined in the geotiff originally
    window_list = [window for _, window in inds.block_windows()]

    # copy the world and meta data
    out_meta = inds.meta.copy()

    print(inds.crs)
    print(out_meta['crs'])

    # write the new geotiff block wise to save ram (memory)
    with rio.open(out_path, "w", **out_meta, **kwds) as dest:
        for sel_window in window_list:
            w = inds.read(window=sel_window)
            dest.write(w, window=sel_window)


############################################################
#  Script Main
############################################################


if __name__ == '__main__':
    import argparse

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Converts a GeoTiff File. The Output is stored in the same directory as input')
    parser.add_argument("input_file",
                        metavar="/path/to/input_file.tif",
                        help="e.g. 'mosaic_model.tif' or 'C:\\Test\\mosaic_model.tif'")
    parser.add_argument("output_filename",
                        metavar="output_filename.tif",
                        help="e.g. 'mosaic_model_jpeg.tif'")
    parser.add_argument("--compress",
                        metavar="<compress method>",
                        default="jpeg",
                        help="Optional: Default is 'jpeg' see all options here: https://rasterio.readthedocs.io/en/latest/api/rasterio.enums.html#rasterio.enums.Compression")
    parser.add_argument("--photometric",
                        metavar="<photometric interp>",
                        default="ycbcr",
                        help="Optional: Default is 'ycbcr' see all options here: https://rasterio.readthedocs.io/en/latest/api/rasterio.enums.html#rasterio.enums.PhotometricInterp")

    args = parser.parse_args()

    print("Input Arguments:")
    print("input_file: ", args.input_file)
    print("output_filename: ", args.output_filename)
    print("photometric: ", args.photometric)
    print("compress: ", args.compress)
    print()

    # arguments for output file
    kwds = {}
    # create new block raster
    kwds['tiled'] = True
    kwds['blockxsize'] = 512
    kwds['blockysize'] = 512

    # choose compression and color representation here
    kwds['photometric'] = args.photometric
    kwds['compress'] = args.compress

    #in_dir = '/Users/TimSchäfer/OneDrive - RSRG/10_RC_Daten/Cogito-Daten/RC_Cogito/01_Drohnendaten_Orthofotos/20220824/'
    #in_filename = 'mosaic_model.tif'

    in_path = path.abspath(args.input_file)

    # check in_path
    assert path.exists(
        in_path), f"File does not exist! Cannot find input file at: {in_path}"

    out_path = path.join(path.dirname(in_path), args.output_filename)

    # check out_path and ask for overwrite...
    if path.exists(out_path):
        print("Output file already exist!")
        while True:
            user_input = input('Do you want to overwrite? y/n: ')

            if user_input.lower() == 'n':
                print("Exit script...")
                sys.exit()
            elif user_input.lower() == 'y':
                print('overwriting')
                break
            else:
                print("Type 'y' or 'n'")

    print("Start process...")

    # start conversion
    convert_geotiff(in_path, out_path, kwds)

    print("Done!")
