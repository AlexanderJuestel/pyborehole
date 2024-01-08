from typing import Union
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


class Well_Design:

    def __init__(self):
        self.pipes = {}

    def add_pipe(self,
                 name: str,
                 pipe_type: str,
                 top: Union[int, float],
                 bottom: Union[int, float],
                 depth_unit: str,
                 inner_diameter: Union[int, float],
                 outer_diameter: Union[int, float],
                 diameter_unit: str,
                 shoe_height: Union[int, float] = None,
                 shoe_width: Union[int, float] = None,
                 shoe_unit: str = None
                 ):
        """Function to add a pip to the well design.

        Parameters
        __________
            name : str
                Name of the pipe used as key for the pipes dict, e.g. ``name='Conductor Casing'``.
            pipe_type : str
                Type of the pipe, e.g. ``pipe_type='conductor casing'``.
            top : Union[int, float]
                Depth of the top of the pipe, e.g. ``top=0``.
            bottom : Union[int, float]
                Depth of the bottom of the pipe, e.g. ``bottom=-100``.
            depth_unit : str
                Unit of the depth values, options include meters (``'m'``) and feet (``'ft'``), e.g. ``depth_unit='m'``.
            inner_diameter : Union[int, float]
                Inner diameter of the pipe, e.g. ``inner_diameter=20``.
            outer_diameter : Union[int, float]
                Outer diameter of the pipe, e.g. ``outer_diameter=22``.
            diameter_unit : str
                Unit of the diameter values, options include millimeters (``'mm'``) and inches (``'in'``), e.g. ``diameter_unit='in'``.
            shoe_height : Union[int, float]
                Height of the casing shoe, e.g. ``shoe_height=3``.
            shoe_width : Union[int, float]
                Width of the casing shoe, e.g. ``show_width=3``.
            shoe_unit : str
                Unit of the shoe size values, options include millimeters (``'mm'``) and inches (``'in'``), e.g. ``shoe_unit='in'``.

        Returns
        _______
            Well_Design


        Raises
        ______
            TypeError
                If the wrong input data types are provided.
            ValueError
                If the wrong pipe type is provided.
            ValueError
                If the wrong depth or diameter unit is provided.

        Example
        _______
            >>> borehole.well_design.add_pipe(name='Conductor Casing', pipe_type='conductor casing', top=0, bottom=-23, depth_unit='m', inner_diameter=20, outer_diameter=22, diameter_unit='in')

        """
        # Checking that the name is of type string
        if not isinstance(name, str):
            raise TypeError('The pipe name must be provided as string')

        # Checking that the type is of type string
        if not isinstance(pipe_type, str):
            raise TypeError('The pipe type must be provided as string')

        # Checking that the pipe type is one of the following
        if pipe_type not in ['conductor casing', 'surface casing', 'intermediate casing', 'production casing',
                        'production liner']:
            raise ValueError('The provided pipe type is not valid')

        # Checking that the top of the pipe is provided as int or float
        if not isinstance(top, (int, float)):
            raise TypeError('The top of the pipe must be provided as int or float')

        # Checking that the bottom of the pipe is provided as int or float
        if not isinstance(bottom, (int, float)):
            raise TypeError('The bottom of the pipe must be provided as int or float')

        # Checking that the depth unit is provided as string
        if not isinstance(depth_unit, str):
            raise TypeError('The depth_unit must be provided as string')

        # Checking that the depth unit is either meters or feet
        if depth_unit not in ['m', 'ft']:
            raise ValueError('The provided depth unit is not valid')

        # Checking that the inner diameter of the pipe is provided as int or float
        if not isinstance(inner_diameter, (int, float)):
            raise TypeError('The inner diameter of the pipe must be provided as int or float')

        # Checking that the outer diameter of the pipe is provided as int or float
        if not isinstance(outer_diameter, (int, float)):
            raise TypeError('The outer diameter of the pipe must be provided as int or float')

        # Checking that the diameter unit is provided as string
        if not isinstance(diameter_unit, str):
            raise TypeError('The diameter_unit must be provided as string')

        # Checking that the diameter unit is either millimeters or inches
        if diameter_unit not in ['mm', 'in']:
            raise ValueError('The provided diameter unit is not valid')

        # Checking that the shoe height is provided as int or float
        if not isinstance(shoe_height, (int, float, type(None))):
            raise TypeError('The shoe height must be provided as int or float')

        # Checking that the shoe width is provided as int or float
        if not isinstance(shoe_width, (int, float, type(None))):
            raise TypeError('The shoe width must be provided as int or float')

        # Checking that the shoe unit is provided as str
        if not isinstance(shoe_unit, (str, type(None))):
            raise TypeError('The shoe unit must be provided as str')

        # Checking that the shoe unit is either millimeters or inches
        if shoe_unit not in ['mm', 'in']:
            raise ValueError('The provided diameter unit is not valid')

        # Adding the pipe
        pipe = Pipe(pipe_type=pipe_type,
                    top=top,
                    bottom=bottom,
                    depth_unit=depth_unit,
                    inner_diameter=inner_diameter,
                    outer_diameter=outer_diameter,
                    diameter_unit=diameter_unit,
                    shoe_height=shoe_height,
                    shoe_width=shoe_width,
                    shoe_unit=shoe_unit)

        self.pipes[name] = pipe
        self.depth_unit = pipe.depth_unit
        self.diameter_unit = pipe.diameter_unit

    def plot_well_design(self,
                           figsize: tuple = (6, 9),
                           xfactor: Union[int, float] = 4,
                           yfactor: Union[int, float] = 1.05):

        """Plot casing scheme/well_design.

        Parameters
        __________
            figsize : tuple, default: ``(6,9)``
                Matplotlib figure size, e.g. ``figsize=(6,9)``.
            xfactor : Union[int, float], default: ``4``.
                Horizontal stretching factor to rescale the figure, e.g. ``xfactor=4``.
            yfactor : Union[int, float], default: ``1.05``.
                Vertical stretching factor to rescale the figure, e.g. ``yfactor=1.05``.

        Returns
        _______
            fig : matplotlib.figure
                Matplotlib figure.
            ax : matplotlib.axes.Axes
                Matplotlib axis.

        """
        # Checking that the figsize is provided as tuple
        if not isinstance(figsize, tuple):
            raise TypeError('The figsize must be provided as tuple')

        # Checking that the xfactor is of type int or float
        if not isinstance(xfactor, (int, float)):
            raise TypeError('The xfactor must be provided as int or float')

        # Checking that the xfactor is of type int or float
        if not isinstance(xfactor, (int, float)):
            raise TypeError('The xfactor must be provided as int or float')

        # Creating figure and axis
        fig, ax = plt.subplots(1, figsize=figsize)

        # Adding Pipes to plot
        for key, elem in self.pipes.items():
            ax.add_patch(Rectangle(elem.xy, elem.width, elem.height, color="black"))
            ax.add_patch(Rectangle((-1 * elem.xy[0], elem.xy[1]), -1 * elem.width, elem.height, color="black"))

        # Calculating axes limits
        top = np.max([elem.top for key, elem in self.pipes.items()])
        bottom = np.min([elem.bottom for key, elem in self.pipes.items()])
        max_diam = np.max([elem.outer_diameter for key, elem in self.pipes.items()])

        # Setting axes limits
        ax.set_ylim(bottom*yfactor, top)
        ax.set_xlim(-max_diam*xfactor, max_diam*xfactor)

        # Setting axes labels
        ax.set_ylabel('Depth [%s]' % self.depth_unit)
        ax.set_xlabel('Diameter [%s]' % self.diameter_unit)

        # Adding Casing Shoes
        for key, elem in self.pipes.items():
            if elem.shoe_width is not None:
                p0 = [elem.outer_diameter, elem.bottom]
                p1 = [elem.outer_diameter, elem.bottom + elem.shoe_height]
                p2 = [elem.outer_diameter + elem.shoe_width, elem.bottom]
                shoe = plt.Polygon([p0, p1, p2], color="black")
                ax.add_patch(shoe)
                p0[0] *= -1
                p1[0] *= -1
                p2 = [-elem.outer_diameter - elem.shoe_width, elem.bottom]
                shoe = plt.Polygon([p0, p1, p2], color="black")
                ax.add_patch(shoe)

        return fig, ax


