import rasterio as rio
from rasterio import enums
from os import path



def convert_geotiff(in_path,out_path):
    """convert_geotiff 
    Compresses a GeoTiff file with JPEG Compression and YCbCr color space.

    Args:
        in_path (str): file to input file (geotiff)
        out_path (str): file to output file (geotiff)
    """
    
    # open the original geotiff
    inds = rio.open(in_path)
    
    
    # get the blocks defined in the geotiff originally
    window_list = [window for _, window in inds.block_windows()]
    
    # copy the world and meta data
    out_meta = inds.meta.copy()

    # arguments for output file
    kwds = {}
    # create new block raster
    kwds['tiled'] = True
    kwds['blockxsize'] = 512
    kwds['blockysize'] = 512
    
    # choose compression and color representation here
    # choose from these options:
    # https://rasterio.readthedocs.io/en/latest/api/rasterio.enums.html#rasterio.enums.PhotometricInterp
    # https://rasterio.readthedocs.io/en/latest/api/rasterio.enums.html#rasterio.enums.Compression
    kwds['photometric'] = enums.PhotometricInterp.ycbcr
    kwds['compress'] = enums.Compression.jpeg
     
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

    args = parser.parse_args()
    
    print("Input Arguments:")
    print("input_file: ", args.input_file)
    print("output_filename: ", args.output_filename)
    print()

    
    #in_dir = '/Users/TimSchäfer/OneDrive - RSRG/10_RC_Daten/Cogito-Daten/RC_Cogito/01_Drohnendaten_Orthofotos/20220824/'
    #in_filename = 'mosaic_model.tif'

    in_path = path.abspath(args.input_file)
    
    # check in_path
    assert path.exists(in_path), f"File does not exist! Cannot find input file at: {in_path}"
    
    out_path = path.join(path.dirname(in_path),args.output_filename)
    
    
    # check out_path and ask for overwrite...
    if path.exists(out_path):
        print("Output file already exist!")
        while True:
            user_input = input('Do you want to overwrite? y/n: ')
        
            if user_input.lower() == 'n':
                print("Exit script...")
                exit(0)
            elif user_input.lower() == 'y':
                print('overwriting')
                break
            else:
                print("Type 'y' or 'n'")
            
    
    print("Start process...")
    
    # start conversion
    convert_geotiff(in_path,out_path)
    
    print("Done!")



    
