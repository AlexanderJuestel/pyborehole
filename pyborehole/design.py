from typing import Union
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import copy


class WellDesign:
    """Class to initiate a well design object

    Parameters
    __________
        borehole : Borehole
            Borehole object.

    Returns
    _______
        WellDesign
            Well design object.

    Examples
    ________
        >>> borehole.add_well_design()
        >>>

    .. versionadded:: 0.0.1
    """

    def __init__(self,
                 borehole):
        self.pipes = {}
        self.cements = {}
        self.depth_unit = None
        self.diameter_unit = None

    def __repr__(self):
        """Return contents of the well design.

        Returns
        _______
             WellDesign
                Contents of the well design.

        .. versionadded:: 0.0.1
        """
        return f"Pipes: {self.pipes} \n" \
               f"Cements: {self.cements}"

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
        """Function to add a pipe to the well design.

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
                Well Design object.

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
            >>> borehole.well_design.add_pipe(name='Conductor Casing', pipe_type='conductor casing', top=0, bottom=-35, depth_unit='m', inner_diameter=20, outer_diameter=21, diameter_unit='in')
            >>> borehole.well_design.pipes['Conductor Casing']
            Type: conductor casing
            Top: 0 m
            Bottom: -35 m
            Inner Diameter: 20 in
            Outer Diameter: 21 in

        .. versionadded:: 0.0.1
        """
        # Checking that the name is of type string
        if not isinstance(name, str):
            raise TypeError('The pipe name must be provided as string')

        # Checking that the type is of type string
        if not isinstance(pipe_type, str):
            raise TypeError('The pipe type must be provided as string')

        # Checking that the pipe type is one of the following
        if pipe_type not in ['conductor casing', 'surface casing', 'intermediate casing', 'production casing',
                             'production liner', 'open hole section']:
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
        if shoe_unit not in ['mm', 'in', None]:
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

    def add_cement(self,
                   name: str,
                   top: Union[int, float],
                   bottom: Union[int, float],
                   pipe_inner: str,
                   pipe_outer: str,
                   depth_unit: str):
        """Function to add cement to the well design.

        Parameters
        __________
            name : str
                Name of the cement used as key for the cement dict, e.g. ``name='Cement 1'``.
            top : Union[int, float]
                Depth of the top of the cement, e.g. ``top=0``.
            bottom : Union[int, float]
                Depth of the bottom of the cement, e.g. ``bottom=-100``.
            pipe_inner : str
                Name of the inner pipe, e.g. ``pipe_inner='Production Liner'``.
            pipe_outer : str
                Name of the outer pipe, e.g. ``pipe_outer='Production Casing'``.
            depth_unit : str
                Unit of the depth values, options include meters (``'m'``) and feet (``'ft'``), e.g. ``depth_unit='m'``.

        Raises
        ______
            TypeError
                If the wrong input data types are provided.
            ValueError
                If an invalid name for the inner or outer pipe is provided.

        Examples
        ________
            >>> borehole.add_well_design()
            >>> borehole.well_design
            Pipes: {}
            Cements: {}

        .. versionadded:: 0.0.1
        """
        # Checking that the name is of type string
        if not isinstance(name, str):
            raise TypeError('The cement name must be provided as string')

        # Checking that the top of the pipe is provided as int or float
        if not isinstance(top, (int, float)):
            raise TypeError('The top of the pipe must be provided as int or float')

        # Checking that the bottom of the pipe is provided as int or float
        if not isinstance(bottom, (int, float)):
            raise TypeError('The bottom of the pipe must be provided as int or float')

        # Checking that the name of the inner pipe is of type string
        if not isinstance(pipe_inner, str):
            raise TypeError('The name of the inner pipe must be provided as string')

        # Checking that the key of the inner pipe is valid
        if pipe_inner not in list(self.pipes.keys()):
            raise ValueError('Name of the inner pipe invalid ')

        # Checking that the key of the outer pip is valid
        if pipe_outer not in list(self.pipes.keys()):
            raise ValueError('Name of the outer pipe invalid ')

        # Checking that the name of the outer pipe is of type string
        if not isinstance(pipe_outer, str):
            raise TypeError('The name of the outer pipe must be provided as string')

        # Checking that the depth unit is provided as string
        if not isinstance(depth_unit, str):
            raise TypeError('The depth_unit must be provided as string')

        # Checking that the depth unit is either meters or feet
        if depth_unit not in ['m', 'ft']:
            raise ValueError('The provided depth unit is not valid')

        # Creating Cement
        cement = Cement(name=name,
                        top=top,
                        bottom=bottom,
                        pipe_inner=pipe_inner,
                        pipe_outer=pipe_outer,
                        depth_unit=depth_unit,
                        pipes=self.pipes)

        self.cements[name] = cement

    def plot_well_design(self,
                         figsize: tuple = (6, 9),
                         xfactor: Union[int, float] = 4,
                         yfactor: Union[int, float] = 1.1,
                         show_pipes: bool = True,
                         show_shoes: bool = True,
                         show_cements: bool = True,
                         show_descriptions: bool = True,
                         xshift_pipes_description: Union[int, float] = 10,
                         xshift_cements_description: Union[int, float] = 60,
                         yshift_description: Union[int, float] = 25):
        """Plot casing scheme/well_design.

        Parameters
        __________
            figsize : tuple, default: ``(6,9)``
                Matplotlib figure size, e.g. ``figsize=(6,9)``.
            xfactor : Union[int, float], default: ``4``.
                Horizontal stretching factor to rescale the figure, e.g. ``xfactor=4``.
            yfactor : Union[int, float], default: ``1.05``.
                Vertical stretching factor to rescale the figure, e.g. ``yfactor=1.05``.
            show_pipes : bool, default: ``True``
                Boolean value to show the pipes, e.g. ``show_pipes=True``.
            show_shoes : bool, default: ``True``
                Boolean value to show the casig shoes, e.g. ``show_shoes=True``.
            show_cements : bool, default: ``True``
                Boolean value to show the cements, e.g. ``show_cements=True``.
            show_descriptions : bool, default: ``True``
                Boolean value to show the descriptions, e.g. ``show_descriptions=True``.
            xshift_pipes_description : Union[int, float], default: ``10``
                Value to shift the descriptions in x-direction, e.g. `xshift_pipes_description=10``.
            xshift_cements_description : Union[int, float], default: ``60``
                Value to shift the descriptions in x-direction, e.g. `xshift_cements_description=60``.
            yshift_description : Union[int, float], default: ``25``
                Value to shift the descriptions in y-direction, e.g. `yshift_description=10``.

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
            >>> borehole.well_design.plot_well_design()

        .. versionadded:: 0.0.1
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

        # Checking that show_pipes is provided as bool
        if not isinstance(show_pipes, bool):
            raise TypeError('Show_pipes must be either True or False')

        # Checking that show_shoes is provided as bool
        if not isinstance(show_shoes, bool):
            raise TypeError('Show_shoes must be either True or False')

        # Checking that show_cements is provided as bool
        if not isinstance(show_cements, bool):
            raise TypeError('Show_cements must be either True or False')

        # Checking that show_descriptions is provided as bool
        if not isinstance(show_descriptions, bool):
            raise TypeError('Show_descriptions must be either True or False')

        # Checking that the x shift for the pipes if of type int or float
        if not isinstance(xshift_pipes_description, (int, float)):
            raise TypeError('The x shift for the pipes must be provided as int or float')

        # Checking that the x shift for the cements if of type int or float
        if not isinstance(xshift_cements_description, (int, float)):
            raise TypeError('The x shift for the cements must be provided as int or float')

        # Checking that the y shift for the descriptions if of type int or float
        if not isinstance(yshift_description, (int, float)):
            raise TypeError('The y shift for the descriptions must be provided as int or float')

        # Creating figure and axis
        fig, ax = plt.subplots(1, figsize=figsize)

        # Adding Pipes to plot
        if show_pipes:
            for key, elem in self.pipes.items():
                if elem.pipe_type == 'open hole section':
                    # Plotting open hole section as wavy line
                    y = np.linspace(elem.top, elem.bottom, 1000)
                    x1 = 0.5 * np.sin(y / 2) - elem.inner_diameter + 0.5
                    x2 = 0.5 * np.cos(y / 2 + np.pi/4) + elem.inner_diameter
                    ax.plot(x1, y, color='black')
                    ax.plot(x2, y, color='black')
                    # Plotting open hole section as dashed line
                    #ax.plot([elem.inner_diameter,elem.inner_diameter],
                    #        [elem.top, elem.bottom],
                    #        linestyle='--',
                    #        color='black')
                    #ax.plot([-elem.inner_diameter, -elem.inner_diameter],
                    #        [elem.top, elem.bottom],
                    #        linestyle='--',
                    #        color='black')
                else:
                    ax.add_patch(Rectangle(elem.xy, elem.width, elem.height, color="black"))
                    ax.add_patch(Rectangle((-1 * elem.xy[0], elem.xy[1]), -1 * elem.width, elem.height, color="black"))

                # Showing Descriptions
                if show_descriptions:
                    max_diam = np.max([elem.outer_diameter for key, elem in self.pipes.items()])
                    for key, elem in self.pipes.items():
                        if elem.pipe_type == 'open hole section':
                            ax.text(max_diam + xshift_pipes_description,
                                    elem.bottom + yshift_description,
                                    elem,
                                    fontsize=8)
                        else:
                            ax.text(max_diam + xshift_pipes_description,
                                    elem.bottom + yshift_description,
                                    elem,
                                    fontsize=8)

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
                ax.add_patch(
                    Rectangle((elem.inner_diameter, elem.top), thicknesses[i] + elem.thickness, 1, color="black"))
                ax.add_patch(Rectangle((-1 * elem.inner_diameter, elem.top), -1 * thicknesses[0] - elem.thickness, 1,
                                       color="black"))
                i = i + 1

        # Adding Casing Shoes
        if show_shoes:
            for key, elem in self.pipes.items():
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
                    ax.add_patch(shoe)

        # Adding Casing Cements
        if show_cements:
            for key, elem in self.cements.items():
                ax.fill_between(elem.xvals, elem.tops, elem.bottoms, color="#6b705c", alpha=0.5)
                ax.fill_between(-1 * elem.xvals, elem.tops, elem.bottoms, color="#6b705c", alpha=0.5)

            # Showing Descriptions
            if show_descriptions:
                max_diam = np.max([elem.outer_diameter for key, elem in self.pipes.items()])
                for key, elem in self.cements.items():
                    ax.text(-max_diam - xshift_cements_description, elem.bottom + yshift_description, elem, fontsize=8)

        # Calculating axes limits
        top = np.min([elem.top for key, elem in self.pipes.items()])
        bottom = np.max([elem.bottom for key, elem in self.pipes.items()])
        max_diam = np.max([elem.outer_diameter for key, elem in self.pipes.items()])

        # Setting axes limits
        ax.set_ylim(bottom * yfactor, top)
        ax.set_xlim(-max_diam * xfactor, max_diam * xfactor)
        #ax.invert_yaxis()

        # Setting axes labels
        ax.set_ylabel('Depth [%s]' % self.depth_unit)
        ax.set_xlabel('Diameter [%s]' % self.diameter_unit)

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
            Pipe object.

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
        >>> pipe1
        Type: conductor casing
        Top: 0 m
        Bottom: -35 m
        Inner Diameter: 20 in
        Outer Diameter: 21 in

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
                Pipe object.

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
            >>> pipe1 = Pipe(pipe_type='conductor casing', top=0, bottom=-35, depth_unit='m', inner_diameter=20, outer_diameter=21, diameter_unit='in')
            >>> pipe1
            Type: conductor casing
            Top: 0 m
            Bottom: -35 m
            Inner Diameter: 20 in
            Outer Diameter: 21 in

        .. versionadded:: 0.0.1
        """

        # Checking that the type is of type string
        if not isinstance(pipe_type, str):
            raise TypeError('The pipe type must be provided as string')

        # Checking that the pipe type is one of the following
        if pipe_type not in ['conductor casing', 'surface casing', 'intermediate casing', 'production casing',
                             'production liner', 'open hole section']:
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
        if shoe_unit not in ['mm', 'in', None]:
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
             Contents of the pipe.

        .. versionadded:: 0.0.1
        """
        return f"Type: {self.pipe_type} \n" \
               f"Top: {self.top} {self.depth_unit} \n" \
               f"Bottom: {self.bottom} {self.depth_unit} \n" \
               f"Inner Diameter: {self.inner_diameter} {self.diameter_unit} \n" \
               f"Outer Diameter: {self.outer_diameter} {self.diameter_unit}"


class Cement:
    """Class to initiate cement.

    Parameters
    __________
        name : str
            Name of the cement used as key for the cement dict, e.g. ``name='Cement 1'``.
        top : Union[int, float]
            Depth of the top of the cement, e.g. ``top=0``.
        bottom : Union[int, float]
            Depth of the bottom of the cement, e.g. ``bottom=-100``.
        pipe_inner : str
            Name of the inner pipe, e.g. ``pipe_inner='Production Liner'``.
        pipe_outer : str
            Name of the outer pipe, e.g. ``pipe_outer='Production Casing'``.
        depth_unit : str
            Unit of the depth values, options include meters (``'m'``) and feet (``'ft'``), e.g. ``depth_unit='m'``.
        pipes : dict
            Dictionary containting the pipes.

    Returns
    _______
        Cement

    Raises
    ______
        TypeError
            If the wrong input data types are provided.
        ValueError
            If an invalid name for the inner or outer pipe is provided.

    Examples
    ________
        >>> cement1 = Cement(top=-200, bottom=-500, depth_unit='m', pipe_inner='Production Liner', pipe_outer='Production Casing')
        >>> cement1
        'Cement 1': Top: -200 m
        Bottom: -500 m
        Cement Thickness: 3 in
        Inner Pipe: Production Liner
        Outer Pipe: Production Liner

    .. versionadded:: 0.0.1
    """

    def __init__(self,
                 name: str,
                 top: Union[int, float],
                 bottom: Union[int, float],
                 depth_unit: str,
                 pipe_inner: str,
                 pipe_outer: str,
                 pipes: dict):
        """Class to initiate cement.

        Parameters
        __________
            name : str
                Name of the cement used as key for the cement dict, e.g. ``name='Cement 1'``.
            top : Union[int, float]
                Depth of the top of the cement, e.g. ``top=0``.
            depth_unit : str
                Unit of the depth values, options include meters (``'m'``) and feet (``'ft'``), e.g. ``depth_unit='m'``.
            bottom : Union[int, float]
                Depth of the bottom of the cement, e.g. ``bottom=-100``.
            pipe_inner : str
                Name of the inner pipe, e.g. ``pipe_inner='Production Liner'``.
            pipe_outer : str
                Name of the outer pipe, e.g. ``pipe_outer='Production Casing'``.
            pipes : dict
                Dictionary containting the pipes.

        Returns
        _______
            Cement

        Raises
        ______
            TypeError
                If the wrong input data types are provided.
            ValueError
                If an invalid name for the inner or outer pipe is provided.

        Examples
        ________
            >>> cement1 = Cement(top=-200, bottom=-500, depth_unit='m', pipe_inner='Production Liner', pipe_outer='Production Casing')
            >>> cement1
            'Cement 1': Top: -200 m
            Bottom: -500 m
            Cement Thickness: 3 in
            Inner Pipe: Production Liner
            Outer Pipe: Production Liner

        .. versionadded:: 0.0.1
        """
        # Checking that the name of the pipe is provided as str
        if not isinstance(name, str):
            raise TypeError('The name of the pipe must be provided as str')

        # Checking that the top of the pipe is provided as int or float
        if not isinstance(top, (int, float)):
            raise TypeError('The top of the pipe must be provided as int or float')

        # Checking that the bottom of the pipe is provided as int or float
        if not isinstance(bottom, (int, float)):
            raise TypeError('The bottom of the pipe must be provided as int or float')

        # Checking that the name of the inner pipe is of type string
        if not isinstance(pipe_inner, str):
            raise TypeError('The name of the inner pipe must be provided as string')

        # Checking that the pipes are provided as dict
        if not isinstance(pipes, dict):
            raise TypeError('The pipes must be provided as dict')

        # Checking that the key of the inner pipe is valid
        if pipe_inner not in list(pipes.keys()):
            raise ValueError('Name of the inner pipe invalid ')

        # Checking that the key of the outer pipe is valid
        if pipe_outer not in list(pipes.keys()):
            raise ValueError('Name of the outer pipe invalid ')

        # Checking that the name of the outer pipe is of type string
        if not isinstance(pipe_outer, str):
            raise TypeError('The name of the outer pipe must be provided as string')

        # Checking that the depth unit is provided as string
        if not isinstance(depth_unit, str):
            raise TypeError('The depth_unit must be provided as string')

        # Checking that the depth unit is either meters or feet
        if depth_unit not in ['m', 'ft']:
            raise ValueError('The provided depth unit is not valid')

        # Setting attributes
        self.name = name
        self.top = top
        self.bottom = bottom
        self.pipe_inner = pipe_inner
        self.pipe_outer = pipe_outer

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

        self.inner = pipes[pipe_inner].outer_diameter
        self.outer = pipes[pipe_outer].inner_diameter

        if pipes[pipe_inner].pipe_type == 'conductor casing':
            self.thickness = pipes[pipe_inner].shoe_width
            self.xvals = np.array([self.inner, self.inner+self.thickness])
        else:
            self.thickness = pipes[pipe_outer].inner_diameter - pipes[pipe_inner].outer_diameter
            self.xvals = np.array([self.inner, self.outer])

        self.diameter_unit = pipes[pipe_inner].diameter_unit

        self.tops = [self.top, self.top]
        self.bottoms = [self.bottom, self.bottom]

    def __repr__(self):
        """Return contents of the cement

        Returns
        _______
            Contents of the cement.

        .. versionadded:: 0.0.1
        """
        return f"Top: {self.top} {self.depth_unit} \n" \
               f"Bottom: {self.bottom} {self.depth_unit} \n" \
               f"Cement Thickness: {self.thickness} {self.diameter_unit}  \n" \
               f"Inner Pipe: {self.pipe_inner} \n" \
               f"Outer Pipe: {self.pipe_inner}"


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