class Pipe:
    """Class to initiate a borehole pipe.

    Parameters
    __________
        pipe_type : str
            Type of the pipe, e.g. ``pipe_type='conductor casing'``.
        top : Union[int, float]
            Depth of the top of the pipe, e.g. ``top=0``.
        bottom : Union[int, float]
            Depth of the bottom of the pipe, e.g. ``bottom=-100``.
        depth_unit : str
            Unit of the depth values, options include meters (``'m'``) and feet (``'ft'``), e.g. ``depth_unit='m'``.
        inner_diameter : Union[int, float]
            Inner diameter of the pipe, e.g. ``inner_diameter=20``.
        outer_diameter : Union[int, float]
            Outer diameter of the pipe, e.g. ``outer_diameter=22``.
        diameter_unit : str
            Unit of the diameter values, options include millimeters (``'mm'``) and inches (``'in'``), e.g. ``diameter_unit='in'``.
        shoe_height : Union[int, float]
            Height of the casing shoe, e.g. ``shoe_height=3``.
        shoe_width : Union[int, float]
            Width of the casing shoe, e.g. ``show_width=3``.
        shoe_unit : str
            Unit of the shoe size values, options include millimeters (``'mm'``) and inches (``'in'``), e.g. ``shoe_unit='in'``.

    Returns
    _______
        Pipe


    Raises
    ______
        TypeError
            If the wrong input data types are provided.
        ValueError
            If the wrong pipe type is provided.
        ValueError
            If the wrong depth or diameter unit is provided.

    Example
    _______
        >>> pipe1 = Pipe(pipe_type='conductor casing', top=0, bottom=-23, depth_unit='m', inner_diameter=20, outer_diameter=22, diameter_unit='in')


    .. versionadded:: 0.0.1
    """

    def __init__(self,
                 pipe_type: str,
                 top: Union[int, float],
                 bottom: Union[int, float],
                 depth_unit: str,
                 inner_diameter: Union[int, float],
                 outer_diameter: Union[int, float],
                 diameter_unit: str,
                 shoe_height: Union[int, float] = None,
                 shoe_width: Union[int, float] = None,
                 shoe_unit: str = None):
        """Class to initiate a borehole pipe.

        Parameters
        __________
            pipe_type : str
                Type of the pipe, e.g. ``pipe_type='conductor casing'``.
            top : Union[int, float]
                Depth of the top of the pipe, e.g. ``top=0``.
            bottom : Union[int, float]
                Depth of the bottom of the pipe, e.g. ``bottom=-100``.
            depth_unit : str
                Unit of the depth values, options include meters (``'m'``) and feet (``'ft'``), e.g. ``depth_unit='m'``.
            inner_diameter : Union[int, float]
                Inner diameter of the pipe, e.g. ``inner_diameter=20``.
            outer_diameter : Union[int, float]
                Outer diameter of the pipe, e.g. ``outer_diameter=22``.
            diameter_unit : str
                Unit of the diameter values, options include millimeters (``'mm'``) and inches (``'in'``), e.g. ``diameter_unit='in'``.
            shoe_height : Union[int, float]
                Height of the casing shoe, e.g. ``shoe_height=3``.
            shoe_width : Union[int, float]
                Width of the casing shoe, e.g. ``show_width=3``.
            shoe_unit : str
                Unit of the shoe size values, options include millimeters (``'mm'``) and inches (``'in'``), e.g. ``shoe_unit='in'``.

        Returns
        _______
            Pipe


        Raises
        ______
            TypeError
                If the wrong input data types are provided.
            ValueError
                If the wrong pipe type is provided.
            ValueError
                If the wrong depth or diameter unit is provided.

        Example
        _______
            >>> pipe1 = Pipe(pipe_type='conductor casing', top=0, bottom=-23, depth_unit='m', inner_diameter=20, outer_diameter=22, diameter_unit='in')


        .. versionadded:: 0.0.1
        """

        # Checking that the type is of type string
        if not isinstance(pipe_type, str):
            raise TypeError('The pipe type must be provided as string')

        # Checking that the pipe type is one of the following
        if pipe_type not in ['conductor casing', 'surface casing', 'intermediate casing', 'production casing',
                        'production liner']:
            raise ValueError('The provided pipe type is not valid')

        # Checking that the top of the pipe is provided as int or float
        if not isinstance(top, (int, float)):
            raise TypeError('The top of the pipe must be provided as int or float')

        # Checking that the bottom of the pipe is provided as int or float
        if not isinstance(bottom, (int, float)):
            raise TypeError('The bottom of the pipe must be provided as int or float')

        # Checking that the depth unit is provided as string
        if not isinstance(depth_unit, str):
            raise TypeError('The depth_unit must be provided as string')

        # Checking that the depth unit is either meters or feet
        if depth_unit not in ['m', 'ft']:
            raise ValueError('The provided depth unit is not valid')

        # Checking that the inner diameter of the pipe is provided as int or float
        if not isinstance(inner_diameter, (int, float)):
            raise TypeError('The inner diameter of the pipe must be provided as int or float')

        # Checking that the outer diameter of the pipe is provided as int or float
        if not isinstance(outer_diameter, (int, float)):
            raise TypeError('The outer diameter of the pipe must be provided as int or float')

        # Checking that the diameter unit is provided as string
        if not isinstance(diameter_unit, str):
            raise TypeError('The diameter_unit must be provided as string')

        # Checking that the diameter unit is either millimeters or inches
        if diameter_unit not in ['mm', 'in']:
            raise ValueError('The provided diameter unit is not valid')

        # Checking that the shoe height is provided as int or float
        if not isinstance(shoe_height, (int, float, type(None))):
            raise TypeError('The shoe height must be provided as int or float')

        # Checking that the shoe width is provided as int or float
        if not isinstance(shoe_width, (int, float, type(None))):
            raise TypeError('The shoe width must be provided as int or float')

        # Checking that the shoe unit is provided as str
        if not isinstance(shoe_unit, (str, type(None))):
            raise TypeError('The shoe unit must be provided as str')

        # Checking that the shoe unit is either millimeters or inches
        if shoe_unit not in ['mm', 'in']:
            raise ValueError('The provided diameter unit is not valid')

        # Setting attributes
        self.pipe_type = pipe_type

        self.top = top
        self.bottom = bottom
        self.length = self.top - self.bottom

        self.depth_unit = depth_unit

        if self.depth_unit == 'm':
            self.top_m = self.top
            self.bottom_m = self.bottom
            self.top_ft = m_to_ft(value=self.top)
            self.bottom_ft = m_to_ft(value=self.bottom)
        elif self.depth_unit == 'ft':
            self.top_m = ft_to_m(value=self.top)
            self.bottom_m = ft_to_m(value=self.bottom)
            self.top_ft = self.top
            self.bottom_ft = self.bottom

        self.inner_diameter = inner_diameter
        self.outer_diameter = outer_diameter
        self.thickness = self.outer_diameter - self.inner_diameter

        self.diameter_unit = diameter_unit

        if self.diameter_unit == 'mm':
            self.inner_diameter_mm = self.inner_diameter
            self.outer_diameter_mm = self.outer_diameter
            self.inner_diameter_in = mm_to_in(value=self.inner_diameter)
            self.outer_diameter_in = mm_to_in(value=self.outer_diameter)
        elif self.diameter_unit == 'in':
            self.inner_diameter_mm = in_to_mm(self.inner_diameter)
            self.outer_diameter_mm = in_to_mm(self.outer_diameter)
            self.inner_diameter_in = self.inner_diameter
            self.outer_diameter_in = self.outer_diameter

        self.shoe_height = shoe_height
        self.shoe_width = shoe_width
        self.shoe_unit = shoe_unit

        if self.shoe_unit == 'mm':
            self.shoe_height_mm = self.shoe_height
            self.shoe_width_mm = self.shoe_width
            self.shoe_height_in = mm_to_in(value=self.shoe_height)
            self.shoe_width_in = mm_to_in(value=self.shoe_width)
        elif self.shoe_unit == 'in':
            self.shoe_height_mm = in_to_mm(self.shoe_height)
            self.shoe_width_mm = in_to_mm(self.shoe_width)
            self.shoe_height_in = self.shoe_height
            self.shoe_width_in = self.shoe_width

        # Setting attributes for Rectangle plotting
        self.xy = np.array([self.inner_diameter, self.bottom])
        self.width = self.thickness
        self.height = self.length

    def __repr__(self):
        """Return contents of the pipe

        Returns
        _______
            borehole.name : str
                Name of the borehole.

        .. versionadded:: 0.0.1
        """
        return f"Type: {self.pipe_type} \n" \
               f"Top: {self.top} {self.depth_unit} \n" \
               f"Bottom: {self.bottom} {self.depth_unit} \n" \
               f"Inner Diameter: {self.inner_diameter} {self.diameter_unit} \n" \
               f"Outer Diameter: {self.outer_diameter} {self.diameter_unit} \n" \



