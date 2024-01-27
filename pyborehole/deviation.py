import pandas as pd
import numpy as np
from typing import Union
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection


class Deviation:
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
        add_origin: bool, default: ``True``
                Boolean value to add the location of the borehole to survey DataFrames.

    Returns
    _______
        Deviation
            Deviation Object.

    Raises
    ______
        TypeError
            If the wrong input data types are provided.

    Examples
    ________
        >>> from pyborehole.borehole import Borehole
        >>> borehole = Borehole(name='Weisweiler R1')
        >>> borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland', location=(6.313031, 50.835676), crs='EPSG:4326', altitude_above_sea_level=136, borehole_id='DABO123456')
        >>> borehole.add_deviation(path='Deviation.csv', delimiter=';', md_column='MD', dip_column='DIP', azimuth_column='AZI')
        >>> borehole.deviation.deviation_df
            Measured Depth  Inclination  Azimuth
        0   0.05            0.0          0.0
        1   0.10            0.0          0.0
        2   0.15            0.0          0.0

    See Also
    ________
        add_litholog : Add LithoLog to the Borehole Object.
        add_well_design : Add Well Design to the Borehole Object.
        add_well_logs : Add Well Logs to the Borehole Object.
        add_well_tops : Add Well Tops to the Borehole Object.

    .. versionadded:: 0.0.1
    """

    def __init__(self,
                 borehole,
                 path: Union[str, pd.DataFrame],
                 delimiter: str,
                 step: Union[float, int] = 5,
                 md_column: str = 'MD',
                 dip_column: str = 'DIP',
                 azimuth_column: str = 'AZI',
                 add_origin: bool = True):
        """Class to initiate a Deviation object.

        Parameters
        __________
            borehole : Borehole
                Borehole Object.
            path : str
                Path to the deviation file, e.g. ``path='Well_Deviation.csv'``.
            delimiter : str
                Delimiter to read the deviation file correctly, e.g. ``delimiter=';'``.
            step : float, default: ``5``
                    Step for resampling the deviation data, e.g. ``step=5``.
            md_column : str, default: ``'MD'``
                    Column containing the measured depths, e.g. ``md_column='MD'``.
            dip_column : str, default: ``'DIP'``
                Column containing the dip values, e.g. ``dip_column='DIP'``.
            azimuth_column : str, default: ``'AZI'``
                Column containing the azimuth values, e.g. ``azimuth_column='AZI'``.
            add_origin: bool, default: ``True``
                Boolean value to add the location of the borehole to survey DataFrames.

        Returns
        _______
            Deviation
                Deviation Object.

        Raises
        ______
            TypeError
                If the wrong input data types are provided.

        Examples
        ________
            >>> from pyborehole.borehole import Borehole
            >>> borehole = Borehole(name='Weisweiler R1')
            >>> borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland', location=(6.313031, 50.835676), crs='EPSG:4326', altitude_above_sea_level=136, borehole_id='DABO123456')
            >>> borehole.add_deviation(path='Deviation.csv', delimiter=';', md_column='MD', dip_column='DIP', azimuth_column='AZI')
            >>> borehole.deviation.deviation_df
                Measured Depth  Inclination  Azimuth
            0   0.05            0.0          0.0
            1   0.10            0.0          0.0
            2   0.15            0.0          0.0

        See Also
        ________
            add_origin_to_desurveying : Add origin to desurveying.
            plot_deviation_polar_plot : Add polar plot representing the deviation of a borehole.
            plot_deviation_3d : Create 3D Deviation Plot.
            get_borehole_tube : Get borehole tube.

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

        # Checking that add_origin is provided as boolean value
        if not isinstance(add_origin, bool):
            raise TypeError('add_origin must be provided as boolean value')

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
        if add_origin:
            if borehole.crs == 'EPSG:4326':
                raise ValueError('Please use location coordinates in a cartesian coordinate system for the borehole when adding the origin to desurveyed borehole')
            self.northing_rel = pos.northing + borehole.y
            self.easting_rel = pos.easting + borehole.x
        else:
            self.northing_rel = pos.northing
            self.easting_rel = pos.easting

        # Calculating dip and azimuth
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

        # Assigning attributes
        self.crs = borehole.crs
        self._borehole = borehole

        self.northing = None
        self.easting = None
        self.tvdss = None

    def add_origin_to_desurveying(self,
                                  x: Union[float, int] = None,
                                  y: Union[float, int] = None,
                                  z: Union[float, int] = None):
        """Add origin to desurveying.

        Parameters
        __________
            x : Union[float, int], default: ``None``
                X-Coordinate of the origin, e.g. ``x=1000``.
            y : Union[float, int], default: ``None``
                Y-Coordinate of the origin, e.g. ``y=1000``.
            z : Union[float, int], default: ``None``
                Altitude of the origin, e.g. ``z=200``.

        Raises
        ______
            ValueError
                If a non-Cartesian coordinate system is used.
            TypeError
                If the wrong input data types are provided.

        Examples
        ________
            >>> from pyborehole.borehole import Borehole
            >>> borehole = Borehole(name='Weisweiler R1')
            >>> borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland', location=(6.313031, 50.835676), crs='EPSG:4326', altitude_above_sea_level=136, borehole_id='DABO123456')
            >>> borehole.add_deviation(path='Deviation.csv', delimiter=';', md_column='MD', dip_column='DIP', azimuth_column='AZI')
            >>> borehole.deviation.add_origin_to_desurveying(x=100, y=100, z=000)

        See Also
        ________
            plot_deviation_polar_plot : Add polar plot representing the deviation of a borehole.
            plot_deviation_3d : Create 3D Deviation Plot.
            get_borehole_tube : Get borehole tube.

        .. versionadded:: 0.0.1
        """
        # Raising a ValueError if the CRS is WGS84
        if self.crs == 'EPSG:4326':
            raise ValueError('Please use location coordinates in a cartesian coordinate system for the borehole when adding the origin to desurveyed borehole')

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
            x = self._borehole.x
        if not y:
            y = self._borehole.y
        if not z:
            z = self._borehole.altitude_above_sea_level

        # Adding the X coordinate
        self.desurveyed_df['Northing'] = self.desurveyed_df['Northing_rel'] + y

        # Adding the Y coordinate
        self.desurveyed_df['Easting'] = self.desurveyed_df['Easting_rel'] + x

        # Adding the Z coordinate
        self.desurveyed_df['True Vertical Depth Below Sea Level'] = z - self.desurveyed_df['True Vertical Depth']

        # Creating Data Dict
        data_dict = {'Northing': [self.desurveyed_df['Northing'].values],
                     'Easting': [self.desurveyed_df['Easting'].values],
                     'True Vertical Depth Below Sea Level': [self.desurveyed_df['True Vertical Depth Below Sea Level'].values],
                     }
        self._borehole.update_df(data_dict=data_dict)

        # Setting attributes
        self.northing = self.desurveyed_df['Northing'].values
        self.easting = self.desurveyed_df['Easting'].values
        self.tvdss = self.desurveyed_df['True Vertical Depth Below Sea Level'].values

    def plot_deviation_polar_plot(self,
                                  c: np.ndarray = None,
                                  vmin: Union[float, int] = None,
                                  vmax: Union[float, int] = None,
                                  cmap: str = 'viridis'):
        """Add polar plot representing the deviation of a borehole.

        Parameters
        __________
            c : np.ndarray, default: ``None``.
                Array for coloring the well path.
            vmin : Union[float, int], default: ``None``.
                Minimum value for colormap, e.g. ``vmin=0``.
            vmax : Union[float, int], default: ``None``.
                Maximum value for colormap, e.g. ``vmax=100``.
            cmap : str, default: ``'viridis'``
                Name of the colormap to be used, e.g. ``cmap='viridis'``.

        Raises
        ______
            TypeError
                If the wrong input data types are provided.

        Examples
        ________
            >>> from pyborehole.borehole import Borehole
            >>> borehole = Borehole(name='Weisweiler R1')
            >>> borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland', location=(6.313031, 50.835676), crs='EPSG:4326', altitude_above_sea_level=136, borehole_id='DABO123456')
            >>> borehole.add_deviation(path='Deviation.csv', delimiter=';', md_column='MD', dip_column='DIP', azimuth_column='AZI')
            >>> borehole.deviation.plot_deviation_polar_plot()

        See Also
        ________
            add_origin_to_desurveying : Add origin to desurveying.
            plot_deviation_3d : Create 3D Deviation Plot.
            get_borehole_tube : Get borehole tube.

        .. versionadded:: 0.0.1
        """
        # Checking that the colors are provided as arrays
        if not isinstance(c, (np.ndarray, type(None))):
            raise TypeError('Color array must be provided as NumPy array')

        # Checking that vmin is provided as float or int
        if not isinstance(vmin, (float, int, type(None))):
            raise TypeError('vmin must be provided as float or int')

        # Checking that vmax is provided as float or int
        if not isinstance(vmax, (float, int, type(None))):
            raise TypeError('vmax must be provided as float or int')

        # Checking that the name of the cmap is provided as string
        if not isinstance(cmap, (str, type(None))):
            raise TypeError('The name of the cmap must be provided as string')

        # Creating plot
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

        # Setting zero to North
        ax.set_theta_zero_location('N')

        # Counting clockwise
        ax.set_theta_direction(-1)

        # Plotting
        if c is not None:
            # Creating the Line Segments
            xy = np.vstack([self.az,
                            self.radius]).T.reshape(-1,
                                                    1,
                                                    2)

            # Stacking Coordinates
            segments = np.hstack([xy[:-1],
                                  xy[1:]])

            # Creating LineCollection
            coll = LineCollection(segments,
                                  cmap=cmap)

            # Setting the data array
            coll.set_array(c)

            # Adding collection to axis
            ax.add_collection(coll)

            # Setting view
            ax.autoscale_view()

            # Setting rlims
            ax.set_rlim(0, 1.05*np.max(self.radius))

        else:
            ax.plot(self.az,
                    self.radius)

            # Setting rlims
            ax.set_rlim(0, 1.05 * np.max(self.radius))

        return fig, ax

    def plot_deviation_3d(self,
                          elev: Union[float, int] = 45,
                          azim: Union[float, int] = 45,
                          roll: Union[float, int] = 0,
                          relative: bool = False):
        """Create 3D Deviation Plot.

        Parameters
        __________
            elev : Union[float, int], default: ``45``
                Elevation angle for view, e.g. ``elev=45``.
            azim : Union[float, int], default: ``45``
                Azimuth angle for view, e.g. ``azim=45``.
            roll : Union[float, int], default: ``0``
                Rolling angle for view, e.g. ``roll=0``.
            relative : bool, default: ``False``
                Boolean value to plot the plot with relative coordinates, e.g. ``relative=False``.

        Returns
        _______
            fig : matplotlib.figure
                Matplotlib figure.
            ax : matplotlib.axes.Axes
                Matplotlib axis.

        Raises
        ______
            TypeError
                If the wrong input data types are provided.

        Examples
        ________
            >>> from pyborehole.borehole import Borehole
            >>> borehole = Borehole(name='Weisweiler R1')
            >>> borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland', location=(6.313031, 50.835676), crs='EPSG:4326', altitude_above_sea_level=136, borehole_id='DABO123456')
            >>> borehole.add_deviation(path='Deviation.csv', delimiter=';', md_column='MD', dip_column='DIP', azimuth_column='AZI')
            >>> borehole.deviation.plot_deviation_3d()

        See Also
        ________
            add_origin_to_desurveying : Add origin to desurveying.
            plot_deviation_polar_plot : Add polar plot representing the deviation of a borehole.
            get_borehole_tube : Get borehole tube.

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

        # Checking that the relative value is provided as bool
        if not isinstance(relative, bool):
            raise TypeError('The relative value must be provided as bool')

        # Creating figure
        fig, ax = plt.subplots(subplot_kw={'projection': '3d'})

        # TODO: Add LineCollection coloring

        # Plotting
        if relative:
            ax.plot(self.easting_rel,
                    self.northing_rel,
                    -self.tvd)
        else:
            ax.plot(self.easting,
                    self.northing,
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
                          z: Union[float, int] = 0,
                          relative: bool = False):
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
            relative : bool, default: ``False``
                Boolean value to plot the plot with relative coordinates, e.g. ``relative=False``.

        Returns
        _______
            tube : pv.Tube
                PyVista Tube of the borehole.

        Raises
        ______
            TypeError
                If the wrong input data types are provided.

        Examples
        ________
            >>> from pyborehole.borehole import Borehole
            >>> borehole = Borehole(name='Weisweiler R1')
            >>> borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland', location=(6.313031, 50.835676), crs='EPSG:4326', altitude_above_sea_level=136, borehole_id='DABO123456')
            >>> borehole.add_deviation(path='Deviation.csv', delimiter=';', md_column='MD', dip_column='DIP', azimuth_column='AZI')
            >>> borehole.deviation.get_borehole_tube(radius=10)

        See Also
        ________
            add_origin_to_desurveying : Add origin to desurveying.
            plot_deviation_polar_plot : Add polar plot representing the deviation of a borehole.
            plot_deviation_3d : Create 3D Deviation Plot.

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

        # Checking that the relative value is provided as bool
        if not isinstance(relative, bool):
            raise TypeError('The relative value must be provided as bool')

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
        if relative:
            spline = lines_from_points(np.c_[self.easting_rel + x,
                                             self.northing_rel + y,
                                             -self.tvd + z])
        else:
            spline = lines_from_points(np.c_[self.easting + x,
                                             self.northing + y,
                                             -self.tvd + z])

        # Creating tube
        tube = spline.tube(radius=radius)

        # Assigning depth values
        tube['TVD'] = tube.points[:, 2]

        return tube
