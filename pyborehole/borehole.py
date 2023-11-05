import pandas as pd
import numpy as np
import shapely
from shapely.geometry import Point, LineString
from pyproj import CRS
import pyproj
import matplotlib.pyplot as plt
from typing import Union
import geopandas as gpd


class Borehole:
    """Class to initiate a borehole object.

    Parameters
    __________
        name : str
            Name of the Borehole, e.g. ``name='Weisweiler R1'``.
        address : str
            Address of the Borehole, e.g. ``address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland'``.
        location : tuple
            Coordinates tuple representing the location of the Borehole, e.g. ``location=(6.313031, 50.835676)``.
        crs : Union[str, pyproj.crs.crs.CRS]
            Coordinate Reference System of the coordinates, e.g. ``crs='EPSG:4326'``.
        altitude_above_sea_level : Union[int, float]
            Altitude above sea level, e.g. ``'altitude_above_sea_level=136``.

    Returns
    _______
        Borhole object.

    Examples
    ________
        >>> from pyborehole.borehole import Borehole
        >>> borehole = Borehole(name='Weisweiler R1', address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland', location=(6.313031, 50.835676), crs='EPSG:4326', altitude_above_sea_level=136)

    .. versionadded:: 0.0.1

    """

    def __init__(self,
                 name: str,
                 address: str,
                 location: tuple,
                 crs: Union[str, pyproj.crs.crs.CRS],
                 altitude_above_sea_level: Union[int, float]):

        # Checking that the name is provided as string
        if not isinstance(name, str):
            raise TypeError('The name of the borehole must be provided as string')

        # Checking that the address is provided as string
        if not isinstance(address, str):
            raise TypeError('The address of the borehole must be provided as string')

        # Checking that the location is provided as tuple
        if not isinstance(location, tuple):
            raise TypeError('The location of the borehole must be provided as tuple')

        # Checking that the crs is provided as string or pyproj CRS
        if not isinstance(crs, (str, pyproj.crs.crs.CRS)):
            raise TypeError('The CRS of the borehole location must be provided as string or pyproject CRS')

        # Checking that the altitude is provided as float
        if not isinstance(altitude_above_sea_level, (int, float)):
            raise TypeError('The altitude of the borehole must be provided as float')

        # Define attributes
        self.name = name
        self.address = address
        self.location = Point(location)
        self.x = list(self.location.coords)[0][0]
        self.y = list(self.location.coords)[0][1]
        self.crs = crs
        self.crs_pyproj = CRS.from_user_input(self.crs)
        self.altitude_above_sea_level = altitude_above_sea_level
        self.altitude_above_kb = None

        # Add Deviation and well logs
        self.deviation = None
        self.logs = None

        # Create borehole DataFrame
        self.df = self.create_df()

    def __str__(self):
        return f"{self.name}"

    def create_df(self):
        """Create DataFrame from Borehole Object Attributes.

        Returns
        _______
            df : pd.DataFrame
                DataFrame containing the Borehole Metadata.

        """
        # Create dict from attributes
        df_dict = {'Name': self.name,
                   'Address': self.address,
                   'Location': self.location,
                   'X': self.x,
                   'Y': self.y,
                   'Coordinate Reference System': self.crs,
                   'Coordinate Reference System PyProj': self.crs_pyproj,
                   'Altitude above sea level': self.altitude_above_sea_level,
                   'Altitude above KB': self.altitude_above_kb
                   }

        # Creating DataFrame from dict
        df = pd.DataFrame.from_dict(data=df_dict,
                                    orient='index',
                                    columns=['Value'])

        return df

    def update_df(self, data_dict: dict):
        """Update DataFrame with data from data_dict.

        Parameters
        __________
            data_dict : dict
                Dictionary containing the new data.

        """
        # Create DataFrame from dict
        df = pd.DataFrame.from_dict(data=data_dict,
                                    orient='index',
                                    columns=['Value'])

        # Concatenating DataFrames
        self.df = pd.concat([self.df,
                             df])

    def add_deviation(self,
                      path: str,
                      delimiter: str,
                      step: float):
        """Add deviation to the Borehole Object.

        Parameters
        __________
            path : str
                Path to the deviation file, e.g. ``path='logs.las'``.
            delimiter : str
                Delimiter to read the deviation file correctly, e.g. ``delimiter=';'``.
            step : float
                Step for resampling the deviation data, e.g. ``step=5``.


        """
        # Create deviation
        self.deviation = Deviation(path=path,
                                   delimiter=delimiter,
                                   step=step)

        # Updating DataFrame
        self.update_df(self.deviation.data_dict)

    def add_well_logs(self,
                      path):
        """Add Well Logs to the Borehole Object.

        Parameters
        __________
            path : str
                Path to the well log file
        """
        # Creating well logs
        self.logs = Logs(path=path)

    # def read_boreholeml(self):
    # def write_boreholeml(self):


