Set-Location "../01_Drohnendaten_Orthofotos/20220824/"

rio convert mosaic_complete.tif mosaic_test_1.tif `
    --dtype uint8 --scale-ratio 1 `
    --co tiled=true --co blockxsize=1024 --co blockysize=1024 `
    --co compress=JPEG --co photometric=RGB 

 
