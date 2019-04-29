# utf-8
"""
This file contains the classes and functions for working with vector (point, line, polygon) data.
"""
# ToDo Look at using GeoPandas
import fiona
import fiona.crs


class VectorLayer:
    """
    For working with and reading Vector data.
    """
    def __init__(self, file_path):
        super().__init__()
        self._file_path = file_path
        self._vector_layer = fiona.open(self._file_path)
        self.x = []
        self.y = []

    def get_crs(self):
        """Returns projection of vector layer"""
        return self._vector_layer.crs

    def get_crs_wkt(self):
        """Returns projection of vector layer in WKT"""
        return self._vector_layer.crs_wkt

    def get_crs_ellipsoid(self):
        """Returns the PROJ.4 ellipsoid for the vector layer"""
        crs = self._vector_layer.crs
        return fiona.crs.to_string(crs)

    def get_bounding_box(self):
        """Returns the bounding box of the vector layer"""
        return self._vector_layer.bounds

    def get_file_type(self):
        """Returns the file type of the vector layer"""
        return self._vector_layer.driver

    def get_data_schema(self):
        """Returns the schema of the vector layer"""
        return self._vector_layer.schema

    def get_geometry_type(self):
        """Returns the geometry type (point, line, polygon) of the vector layer"""
        return self.get_data_schema()['geometry']

    def get_all_metadata(self):
        """Returns all metadata attached to the vector layer"""
        return self._vector_layer.meta

    def get_all_features(self):
        """Returns all features in the vector layer"""
        return [feature["geometry"] for feature in self._vector_layer]

    def fishnet(self, cell_size=1, centroid=True):
        """Returns a square grid based on the bounding box and the width in meters"""

        if cell_size <= 0:  # Value must be greater than 0, otherwise error
            raise ValueError('This value must be greater than zero.')

        westing, southing, easting, northing = self.get_bounding_box()  # Get the bounding easting's and northing's in m

        # Get each X measuring point coordinate and add to list, adjust to centroid if necessary
        for x_dim in range(round((easting - westing) / cell_size)):
            if centroid:
                self.x.append((westing + (x_dim * cell_size) + (cell_size / 2)))
            else:
                self.x.append(westing + (x_dim * cell_size))

        # Get each Y measuring point coordinate and add to list, adjust to centroid if necessary
        for y_dim in range(round((northing - southing) / cell_size)):
            if centroid:
                self.y.append((southing + (y_dim * cell_size) + (cell_size / 2)))
            else:
                self.y.append(southing + (y_dim * cell_size))

        return {'xcoords': self.x, 'ycoords': self.y}  # Return both X and Y lists as a dictionary
