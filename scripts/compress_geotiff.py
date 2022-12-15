import rasterio as rio
import pathlib
from os import path
import sys


def convert_geotiff(in_path, out_path, creation_options):
    """convert_geotiff 
    Compresses a GeoTiff file with JPEG Compression and YCbCr color space.

    Args:
        in_path (str): file to input file (geotiff)
        out_path (str): file to output file (geotiff)
        kwds (args): arguments for the rasterio write operation
    """

    src = rio.open(in_path)

    print(f"CRS: {src.crs.to_string()}")

    # get the blocks defined in the geotiff originally
    window_list = [window for _, window in src.block_windows()]

    # Use the input file's profile, updated by CLI
    # options, as the profile for the output file.
    profile = src.profile
    profile.update(**creation_options)
    print("Export profile:\n", profile)

    # write the new geotiff block wise to save ram (memory)
    with rio.open(out_path, "w", **profile) as dest:
        for sel_window in window_list:
            w = src.read(window=sel_window)
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
    parser.add_argument("--export_world_file", "-w",
                        action='store_true',
                        help="Optional: Add this Argument if you want to export an additional world file. Default is no world file will be exported.")
    parser.add_argument('--co', '--profile',
                        dest='creation_options',
                        metavar='NAME=VALUE ...',
                        nargs="+",
                        default=[],
                        action="append",
                        help="Driver specific creation options. The override the other arguments if defined multiple times."
                             "See the documentation for the selected output driver for "
                             "more information. https://gdal.org/drivers/raster/gtiff.html#creation-options")

    args = parser.parse_args()

    print("Input Arguments:")
    for arg in vars(args):
        print(arg, getattr(args, arg))
    print()

    in_path = path.abspath(args.input_file)

    # check in_path
    assert path.exists(
        in_path), f"File does not exist! Cannot find input file at: {in_path}"

    out_path = path.join(path.dirname(in_path), args.output_filename)

    # creation_options for output file
    creation_options = {}

    # set default creation options
    # create new block raster
    creation_options['tiled'] = True
    creation_options['blockxsize'] = 512
    creation_options['blockysize'] = 512

    # choose compression and color representation here
    creation_options['photometric'.lower()] = args.photometric.lower()
    creation_options['compress'] = args.compress.lower()

    # argument for exporting a world file export if not a tiff
    if pathlib.Path(out_path).suffix not in [".tif", ".tiff"]:
        args.export_world_file = True
    creation_options['tfw'] = args.export_world_file

    # check and parse creation options
    msg = "Wrong format of argument creation_option: {}\nPlease use the Format 'NAME=VALUE' for the creation_options."
    for cos in args.creation_options:
        for co in cos:
            assert co.count("=") == 1, msg.format(co)
            key_val = co.split("=")
            creation_options[key_val[0].lower()] = key_val[1].lower()

    # Print kwds
    print("Creation Options:")
    for x in creation_options:
        print(f"{x}:  {creation_options[x]}")
    print()

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
    convert_geotiff(in_path, out_path, creation_options)

    print("Done!")