def m_to_ft(value: Union[int, float]) -> float:
    """Auxiliary function to convert meters to feet.

    Parameters
    __________
        value : Union[int, float]
            Value in meters.

    Returns
    _______
        feet : float
            Value in feet.

    Raises
    ______
        TypeError
            If the wrong input data types are provided.

    Example
    _______
        >>> feet = well_design.m_to_ft(value=10)
        >>> feet
        32.8084

    .. versionadded:: 0.0.1
    """
    # Checking that the provided value is of type int or float
    if not isinstance(value, (int, float)):
        raise TypeError('The provided value must be of type int or float')

    # Calculating feet from meters
    feet = value / 0.3048

    return feet


def ft_to_m(value: Union[int, float]) -> float:
    """Auxiliary function to convert feet to meters.

    Parameters
    __________
        value : Union[int, float]
            Value in feet.

    Returns
    _______
        feet : float
            Value in meters.

    Raises
    ______
        TypeError
            If the wrong input data types are provided.

    Example
    _______
        >>> meters = well_design.ft_to_m(value=10)
        >>> meters
        3.048

    .. versionadded:: 0.0.1
    """
    # Checking that the provided value is of type int or float
    if not isinstance(value, (int, float)):
        raise TypeError('The provided value must be of type int or float')

    # Calculating meters from feet
    meters = value * 0.3048

    return meters


