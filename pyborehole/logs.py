import pandas as pd
import matplotlib.pyplot as plt
from typing import Union, List
import numpy as np
import geopandas as gpd
import shapely
from shapely.geometry import Point, LineString
from matplotlib.patches import Rectangle
import copy


class LASLogs:
    """Class to initiate a Well Log Object.

    Parameters
    __________
        borehole : Borehole
            Borehole object.
        path : str
            Path to the well logs, e.g. ``path='logs.las'``.

    Returns
    _______
        LASLogs
            Well Log Object.

    Raises
    ______
        TypeError
            If the wrong input data types are provided.

    Examples
    ________
        >>> import pyborehole
        >>> from pyborehole.borehole import Borehole
        >>> borehole = Borehole(name='Weisweiler R1')
        >>> borehole.init_properties(location=(6.313031, 50.835676), crs='EPSG:4326', altitude_above_sea_level=136)
        >>> borehole.add_well_logs(path='Well_logs.las')
        >>> borehole.logs.well_header
            mnemonic   unit   value               descr
        0   STRT       M      100.0               Log Start Depth
        1   STOP       M      0.05                Log Stop Depth
        2   STEP       M      -0.05               Log Increment
        3   NULL              -999.25             Null Value
        4   COMP              RWE Power           Company Name
        5   WELL              EB 1                Well Name
        6   FLD               KW Weisweiler       Field Name
        7   LOC                                   Location
        8   PROV                                  Province
        9   SRVC                                  Service Company
        10  DATE              26-Oct-2023         Date
        11  UWI                                   Unique Well ID

    See Also
    ________
        add_deviation : Add deviation to the Borehole Object.
        add_litholog : Add LithoLog to the Borehole Object.
        add_well_design : Add Well Design to the Borehole Object.
        add_well_tops : Add Well Tops to the Borehole Object.

    .. versionadded:: 0.0.1
    """

    def __init__(self,
                 borehole,
                 path: str):
        """Class to initiate a Well Log Object.

        Parameters
        __________
            borehole : Borehole
                Borehole object.
            path : str
                Path to the well logs, e.g. ``path='logs.las'``.

        Returns
        _______
            LASLogs
                Well Log Object.

        Raises
        ______
            TypeError
                If the wrong input data types are provided.

        Examples
        ________
            >>> import pyborehole
            >>> from pyborehole.borehole import Borehole
            >>> borehole = Borehole(name='Weisweiler R1')
            >>> borehole.init_properties(location=(6.313031, 50.835676), crs='EPSG:4326', altitude_above_sea_level=136)
            >>> borehole.add_well_logs(path='Well_logs.las')
            >>> borehole.logs.well_header
                mnemonic   unit   value               descr
            0   STRT       M      100.0               Log Start Depth
            1   STOP       M      0.05                Log Stop Depth
            2   STEP       M      -0.05               Log Increment
            3   NULL              -999.25             Null Value
            4   COMP              RWE Power           Company Name
            5   WELL              EB 1                Well Name
            6   FLD               KW Weisweiler       Field Name
            7   LOC                                   Location
            8   PROV                                  Province
            9   SRVC                                  Service Company
            10  DATE              26-Oct-2023         Date
            11  UWI                                   Unique Well ID

        .. versionadded:: 0.0.1
        """
        # Importing lasio
        try:
            import lasio
        except ModuleNotFoundError:
            ModuleNotFoundError('lasio package not installed')

        # Checking that the path is provided as string
        if not isinstance(path, str):
            raise TypeError('The path must be provided as string')

        # Opening LAS file
        las = lasio.read(path)

        # Extracting DataFrame from LAS file
        self.df = las.df().sort_index()

        # Changing the name of the index column and reset index
        self.df.index.rename('DEPTH', inplace=True)
        self.df = self.df.reset_index()

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

        self.well_tops = borehole.well_tops
        self.has_well_tops = borehole.has_well_tops
        self.has_well_design = borehole.has_well_design
        self.well_design = borehole.well_design

    def plot_well_logs(self,
                       tracks: Union[str, list],
                       depth_column: str = 'MD',
                       colors: Union[str, list] = None,
                       add_well_tops: bool = False,
                       add_well_design: bool = False,
                       fill_between: int = None,
                       add_net_to_gross: int = None):
        """Plot well logs.

        Parameters
        __________

        tracks : Union[str, list]
            Name/s of the logs to be plotted, e.g. ``tracks='SGR'`` or ``tracks=['SGR', 'K'].
        depth_column : str
            Name of the column holding the depths, e.g. ``depth_column='MD'``.
        colors : Union[str, list]
            Colors of the logs, e.g. ``colors='black'`` or ``colors=['black', 'blue'].
        add_well_tops : bool, default = False
            Boolean to add well tops to the plot.
        add_well_design : bool, default = False
            Boolean to add well design to the plot.
        fill_between : int, default: ``None``
            Number of the axis to fill.
        add_net_to_gross : int, default: ``None``
            Number of axis to fill with the net to gross values.

        Returns
        _______
            fig : matplotlib.figure
                Matplotlib Figure.
            ax : matplotlib.axes.Axes
                Matplotlib Axes.

        Raises
        ______
            TypeError
                If the wrong input data types are provided.
            ValueError
                If no well tops are provided but add_well_tops is set to True.
            ValueError
                If the wrong column names are provided

        Examples
        ________
            >>> import pyborehole
            >>> from pyborehole.borehole import Borehole
            >>> borehole = Borehole(name='Weisweiler R1')
            >>> borehole.init_properties(location=(6.313031, 50.835676), crs='EPSG:4326', altitude_above_sea_level=136)
            >>> borehole.add_well_logs(path='Well_logs.las')
            >>> borehole.logs.plot_well_logs(tracks=['SGR', 'CAL'], depth_column='DEPTH', colors=['black', 'red'])

        See Also
        ________
            plot_well_log_along_path : Plot well log along path.
            calculate_vshale : Calculate Shale Volume.
            calculate_vshale_linear : Calculate Shale Volume linear method.
            calculate_net_to_gross : Calculate net to gross.

        .. versionadded:: 0.0.1
        """
        # Checking that the tracks are provided as list or string
        if not isinstance(tracks, (list, str)):
            raise TypeError('The track/s must bei either provided as str or a list of strings')

        # Checking that the tracks are in the DataFrame
        if isinstance(tracks, str):
            if not {tracks}.issubset(self.df.columns):
                raise ValueError('The track is not part of the curves')
        elif isinstance(tracks, list):
            if not all({track}.issubset(self.df.columns) for track in tracks):
                raise ValueError('Not all tracks are part of the curves')

        # Checking that the depth column is of type string
        if not isinstance(depth_column, str):
            raise TypeError('Depth_column must be provided as string')

        # Checking that the depth column is in the DataFrame
        if not {depth_column}.issubset(self.df):
            raise ValueError('The depth_column is not part of the curves')

        # Checking that the colors are provided as list or string
        if not isinstance(colors, (list, str)):
            raise TypeError('The track/s must bei either provided as str or a list of strings')

        # Checking that the add_well_tops variable is of type bool
        if not isinstance(add_well_tops, bool):
            raise TypeError('The add_well_tops variable must be provided as bool')

        # Checking that the add_well_design variable is of type bool
        if not isinstance(add_well_design, bool):
            raise TypeError('The add_well_design variable must be provided as bool')

        # Checking that the fill_between variable is of type int
        if not isinstance(fill_between, (int, type(None))):
            raise TypeError('The fill_between variable must be provided as int')

        # Checking that the add_net to_gross variable is of type bool
        if not isinstance(add_net_to_gross, (int, type(None))):
            raise TypeError('The add_net_to_gross variable must be provided as int')

        # Selecting tracks
        df = self.df[tracks + [depth_column]].reset_index()

        # Creating plot if tracks is of type string
        if isinstance(tracks, str):
            # Creating plot
            fig, ax = plt.subplots(1, 1, figsize=(1 * 2, 8))

            ax.plot(df[tracks], df[depth_column], color=colors)
            ax.grid()
            ax.invert_yaxis()
            buffer = (max(df[depth_column]) - min(df[depth_column])) / 20
            ax.set_ylim(max(df[depth_column]) + buffer, min(df[depth_column]) - buffer)
            ax.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
            ax.xaxis.set_label_position('top')
            ax.set_xlabel(tracks + ' [%s]' %
                          self.curves[self.curves['original_mnemonic'] == tracks].reset_index(drop=True)['unit'].iloc[
                              0], color='black')
            ax.set_ylabel(depth_column + ' [m]')

            # Fill between curve
            if fill_between:
                left_col_value = np.min(df[tracks].dropna().values)
                right_col_value = np.max(df[tracks].dropna().values)
                span = abs(left_col_value - right_col_value)
                cmap = plt.get_cmap('hot_r')
                color_index = np.arange(left_col_value, right_col_value, span / 100)
                # loop through each value in the color_index
                for index in sorted(color_index):
                    index_value = (index - left_col_value) / span
                    color = cmap(index_value)  # obtain color for color index value
                    ax.fill_betweenx(df[depth_column], df[tracks], left_col_value, where=df[tracks] >= index,
                                     color=color)

            return fig, ax

        # Creating plot if tracks is of type list
        elif isinstance(tracks, list):

            # Helping variable for adding well tops
            if add_well_tops:
                j = 1
            else:
                j = 0

            if add_well_design:
                k = 1
            else:
                k = 0

            # Setting colors
            if not colors:
                colors = [None] * len(tracks)

            # Creating plot
            fig, ax = plt.subplots(1,
                                   len(tracks) + j + k,
                                   figsize=((len(tracks) + j + k) * 1.8, 8),
                                   sharey=True)

            # Adding well tops
            if add_well_tops:
                if not self.has_well_tops:
                    raise ValueError('Please add well tops to the borehole object to plot them')
                else:
                    for index, row in self.well_tops.df.iterrows():
                        ax[0 + k].axhline(row[self.well_tops.df.columns[1]], 0, 1, color='black')
                        ax[0 + k].text(0.05, row[self.well_tops.df.columns[1]] - 1, s=row[self.well_tops.df.columns[0]],
                                       fontsize=6)
                        ax[0 + k].grid()
                        ax[0 + k].axes.get_xaxis().set_ticks([])

            # Adding well design
            if add_well_design:
                if not self.has_well_design:
                    raise ValueError('Please add a well design to the borehole object to plot it')
                else:
                    for key, elem in self.well_design.pipes.items():
                        if elem.pipe_type == 'open hole section':
                            # Plotting open hole section as wavy line
                            y = np.linspace(elem.top, elem.bottom, 1000)
                            x1 = 0.5 * np.sin(y / 2) - elem.inner_diameter + 0.5
                            x2 = 0.5 * np.cos(y / 2 + np.pi / 4) + elem.inner_diameter
                            ax[k].plot(x1, y, color='black')
                            ax[k].plot(x2, y, color='black')
                            # Plotting open hole section as dashed line
                            # ax.plot([elem.inner_diameter,elem.inner_diameter],
                            #        [elem.top, elem.bottom],
                            #        linestyle='--',
                            #        color='black')
                            # ax.plot([-elem.inner_diameter, -elem.inner_diameter],
                            #        [elem.top, elem.bottom],
                            #        linestyle='--',
                            #        color='black')
                        else:
                            ax[k].add_patch(Rectangle(elem.xy, elem.width, elem.height, color="black"))
                            ax[k].add_patch(
                                Rectangle((-1 * elem.xy[0], elem.xy[1]), -1 * elem.width, elem.height, color="black"))

                    # Deep copy of pipes dict
                    x = copy.deepcopy(self.pipes)

                    # Popping open hole section
                    try:
                        type_list = [elem.pipe_type for key, elem in x.items()]
                        index_open_hole = type_list.index('open hole section')
                        key_open_hole = list(x.keys())[index_open_hole]
                        x.pop(key_open_hole)
                    except ValueError:
                        pass

                    # Getting diameters and calculating thickness of cement between each pipe
                    outer_diameters = sorted([elem.outer_diameter for key, elem in x.items()], reverse=False)
                    inner_diameters = sorted([elem.inner_diameter for key, elem in x.items()], reverse=False)
                    thicknesses = [y - x for x, y in zip(outer_diameters[:-1], inner_diameters[1:])]

                    # Sorting pipes
                    pipes_sorted = {k: v for k, v in sorted(x.items(), key=lambda item: item[1].outer_diameter)}

                    # Selecting pies
                    pipes_selected = {k: pipes_sorted[k] for k in list(pipes_sorted)[:len(thicknesses)]}

                    # Plotting top of pipe
                    i = 0
                    for key, elem in pipes_selected.items():
                        i = i
                        ax[k].add_patch(
                            Rectangle((elem.inner_diameter, elem.top), thicknesses[i] + elem.thickness, 1,
                                      color="black"))
                        ax[k].add_patch(Rectangle((-1 * elem.inner_diameter, elem.top),
                                                  -1 * thicknesses[0] - elem.thickness, 1,
                                                  color="black"))
                        i = i + 1

                    # Plotting Casing Shoes
                    for key, elem in self.well_design.pipes.items():
                        if elem.shoe_width is not None:
                            p0 = [elem.outer_diameter, elem.bottom]
                            p1 = [elem.outer_diameter, elem.bottom - elem.shoe_height]
                            p2 = [elem.outer_diameter + elem.shoe_width, elem.bottom]
                            shoe = plt.Polygon([p0, p1, p2], color="black")
                            ax.add_patch(shoe)
                            p0[0] *= -1
                            p1[0] *= -1
                            p2 = [-elem.outer_diameter - elem.shoe_width, elem.bottom]
                            shoe = plt.Polygon([p0, p1, p2], color="black")
                            ax[k].add_patch(shoe)

                    # Adding Casing Cements
                    for key, elem in self.well_design.cements.items():
                        ax[k].fill_between(elem.xvals, elem.tops, elem.bottoms, color="#6b705c", alpha=0.5)
                        ax[k].fill_between(-1 * elem.xvals, elem.tops, elem.bottoms, color="#6b705c", alpha=0.5)

                    # Calculating axes limits
                    top = np.min([elem.top for key, elem in self.well_design.pipes.items()])
                    bottom = np.max([elem.bottom for key, elem in self.well_design.pipes.items()])
                    max_diam = np.max([elem.outer_diameter for key, elem in self.well_design.pipes.items()])

                    # Setting axes limits
                    buffer = (max(df[depth_column]) - min(df[depth_column])) / 20
                    ax[k].set_ylim(max(df[depth_column]) + buffer, min(df[depth_column]) - buffer)
                    ax.set_xlim(-max_diam * 1, max_diam * 1)
                    # ax.invert_yaxis()

                    # Setting axes labels
                    ax.set_xlabel('Diameter [in]')

            # Plotting tracks
            for i in range(len(tracks)):
                ax[i + j + k].plot(df[tracks[i]], df[depth_column], color=colors[i])
                ax[i + j + k].grid()
                ax[i + j + k].invert_yaxis()
                buffer = (max(df[depth_column]) - min(df[depth_column])) / 20
                ax[i + j + k].set_ylim(max(df[depth_column]) + buffer, min(df[depth_column]) - buffer)
                ax[i + j + k].tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
                ax[i + j + k].xaxis.set_label_position('top')
                ax[i + j + k].set_xlabel(tracks[i] + ' [%s]' %
                                         self.curves[self.curves['original_mnemonic'] == tracks[i]].reset_index(
                                             drop=True)[
                                             'unit'].iloc[0],
                                         color='black' if isinstance(colors[i], type(None)) else colors[i])
                ax[0].set_ylabel(depth_column + ' [m]')

            # Fill between curves
            if fill_between is not None:
                left_col_value = np.min(df[tracks[fill_between]].dropna().values)
                right_col_value = np.max(df[tracks[fill_between]].dropna().values)
                span = abs(left_col_value - right_col_value)
                cmap = plt.get_cmap('hot_r')
                color_index = np.arange(left_col_value, right_col_value, span / 100)

                # Dropping duplicate columns if the same track is selected twice
                try:
                    df1 = df[tracks[fill_between]].copy(deep=True)
                    df1 = df1.loc[:, ~df1.columns.duplicated()]
                except AttributeError:
                    df1 = df[tracks[fill_between]].copy(deep=True)

                # loop through each value in the color_index
                for index in sorted(color_index):
                    index_value = (index - left_col_value) / span
                    color = cmap(index_value)  # obtain color for color index value
                    ax[fill_between + j].fill_betweenx(df[depth_column],
                                                       #
                                                       df1.values.flatten(),
                                                       left_col_value,
                                                       where=df1.values.flatten() >= index,
                                                       color=color)

            # Adding net to gross
            if add_net_to_gross is not None:
                if 'N/G' not in self.df.columns:
                    raise ValueError('Net to gross has not been calculated yet')

                ax[add_net_to_gross + j].fill_betweenx(self.df[depth_column],
                                                               self.df[tracks[add_net_to_gross]],
                                                               0,
                                                               where=self.df['N/G'] == 1,
                                                               color='yellow')
                ax[add_net_to_gross + j].fill_betweenx(self.df[depth_column],
                                                               self.df[tracks[add_net_to_gross]],
                                                               0,
                                                               where=self.df['N/G'] == 0,
                                                               color='brown')

            plt.tight_layout()

            return fig, ax

    def plot_well_log_along_path(self,
                                 log: str,
                                 coordinates: pd.DataFrame,
                                 spacing: float = 0.5,
                                 radius_factor: float = 75):
        """Plot well log along path.

        Parameters
        __________


        Raises
        ______
            ModuleNotFoundError
                Raises error if PyVista is not installed.
            TypeError
                If the wrong input data types are provided.
            ValueError
                Raises error if the wrong column names are provided.

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

    def calculate_vshale(self,
                         method: str,
                         column: str,
                         minz: Union[float, int] = None,
                         maxz: Union[float, int] = None,
                         depth_column: str = None):
        """Calculate Shale Volume.

        Parameters
        __________
            method : str
                Method used to calculate the Shale Volume, e.g. ``method='linear'``.
            column : str
                Column of the borehole.logs.df containing the Gamma Ray Value, e.g. ``column='GR'``.
            minz : Union[float, int], default: ``None``
                Minimum Z value.
            maxz : Union[float, int], default: ``None``
                Maximum Z value.
            depth_column : str, default: ``None``
                Name of the column holding the depths, e.g. ``depth_column='MD'``.

        Returns
        _______
            borehole.logs.df : pd.DataFrame
                Log DataFrame with appended Shale Volume.

        Raises
        ______
            TypeError
                If the wrong input data types are provided.
            ValueError
                If a method is chosen that is not available.

        Examples
        ________
            >>> import pyborehole
            >>> from pyborehole.borehole import Borehole
            >>> borehole = Borehole(name='Weisweiler R1')
            >>> borehole.init_properties(location=(6.313031, 50.835676), crs='EPSG:4326', altitude_above_sea_level=136)
            >>> borehole.add_well_logs('Well_Logs.las')
            >>> borehole.logs.calculate_vshale(method='linear', column='GR')

        See Also
        ________
            calculate_vshale_linear : Calculate Shale Volume with the linear method.
            calculate_net_to_gross : Calculate Net to Gross value.

        .. versionadded:: 0.0.1
        """
        # Checking that the method is of type str
        if not isinstance(method, str):
            raise TypeError('The method must be provided as string')

        # Checking that the provided method is in the list of methods
        if method not in ['linear']:
            raise ValueError('Provided method is not implemented')

        # Checking that the column is of type str
        if not isinstance(column, str):
            raise TypeError('The column name must be provided as string')

        # Checking that the minz value is of type float or int
        if not isinstance(minz, (float, int, type(None))):
            raise TypeError('minz must be provided as float or int')

        # Checking that the maxz value is of type float or int
        if not isinstance(maxz, (float, int,type(None))):
            raise TypeError('maxz must be provided as float or int')

        # Selecting method
        if method == 'linear':
            self.calculate_vshale_linear(column=column,
                                         minz=minz,
                                         maxz=maxz,
                                         depth_column=depth_column)

        return self.df

    def calculate_vshale_linear(self,
                                column: str,
                                minz: Union[float, int] = None,
                                maxz: Union[float, int] = None,
                                depth_column: str = None):
        """Calculate Shale Volume with the linear method.

        Parameters
        __________
            column : str
                Column of the borehole.logs.df containing the Gamma Ray Value, e.g. ``column='GR'``.
            minz : Union[float, int], default: ``None``
                Minimum Z value.
            maxz : Union[float, int], default: ``None``
                Maximum Z value.
            depth_column : str, default: ``None``
                Name of the column holding the depths, e.g. ``depth_column='MD'``.

        Raises
        ______
            TypeError
                If the wrong input data types are provided.

        Examples
        ________
            >>> import pyborehole
            >>> from pyborehole.borehole import Borehole
            >>> borehole = Borehole(name='Weisweiler R1')
            >>> borehole.init_properties(location=(6.313031, 50.835676), crs='EPSG:4326', altitude_above_sea_level=136)
            >>> borehole.add_well_logs('Well_Logs.las')
            >>> borehole.logs.calculate_vshale_linear(column='GR')

        See Also
        ________
            calculate_vshale : Calculate Shale Volume.
            calculate_net_to_gross : Calculate Net to Gross value.

        .. versionadded:: 0.0.1
        """
        # Checking that the column is of type str
        if not isinstance(column, str):
            raise TypeError('The column name must be provided as string')

        # Checking that the minz value is of type float or int
        if not isinstance(minz, (float, int, type(None))):
            raise TypeError('minz must be provided as float or int')

        # Checking that the maxz value is of type float or int
        if not isinstance(maxz, (float, int, type(None))):
            raise TypeError('maxz must be provided as float or int')

        # Checking that the depth column is of type string
        if not isinstance(depth_column, (str, type(None))):
            raise TypeError('Depth_column must be provided as string')

        # Cropping DataFrame
        if None not in (minz, maxz):
            df = self.df[(self.df[depth_column] >= minz) & (self.df[depth_column] <= maxz)].copy(deep=True)
        else:
            df = self.df.copy(deep=True)

        # Obtaining min and max Gamma Ray values
        gr_max = df[column].max()
        gr_min = df[column].min()

        # Calculating Shale Volume
        vshale = (df[column] - gr_min) / (gr_max - gr_min)

        # Appending Shale Volume to Borehole Logs DataFrame
        self.df['VShale_Linear'] = vshale

    def calculate_net_to_gross(self,
                               method: str,
                               column: str,
                               cutoff: Union[float, int],
                               minz: Union[float, int] = None,
                               maxz: Union[float, int] = None,
                               depth_column: str = None):
        """Calculate Net to Gross value.

        Parameters
        __________
            method : str
                Method used to calculate the Shale Volume, e.g. ``method='linear'``.
            column : str
                Column of the borehole.logs.df containing the Gamma Ray Value, e.g. ``column='GR'``.
            cutoff : Union[float, int]
                Cutoff value for net to gross estimation, e.g. ``cutoff=0.3``.
            minz : Union[float, int], default: ``None``
                Minimum Z value.
            maxz : Union[float, int], default: ``None``
                Maximum Z value.
            depth_column : str, default: ``None``
                Name of the column holding the depths, e.g. ``depth_column='MD'``.

        Returns
        _______
            net_to_gross : float
                Net to gross value

        Raises
        ______
            TypeError
                If the wrong input data types are provided.

        Examples
        ________
            >>> import pyborehole
            >>> from pyborehole.borehole import Borehole
            >>> borehole = Borehole(name='Weisweiler R1')
            >>> borehole.init_properties(location=(6.313031, 50.835676), crs='EPSG:4326', altitude_above_sea_level=136)
            >>> borehole.add_well_logs('Well_Logs.las')
            >>> borehole.logs.calculate_net_to_gross(method='linear', column='GR', cutoff=0.3)

        See Also
        ________
            calculate_vshale : Calculate Shale Volume.
            calculate_vshale_linear : Calculate Shale Volume with the linear method.

        .. versionadded:: 0.0.1

        """
        # Checking that the method is of type str
        if not isinstance(method, str):
            raise TypeError('The method must be provided as string')

        # Checking that the provided method is in the list of methods
        if method not in ['linear']:
            raise ValueError('Provided method is not implemented')

        # Checking that the column is of type str
        if not isinstance(column, str):
            raise TypeError('The column name must be provided as string')

        # Checking that the cutoff value is of type float or int
        if not isinstance(cutoff, (float, int)):
            raise TypeError('The cutoff value must be provided as float or int')

        # Checking that the minz value is of type float or int
        if not isinstance(minz, (float, int, type(None))):
            raise TypeError('minz must be provided as float or int')

        # Checking that the maxz value is of type float or int
        if not isinstance(maxz, (float, int, type(None))):
            raise TypeError('maxz must be provided as float or int')

        # Checking that the depth column is of type string
        if not isinstance(depth_column, (str, type(None))):
            raise TypeError('Depth_column must be provided as string')

        # Calculating Shale Volume
        self.calculate_vshale(method=method,
                              column=column,
                              minz=minz,
                              maxz=maxz,
                              depth_column=depth_column)

        # Setting column name of Shale Volume
        if method == 'linear':
            column_vshale = 'VShale_Linear'

        #
        def calculating_ng(row,
                           cutoff_value):
            if row <= cutoff_value:
                return 1
            elif cutoff_value < row <= 1:
                return 0
            else:
                return -1

        # Calculating Net to Gross for each Shale Volume value
        self.df['N/G'] = self.df[column_vshale].apply(lambda row: calculating_ng(row,cutoff))
        #self.df['N/G'] = self.df[column_vshale].apply(lambda row: 1 if row <= cutoff else 0)

        # Calculating Net to Gross value
        net_to_gross = self.df['N/G'].value_counts()[0] / (
                self.df['N/G'].value_counts()[0] + self.df['N/G'].value_counts()[1])

        return net_to_gross


class DLISLogs:
    """Class to initiate a Well Log Object.

        Parameters
        __________
            path : str
                Path to the well logs, e.g. ``path='logs.dlis'``.

        """

    def __init__(self,
                 borehole,
                 path: str,
                 nodata: Union[int, float] = -9999):

        # Importing dlisio
        try:
            from dlisio import dlis
        except ModuleNotFoundError:
            ModuleNotFoundError('dlisio package not installed')

        # Opening DLIS file
        dlis, *tail = dlis.load(path)

        # Getting column names
        columns = [channel.name for channel in dlis.channels]

        # Getting Curves
        curves = [channel.curves() for channel in dlis.channels]

        # Creating DataFrame from curves
        df = pd.DataFrame(curves).T

        # Assigning column names
        df.columns = columns

        # Replace NaN Values
        df = df.replace(nodata, np.NaN)

        # Extracting DataFrame from LAS file
        self.df = df


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
            Points defining the PolyLine.

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


def resample_log(log: Union[gpd.GeoDataFrame, LineString, pd.DataFrame],
                 resampling: int,
                 column_name: str = None,
                 resampling_start=0,
                 resampling_end=None,
                 rounding_precision=5,
                 drop_first: bool = False,
                 drop_last: bool = False,
                 ) -> gpd.GeoDataFrame:
    """Resample one log. Data must be provided as GeoDataFrame with the log Data as Shapely Points.



    """
    # Creating gdf from values
    if isinstance(log, pd.DataFrame):
        log = gpd.GeoDataFrame(geometry=[LineString(log[[column_name, 'DEPTH']].values)])
    # Extracting LineString from Value and assigning column name
    if isinstance(log, gpd.GeoDataFrame):
        if not column_name:
            column_name = 'X'
        log = log.geometry.iloc[0]
    # Assigning column name
    elif isinstance(log, shapely.geometry.LineString):
        if not column_name:
            column_name = 'X'

    # Extracting coordinates
    x = [coords[0] for coords in list(log.coords)]
    y = [coords[1] for coords in list(log.coords)]

    # Getting last position for resampling
    if not resampling_end:
        resampling_end = np.negative(np.floor(y[-1]), where=False)

    # Create LineStrings along Log
    linestrings = [LineString([(min(x),
                                y_sample),
                               (max(x),
                                y_sample)]) for y_sample in np.arange(resampling_start,
                                                                      resampling_end,
                                                                      -resampling)]

    # Create intersection points between LineStrings and log
    points = [
        shapely.wkt.loads(shapely.wkt.dumps(log.intersection(line_intersect), rounding_precision=rounding_precision))
        for line_intersect in linestrings if not log.intersection(line_intersect).is_empty]

    # Creating GeoDataFrame from log
    gdf_resampled = gpd.GeoDataFrame(geometry=points)

    # Setting columns
    gdf_resampled[column_name] = gdf_resampled.geometry.centroid.x
    gdf_resampled['Y'] = np.round(gdf_resampled.geometry.centroid.y, 1)

    # Concatenating GeoDataFrames
    gdf_resampled = pd.concat([pd.DataFrame.from_dict(
        {'geometry': Point(x[0], y[0]), column_name: [x[0]], 'Y': [y[0]]}, orient='columns'),
        gdf_resampled,
        pd.DataFrame.from_dict(
            {'geometry': Point(x[-1], y[-1]), column_name: [x[-1]], 'Y': [y[-1]]},
            orient='columns')
    ], ignore_index=True)

    # Dropping duplicates and resetting index
    gdf_resampled = gdf_resampled.drop_duplicates().reset_index(drop=True)

    # Dropping first depth
    if drop_first:
        gdf_resampled = gdf_resampled[1:].reset_index(drop=True)

    # Dropping last depth
    if drop_last:
        gdf_resampled = gdf_resampled[:-1]

    return gdf_resampled


def resample_logs(logs: pd.DataFrame,
                  resampling: int,
                  resampling_start=0,
                  resampling_end=None,
                  rounding_precision=5,
                  drop_first: bool = True,
                  drop_last: bool = True, ):
    # Resampling DataFrames
    dfs = [resample_log(log=logs[['DEPTH', column]],
                        resampling=resampling,
                        column_name=column,
                        resampling_start=resampling_start,
                        resampling_end=resampling_end,
                        rounding_precision=rounding_precision,
                        drop_first=drop_first,
                        drop_last=drop_last) for column in logs.columns.drop('DEPTH')]

    # Concatenating DataFrames
    df = pd.concat(dfs, axis=1).drop('geometry', axis=1)

    # Dropping duplicate columns
    df = df.loc[:, ~df.columns.duplicated()]

    return df


def merge_logs(paths: List[str],
               resampling: Union[float, int]) -> pd.DataFrame:
    try:
        import lasio
    except ModuleNotFoundError:
        ModuleNotFoundError('lasio package not installed')

    # Opening LAS Files as DataFrames
    dfs = [lasio.read(path).df().reset_index() for path in paths]

    # Resampling logs
    dfs_resampled = [resample_logs(logs=df,
                                   resampling=-resampling,
                                   drop_first=True,
                                   drop_last=True) for df in dfs]

    # Getting minimum und maximum depth
    miny = [df.describe().loc['min']['Y'] for df in dfs_resampled]
    maxy = [df.describe().loc['max']['Y'] for df in dfs_resampled]

    # Creating DataFrame ranging across the entire depth range
    df_depth = pd.DataFrame(np.arange(min(miny), max(maxy) + 1, 1), columns=['Y'])

    # Copying depth DataFrame
    merged_df = df_depth.copy(deep=True)

    # Merging DataFrames
    for i in range(len(dfs_resampled)):
        dfs_resampled[i] = dfs_resampled[i].rename(columns={'X': 'X_%s' % i})
        merged_df = pd.merge(merged_df, dfs_resampled[i], on='Y', how='outer')

    # Renaming column and setting index
    merged_df = merged_df.rename(columns={'Y': 'DEPTH'}).set_index('DEPTH')

    return merged_df