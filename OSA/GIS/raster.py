# utf-8
"""
This file contains the classes and functions for working with raster data.
"""
# External imports
import pandas
import rasterio
from rasterio.mask import mask

# Internal imports
from .vector import VectorLayer


class RasterLayer:
    """
    For working with and reading Raster data.
    """
    def __init__(self, file_path):
        super().__init__()
        self._file_path = file_path
        self._raster_layer = rasterio.open(self._file_path)

    def get_crs(self):
        """Returns projection of the raster layer"""
        return self._raster_layer.crs

    def get_transform(self):
        """Returns affine transform (how the raster layer is scaled, rotated, skewed, and/or translated)"""
        return self._raster_layer.transform

    def get_dimensions(self):
        """Returns tuple containing width and height of the raster layer"""
        dimension = (self._raster_layer.width, self._raster_layer.height)
        return dimension

    def get_bands(self):
        """Returns the number of bands in the raster layer"""
        return self._raster_layer.count

    def get_bounding_box(self):
        """Returns the bounding box of the raster layer"""
        return self._raster_layer.bounds

    def get_file_type(self):
        """Returns the file type of the raster layer"""
        return self._raster_layer.driver

    def get_no_data_values(self):
        """Returns all no data channels in the raster layer"""
        return self._raster_layer.nodatavals

    def get_data_types(self):
        """Returns the data type of the raster layer"""
        return self._raster_layer.dtypes

    def get_all_metadata(self):
        """Returns all metadata attached to raster layer"""
        return self._raster_layer.meta

    def mask(self, vector_layer, export_file):
        """Creates a new raster layer which has been masked by a shapefile and points to the new layer"""
        if isinstance(vector_layer, VectorLayer):
            if vector_layer.get_geometry_type() == 'Polygon':
                features = vector_layer.get_all_features()
                out_image, out_transform = mask(self._raster_layer, features, crop=True)
                out_meta = self._raster_layer.meta.copy()
                out_meta.update({"height": out_image.shape[1], "width": out_image.shape[2], "transform": out_transform})

                with rasterio.open(export_file, "w", **out_meta) as dest:
                    dest.write(out_image)
                self._raster_layer.close()
                self._file_path = export_file
                self._raster_layer = rasterio.open(export_file)
            else:
                print('raise not_polygon error')
        else:
            print('raise not_vector error')

    def get_value_at_point(self, x, y):
        """Returns the value of the raster at the specified easting and northing"""
        return self._raster_layer.sample([(x, y)])

    def get_values(self, points):
        """Returns the values at all points specified as a pandas dataframe"""
        vals = []
        for x in points['xcoords']:
            for y in points['ycoords']:
                for val in self.get_value_at_point(x, y):
                    vals.append(val)
        d_frame = pandas.DataFrame(vals)
        return d_frame