class Deviation():
    """Class to initiate a Deviation object.

    Parameters
    __________
        path : str
            Path to the deviation file, e.g. ``path='logs.las'``.
        delimiter : str
            Delimiter to read the deviation file correctly, e.g. ``delimiter=';'``.
        step : float
                Step for resampling the deviation data, e.g. ``step=5``.

    """
    def __init__(self,
                 path: str,
                 delimiter: str,
                 step: float = 5):

        # Importing wellpathpy
        try:
            import wellpathpy as wp
        except ModuleNotFoundError:
            ModuleNotFoundError('wellpathpy package not installed')

        # Opening deviation file
        md, inc, azi = wp.read_csv(fname=path,
                                   delimiter=delimiter)

        # Creating deviation
        dev = wp.deviation(
            md=md,
            inc=inc,
            azi=azi
        )

        # Assigning attributes
        self.md = dev.md
        self.inc = dev.inc
        self.azi = dev.azi

        # Calculating positions
        pos = dev.minimum_curvature().resample(depths=list(range(0,
                                                                 int(dev.md[-1]) + 1,
                                                                 step)))

        # Assigning attributes
        self.tvd = pos.depth
        self.northing_rel = pos.northing
        self.easting_rel = pos.easting

        self.az = np.arctan2(self.easting_rel,
                             self.northing_rel)
        self.radius = np.sqrt(self.northing_rel ** 2 + self.easting_rel ** 2)

        # Creating data dict
        data_dict = {'Measured Depth': [self.md],
                     'Inclination': [self.inc],
                     'Azimuth': [self.azi],
                     'True Vertical Depth': [self.tvd],
                     'Northing_rel': [self.northing_rel],
                     'Easting_rel': [self.easting_rel],
                     }

        # Assigning data_dict
        self.data_dict = data_dict

        # Creating DataFrame from deviation data
        self.deviation_df = pd.DataFrame.from_dict({'Measured Depth': self.md,
                                                    'Inclination': self.inc,
                                                    'Azimuth': self.azi},
                                                   orient='columns',
                                                   )

        # Creating DataFrame from position data
        self.desurveyed_df = pd.DataFrame.from_dict({'True Vertical Depth': self.tvd,
                                                     'Northing_rel': self.northing_rel,
                                                     'Easting_rel': self.easting_rel},
                                                    orient='columns',
                                                    )

    def add_origin_to_desurveying(self,
                                  x: float =0,
                                  y: float =0,
                                  z: float =0):
        """Add origin to desurveying.

        Parameters
        __________
            x : float
                X-Coordinate of the origin, e.g. ``x=1000``.
            y : float
                Y-Coordinate of the origin, e.g. ``y=1000``.
            z : float
                Altitude of the origin, e.g. ``z=200``.

        """
        # Adding the X coordinate
        self.desurveyed_df['Northing'] = self.desurveyed_df['Northing_rel'] + y

        # Adding the Y coordinate
        self.desurveyed_df['Easting'] = self.desurveyed_df['Easting_rel'] + x

        # Adding the Z coordinate
        self.desurveyed_df['True Vertical Depth Below Sea Level'] = z - self.desurveyed_df['True Vertical Depth']

    def plot_deviation_polar_plot(self,
                                  c: np.ndarray = None,
                                  vmin: float = None,
                                  vmax: float = None):
        """Add polar plot representing the deviation of a borehole.

        Parameters
        __________
            c : np.ndarray
                Array for coloring the well path.
            vmin : float
                Minimum value for colormap.
            vmax : float
                Maximum value for colormap.

        """
        # Creating plot
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

        # Setting zero to North
        ax.set_theta_zero_location('N')

        # Counting clockwise
        ax.set_theta_direction(-1)

        # Plotting
        if c is not None:
            ax.scatter(self.az,
                       self.radius,
                       c=c,
                       vmin=vmin,
                       vmax=vmax)
        else:
            ax.plot(self.az,
                    self.radius)

        return fig, ax

    def plot_deviation_3d(self,
                          elev: float = 45,
                          azim: float = 45,
                          roll: float = 0):
        """Create 3D Deviation Plot.

        Parameters
        __________
            elev : float
                Elevation angle for view.
            azim : float
                Azimuth angle for view.
            roll : float
                Rolling angle for view.
        """
        # Creating figure
        fig, ax = plt.subplots(subplot_kw={'projection': '3d'})

        # Plotting
        ax.plot(self.easting_rel,
                self.northing_rel,
                -self.tvd)

        # Setting plotting parameters
        ax.view_init(elev, azim, roll)
        ax.set_xlabel('Easting')
        ax.set_ylabel('Northing')
        ax.set_zlabel('TVD')

        plt.tight_layout()

        return fig, ax

    def get_borehole_tube(self,
                          radius: float = 10,
                          x: float = 0,
                          y: float = 0):
        """Get borehole tube.

        Parameters
        __________
            radius : float
                Radius of the borehole tube, e.g. ``radius=10``.
            x : float
                X-coordinate of the borehole, e.g. ``x=1000``.
            y : float
                X-coordinate of the borehole, e.g. ``y=1000``.
        """

        # Importing pyvista
        try:
            import pyvista as pv
        except ModuleNotFoundError:
            ModuleNotFoundError('PyVista package not installed')

        # Creating lines from points
        def lines_from_points(points):
            """Given an array of points, make a line set"""
            poly = pv.PolyData()
            poly.points = points
            cells = np.full((len(points) - 1, 3), 2, dtype=np.int_)
            cells[:, 1] = np.arange(0, len(points) - 1, dtype=np.int_)
            cells[:, 2] = np.arange(1, len(points), dtype=np.int_)
            poly.lines = cells
            return poly

        # Creating spline
        spline = lines_from_points(np.c_[self.easting_rel + x,
                                         self.northing_rel + y,
                                         -self.tvd])
        # Creating tube
        tube = spline.tube(radius=radius)

        # Assigning depth values
        tube['TVD'] = tube.points[:,2]

        return tube


