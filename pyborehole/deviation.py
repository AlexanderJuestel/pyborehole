from pyborehole.borehole import Borehole
from typing import Union
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Deviation(Borehole):
    """Class to initiate a Deviation object.

    Parameters
    __________
        path : str
            Path to the deviation file, e.g. ``path='Well_deviation.csv'``.
        delimiter : str
            Delimiter to read the deviation file correctly, e.g. ``delimiter=';'``.
        step : float, default: ``5``
                Step for resampling the deviation data, e.g. ``step=5``.
        md_column : str, default: ``'MD'``
                Column containing the measured depths.
        dip_column : str, default: ``'DIP'``
            Column containing the dip values.
        azimuth_column : str, default: ``'AZI'``
            Column containing the azimuth values.

    Raises
    ______
        TypeError
            If the wrong input data types are provided.

    Examples
    ________
        >>> borehole.add_deviation(path='Deviation.csv', delimiter=';', md_column='MD', dip_column='DIP', azimuth_column='AZI')
        >>> borehole.deviation.deviation_df
            Measured Depth  Inclination  Azimuth
        0   0.05            0.0          0.0
        1   0.10            0.0          0.0
        2   0.15            0.0          0.0

    .. versionadded:: 0.0.1
    """

    def __init__(self,
                 borehole,
                 path: Union[str, pd.DataFrame],
                 delimiter: str,
                 step: Union[float, int] = 5,
                 md_column: str = 'MD',
                 dip_column: str = 'DIP',
                 azimuth_column: str = 'AZI'):
        """

        Parameters
        __________
            path : str
                Path to the deviation file, e.g. ``path='Well_Deviation.csv'``.
            delimiter : str
                Delimiter to read the deviation file correctly, e.g. ``delimiter=';'``.
            step : float
                    Step for resampling the deviation data, e.g. ``step=5``.
            md_column : str, default: ``'MD'``
                    Column containing the measured depths, e.g. ``md_column='MD'``.
            dip_column : str, default: ``'DIP'``
                Column containing the dip values, e.g. ``dip_column='DIP'``.
            azimuth_column : str, default: ``'AZI'``
                Column containing the azimuth values, e.g. ``azimuth_column='AZI'``.

        Raises
        ______
            TypeError
                If the wrong input data types are provided.

        Examples
        ________
            >>> borehole.add_deviation(path='Deviation.csv', delimiter=';', md_column='MD', dip_column='DIP', azimuth_column='AZI')
            >>> borehole.deviation.deviation_df
                Measured Depth  Inclination  Azimuth
            0   0.05            0.0          0.0
            1   0.10            0.0          0.0
            2   0.15            0.0          0.0

        .. versionadded:: 0.0.1

        """
        # Checking that the path is of type str or a Pandas DataFrame
        if not isinstance(path, (str, pd.DataFrame)):
            raise TypeError('path must be provided as string or Pandas DataFrame')

        # Checking that the delimiter is of type string
        if not isinstance(delimiter, str):
            raise TypeError('delimiter must be of type string')

        # Checking that the step is of type float or int
        if not isinstance(step, (float, int)):
            raise TypeError('step must be provided as float or int')

        # Checking that the md_column is of type str
        if not isinstance(md_column, str):
            raise TypeError('md_column must be provided as str')

        # Checking that the dip_column is of type str
        if not isinstance(dip_column, str):
            raise TypeError('dip_column must be provided as str')

        # Checking that the azimuth_column is of type str
        if not isinstance(azimuth_column, str):
            raise TypeError('azimuth_column must be provided as str')

        # Checking that the DataFrame contains the columns
        if isinstance(path, pd.DataFrame):
            if not {md_column, dip_column, azimuth_column}.issubset(path.columns):
                raise ValueError('Provided columns are not within the DataFrame')

        # Importing wellpathpy
        try:
            import wellpathpy as wp
        except ModuleNotFoundError:
            ModuleNotFoundError('wellpathpy package not installed')

        # Opening deviation file
        if isinstance(path, str):
            md, inc, azi = wp.read_csv(fname=path,
                                       delimiter=delimiter)

        # Opening Pandas DataFrame
        if isinstance(path, pd.DataFrame):
            md = path[md_column].values
            inc = path[dip_column].values
            azi = path[azimuth_column].values

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

        self.x = borehole.x
        self.y = borehole.y
        self.z = borehole.altitude_above_sea_level

    def add_origin_to_desurveying(self,
                                  x: Union[float, int] = None,
                                  y: Union[float, int] = None,
                                  z: Union[float, int] = None):
        """Add origin to desurveying.

        Parameters
        __________
            x : Union[float, int]
                X-Coordinate of the origin, e.g. ``x=1000``.
            y : Union[float, int]
                Y-Coordinate of the origin, e.g. ``y=1000``.
            z : Union[float, int]
                Altitude of the origin, e.g. ``z=200``.

        Raises
        ______
            TypeError
                If the wrong input data types are provided.

        Examples
        ________
            >>> borehole.deviation.add_origin_to_desurveying(x=100, y=100, z=000)

        .. versionadded:: 0.0.1

        """
        # Checking that the x coordinate is of type float or int
        if not isinstance(x, (float, int, type(None))):
            raise TypeError('X coordinate must be provided as float or int')

        # Checking that the y coordinate is of type float or int
        if not isinstance(y, (float, int, type(None))):
            raise TypeError('Y coordinate must be provided as float or int')

        # Checking that the z coordinate is of type float or int
        if not isinstance(z, (float, int, type(None))):
            raise TypeError('Z coordinate must be provided as float or int')

        # Setting coordinates
        if not x:
            x = self.x
        if not y:
            y = self.y
        if not z:
            z = self.z

        # Adding the X coordinate
        self.desurveyed_df['Northing'] = self.desurveyed_df['Northing_rel'] + y

        # Adding the Y coordinate
        self.desurveyed_df['Easting'] = self.desurveyed_df['Easting_rel'] + x

        # Adding the Z coordinate
        self.desurveyed_df['True Vertical Depth Below Sea Level'] = z - self.desurveyed_df['True Vertical Depth']

    def plot_deviation_polar_plot(self,
                                  c: np.ndarray = None,
                                  vmin: Union[float, int] = None,
                                  vmax: Union[float, int] = None):
        """Add polar plot representing the deviation of a borehole.

        Parameters
        __________
            c : np.ndarray
                Array for coloring the well path.
            vmin : Union[float, int]
                Minimum value for colormap.
            vmax : Union[float, int]
                Maximum value for colormap.

        Raises
        ______
            TypeError
                If the wrong input data types are provided.

        Examples
        ________
            >>> borehole.deviation.plot_deviation_polar_plot()

        .. versionadded:: 0.0.1

        """
        # Checking that the colors are provided as arrays
        if not isinstance(c, np.ndarray):
            raise TypeError('Color array must be provided as NumPy array')

        # Checking that vmin is provided as float or int
        if not isinstance(vmin, (float, int)):
            raise TypeError('vmin must be provided as float or int')

        # Checking that vmax is provided as float or int
        if not isinstance(vmax, (float, int)):
            raise TypeError('vmax must be provided as float or int')

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
                          elev: Union[float, int] = 45,
                          azim: Union[float, int] = 45,
                          roll: Union[float, int] = 0):
        """Create 3D Deviation Plot.

        Parameters
        __________
            elev : Union[float, int], default: ``45``
                Elevation angle for view, e.g. ``elev=45``.
            azim : Union[float, int], default: ``45``
                Azimuth angle for view, e.g. ``azim=45``.
            roll : Union[float, int], default: ``0``
                Rolling angle for view, e.g. ``roll=0``.

        Raises
        ______
            TypeError
                If the wrong input data types are provided.

        Examples
        ________
            >>> borehole.deviation.plot_deviation_3d()

        .. versionadded:: 0.0.1

        """
        # Checking that the elevation is provided as float or int
        if not isinstance(elev, (float, int)):
            raise TypeError('Elevation must be provided as float or int')

        #  Checking that the azimuth is provided as float or int
        if not isinstance(azim, (float, int)):
            raise TypeError('Azimuth must be provided as float or int')

        # Checking that the roll is provided as float or int
        if not isinstance(roll, (float, int)):
            raise TypeError('Roll must be provided as float or int')

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
                          radius: Union[float, int] = 10,
                          x: Union[float, int] = 0,
                          y: Union[float, int] = 0,
                          z: Union[float, int] = 0):
        """Get borehole tube.

        Parameters
        __________
            radius : Union[float, int], default: ``10``
                Radius of the borehole tube, e.g. ``radius=10``.
            x : Union[float, int], default: ``0``
                X-coordinate of the borehole, e.g. ``x=1000``.
            y : Union[float, int], default: ``0``
                Y-coordinate of the borehole, e.g. ``y=1000``.
            z : Union[float, int], default: ``0``
                Z-coordinate of the borehole, e.g. ``y=100``.

        Raises
        ______
            TypeError
                If the wrong input data types are provided.

        Examples
        ________
            >>> borehole.deviation.get_borehole_tube(radius=10)

        .. versionadded:: 0.0.1
        """
        # Checking that the radius is provided as float or int
        if not isinstance(radius, (float, int)):
            raise TypeError('radius must be provided as float or int')

        # Checking that the x coordinate of the borehole is provided as float or int
        if not isinstance(x, (float, int)):
            raise TypeError('x coordinate must be provided as float or int')

        # Checking that the y coordinate of the borehole is provided as float or int
        if not isinstance(y, (float, int)):
            raise TypeError('y coordinate must be provided as float or int')

        # Checking that the y coordinate of the borehole is provided as float or int
        if not isinstance(y, (float, int)):
            raise TypeError('y coordinate must be provided as float or int')

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
                                         -self.tvd + z])
        # Creating tube
        tube = spline.tube(radius=radius)

        # Assigning depth values
        tube['TVD'] = tube.points[:, 2]

        return tube