def mm_to_in(value: Union[int, float]) -> float:
    """Auxiliary function to convert millimeters to inches.

    Parameters
    __________
        value : Union[int, float]
            Value in millimeters.

    Returns
    _______
        feet : float
            Value in inches.

    Raises
    ______
        TypeError
            If the wrong input data types are provided.

    Example
    _______
        >>> inches = well_design.mm_to_in(value=10)
        >>> inches
        0.3937

    .. versionadded:: 0.0.1
    """
    # Checking that the provided value is of type int or float
    if not isinstance(value, (int, float)):
        raise TypeError('The provided value must be of type int or float')

    # Calculating inches from meters
    inches = value / 25.4

    return inches


def in_to_mm(value: Union[int, float]) -> float:
    """Auxiliary function to convert inches to millimiters.

    Parameters
    __________
        value : Union[int, float]
            Value in inches.

    Returns
    _______
        feet : float
            Value in millimeters.

    Raises
    ______
        TypeError
            If the wrong input data types are provided.

    Example
    _______
        >>> inches = well_design.in_to_mm(value=10)
        >>> inches
        254

    .. versionadded:: 0.0.1
    """
    # Checking that the provided value is of type int or float
    if not isinstance(value, (int, float)):
        raise TypeError('The provided value must be of type int or float')

    # Calculating millimeters from inches
    millimeters = value * 25.4

    return millimeters