class Logs:
    """Class to initiate a Well Log Object.

    Parameters
    __________
        path : str
            Path to the well logs, e.g. ``path='logs.las'``.

    """
    def __init__(self, path: str):

        # Importing lasio
        try:
            import lasio
        except ModuleNotFoundError:
            ModuleNotFoundError('lasio package not installed')

        # Opening LAS file
        las = lasio.read(path)

        # Extracting DataFrame from LAS file
        self.df = las.df()

        # Creating DataFrame from curve data
        self.curves = pd.DataFrame(list(zip([las.curves[i]['original_mnemonic'] for i in range(len(las.curves))],
                                            [las.curves[i]['mnemonic'] for i in range(len(las.curves))],
                                            [las.curves[i]['descr'] for i in range(len(las.curves))],
                                            [las.curves[i]['unit'] for i in range(len(las.curves))])),
                                   columns=['original_mnemonic',
                                            'mnemonic',
                                            'descr',
                                            'unit'])

        # Creating DataFrame from well header
        self.well_header = pd.DataFrame(list(zip([las.well[i]['mnemonic'] for i in range(len(las.well))],
                                                 [las.well[i]['unit'] for i in range(len(las.well))],
                                                 [las.well[i]['value'] for i in range(len(las.well))],
                                                 [las.well[i]['descr'] for i in range(len(las.well))])),
                                        columns=['mnemonic',
                                                 'unit',
                                                 'value',
                                                 'descr'])

        # Creating DataFrame from parameters
        self.params = pd.DataFrame(list(zip([las.params[i]['mnemonic'] for i in range(len(las.params))],
                                            [las.params[i]['unit'] for i in range(len(las.params))],
                                            [las.params[i]['value'] for i in range(len(las.params))],
                                            [las.params[i]['descr'] for i in range(len(las.params))])),
                                   columns=['mnemonic',
                                            'unit',
                                            'value',
                                            'descr'])

    def plot_well_logs(self,
                       tracks: Union[str, list]):
        """Plot well logs

        Parameters
        __________

        tracks : Union[str, list]
            Name/s of the logs to be plotted
        """
        # Selecting tracks
        df = self.df[tracks].reset_index()

        # Creating plot
        fig, ax = plt.subplots(1, len(tracks), figsize=(len(tracks) * 2, 8))

        # Plotting tracks
        for i in range(len(tracks)):
            ax[i].plot(df[tracks[i]], df['MD'])
            ax[i].grid()
            ax[i].invert_yaxis()
            buffer = (max(df['MD']) - min(df['MD'])) / 20
            ax[i].set_ylim(max(df['MD']) + buffer, min(df['MD']) - buffer)

        return fig, ax

    def plot_well_log_along_path(self,
                                 log: str,
                                 coordinates: pd.DataFrame,
                                 spacing: float = 0.5,
                                 radius_factor: float = 75):
        """

        Parameters
        __________

        """
        # Importing pyvista
        try:
            import pyvista as pv
        except ModuleNotFoundError:
            ModuleNotFoundError('PyVista package not installed')

        if not {'Northing', 'Easting', 'True Vertical Depth Below Sea Level'}.issubset(coordinates.columns):
            raise ValueError('The coordinates DataFrame must contain a northing, easting and true vertical depth '
                             'below sea level column')

        coordinates = coordinates[['Easting', 'Northing', 'True Vertical Depth Below Sea Level']].to_numpy()

        logs = self.df.reset_index()[['MD', log]]

        points = resample_between_well_deviation_points(coordinates=coordinates,
                                                        spacing=spacing)

        # polyline_well_path = polyline_from_points(points=coordinates)

        polyline_well_path_resampled = pv.Spline(points)

        points_along_spline = get_points_along_spline(spline=polyline_well_path_resampled,
                                                      dist=logs['MD'].values)

        polyline_along_spline = polyline_from_points(points=points_along_spline)

        polyline_along_spline['values'] = logs[log].values

        tube_along_spline = polyline_along_spline.tube(scalars='values',
                                                       radius_factor=radius_factor)

        return tube_along_spline


