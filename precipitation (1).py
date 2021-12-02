import os
import gdal
import numpy as np


class RasterMeanCalculator:
    def __init__(self, input_path, output_path, aoi, clipped):
        self.input_path = input_path
        self.output_path = output_path
        self.aoi = aoi
        self.clipped = clipped

    def read_input_tiff_files(self):
        raster_list = [raster for raster in os.listdir(self.inputPath) if raster[-4:] == '.tif']
        print(raster_list, 'raster_list')
        return raster_list

    def clip_images_to_size_vector_file(self):
        for raster in self.read_input_tiff_files():
            print(self.output_path + raster[:-4] + raster[-4:])
            options = gdal.WarpOptions(cutlineDSName=self.aoi, cropToCutline=True)
            try:
                gdal.Warp(
                    srcDSOrSrcDSTab=self.input_path + raster,
                    destNameOrDestDS=self.output_path + raster[:-4] + raster[-4:],
                    options=options
                )
            except Exception as e:
                print(e)
                pass
        return True

    def calculate_mean_of_clipped_images(self):
        self.clip_images_to_size_vector_file()
        res = []
        for raster in self.clipped:
            ds = gdal.Open(raster)
            res.append(ds.GetRasterBand(1).ReadAsArray())
        stacked = np.dstack(res)
        mean = np.mean(stacked, axis=-1)
        driver = gdal.GetDriverByName('Geotiff')
        result = driver.CreateCopy('mean_precipitation.tif', gdal.Open(clipped[0]))
        result.GetRasterBand(1).WriteArray(mean)


if __name__ == '__main__':
    raster_mean_calculator = RasterMeanCalculator(
        input_path=r'E:\images for icha\Cropland masks\Cropland masks',
        output_path=r'D:\assign',
        aoi=r'E:\DL_Invasion\Outputs\vector\vectors sent\new\subcounty shapefilesCounty.shp\Bura.shp',
        clipped=r'D:\assign\Output'
    )
    raster_mean_calculator.calculate_mean_of_clipped_images()
    print("Done executing function")
