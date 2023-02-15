# %%
import numpy
import rasterio
from rasterio.enums import Resampling
from rasterio.windows import Window
from rasterio import Affine
import os 

# %%

resample_factor = 1 / 6  # Downsample to 1/2 of the resolution

input_path = '/Users/TimSchäfer/OneDrive - RSRG/10_RC_Daten/Cogito-Daten/RC_Cogito/01_Drohnendaten_Orthofotos/20220824/mosaic_complete.tif'
output_filename = f'{os.path.splitext(os.path.basename(input_path))[0]}_resampled_{resample_factor:.2f}.tif'
output_path = os.path.join(os.path.dirname(input_path),output_filename)

# %%

# Open the datasets once, not every single loop iteration...
# Load 20m profile and block sizes
with rasterio.open(input_path) as data:


    blocks = list(data.block_windows()) 
    t = data.transform
    # rescale the metadata
    transform = Affine(t.a / resample_factor, t.b, t.c, t.d, t.e / resample_factor, t.f)
    height = int(data.height * resample_factor)
    width = int(data.width * resample_factor)

    profile = data.profile
    
    profile.update(transform=transform, driver='GTiff',
                   height=height, width=width)
    
    with rasterio.open(output_path, 'w', **profile) as dataset:
        # Loop on blocks
        for _, window in blocks:
            # Resample the window
            res_window = Window(int(window.col_off * resample_factor), int(window.row_off * resample_factor),
                                int(window.width * resample_factor), int(window.height * resample_factor))
            try:
                result = data.read(
                    out_shape=(
                        data.count,
                        res_window.height,
                        res_window.width
                    ),
                    resampling=Resampling.bilinear,
                    masked=True,
                    window=window
                )
            except Exception as e:
                print("Error:",e)
                break
            dataset.write(result, window=res_window)