def resample_between_well_deviation_points(coordinates: np.ndarray,
                                           spacing: Union[float, int]) -> np.ndarray:
    """Resample between points that define the path of a well.

    Parameters
    __________
        coordinates: np.ndarray
            Nx3 Numpy array containing the X, Y, and Z coordinates that define the path of a well.

    Returns
    _______
         points_resampled: np.ndarray
            Resampled points along a well.

    .. versionadded:: 1.0.x

    """

    # Checking that the coordinates are provided as np.ndarray
    if not isinstance(coordinates, np.ndarray):
        raise TypeError('Coordinates must be provided as NumPy Array')

    # Checking that three coordinates are provided for each point
    if coordinates.shape[1] != 3:
        raise ValueError('Three coordinates X, Y, and Z must be provided for each point')

        # Creating list for storing points
    list_points = []

    # Iterating over points and creating additional points between all other points
    for i in range(len(coordinates) - 1):
        dist = np.linalg.norm(coordinates[i] - coordinates[i + 1])
        num_points = int(dist // spacing)
        points = np.linspace(coordinates[i], coordinates[i + 1], num_points + 1)
        list_points.append(points)

    # Converting lists of points into np.ndarray
    points_resampled = np.array([item for sublist in list_points for item in sublist])

    return points_resampled


def polyline_from_points(points: np.ndarray):
    """Create PyVista PolyLine from points

    Parameters
    __________

        points: np.ndarray
            Points defining the PolyLine

    Return
    ______

        poly: pv.core.pointset.PolyData

    .. versionadded:: 1.0.x

    """

    # Importing pyvista
    try:
        import pyvista as pv
    except ModuleNotFoundError:
        ModuleNotFoundError('PyVista package not installed')

    # Checking that the points are of type PolyData Pointset
    if not isinstance(points, np.ndarray):
        raise TypeError('The points must be provided as NumPy Array')

    # Creating PolyData Object
    poly = pv.PolyData()

    # Assigning points
    poly.points = points

    # Creating line values
    the_cell = np.arange(0, len(points), dtype=np.int_)
    the_cell = np.insert(the_cell, 0, len(points))

    # Assigning values to PolyData
    poly.lines = the_cell

    return poly


def get_points_along_spline(spline,
                            dist: np.ndarray):
    """Return the closest point on the spline a given a length along a spline.

    Parameters
    __________

        spline: pv.core.pointset.PolyData
            Spline with the resampled vertices

        dist: np.ndarray
            np.ndarray containing the measured depths (MD) of values along the well path

    Returns
    _______

        spline.points[idx_list]: pv.core.pyvista_ndarray.pyvista_ndarray
            PyVista Array containing the selected points

    .. versionadded:: 1.0.x

    """

    # Importing pyvista
    try:
        import pyvista as pv
    except ModuleNotFoundError:
        ModuleNotFoundError('PyVista package not installed')

    # Checking that the spline is a PyVista PolyData Pointset
    if not isinstance(spline, pv.core.pointset.PolyData):
        raise TypeError('The well path/the spline must be provided as PyVista PolyData Pointset')

    # Checking that the distances are provided as np.ndarray
    if not isinstance(dist, np.ndarray):
        raise TypeError('The distances must be provided as np.ndarray')

    # Creating list for storing indices
    idx_list = []

    # Getting index of spline that match with a measured value and append index to list of indices
    for distance in dist:
        idx = np.argmin(np.abs(spline.point_data['arc_length'] - distance))
        idx_list.append(idx)

    points = spline.points[idx_list]

    return points


def resample_log(line: Union[gpd.GeoDataFrame, LineString],
                 resampling: int,
                 resampling_start=0,
                 resampling_end=None,
                 rounding_precision=5,
                 ) -> gpd.GeoDataFrame:
    # Extracting Linestring from gdf
    if isinstance(line, gpd.GeoDataFrame):
        line = line.geometry.iloc[0]

    x = [coords[0] for coords in list(line.coords)]
    y = [coords[1] for coords in list(line.coords)]

    if not resampling_end:
        resampling_end = np.negative(np.floor(y[-1]), where=False)

    linestrings = [LineString([(min(x),
                                y_sample),
                               (max(x),
                                y_sample)]) for y_sample in np.arange(resampling_start,
                                                                      resampling_end,
                                                                      -resampling)]

    points = [
        shapely.wkt.loads(shapely.wkt.dumps(line.intersection(line_intersect), rounding_precision=rounding_precision))
        for line_intersect in linestrings if not line.intersection(line_intersect).is_empty]

    gdf_resampled = gpd.GeoDataFrame(geometry=points)
    gdf_resampled['X'] = gdf_resampled.geometry.centroid.x
    gdf_resampled['Y'] = np.round(gdf_resampled.geometry.centroid.y, 1)

    gdf_resampled = pd.concat([pd.DataFrame.from_dict(
        {'geometry': Point(x[0], y[0]), 'X': [x[0]], 'Y': [y[0]]}, orient='columns'),
                               gdf_resampled,
                               pd.DataFrame.from_dict(
                                   {'geometry': Point(x[-1], y[-1]), 'X': [x[-1]], 'Y': [y[-1]]},
                                   orient='columns')
                               ], ignore_index=True)

    return gdf_resampled
