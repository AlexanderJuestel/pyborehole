import pandas as pd
from shapely.geometry import Point
from pyproj import CRS
import pyproj
from typing import Union, Tuple
import geopandas as gpd

from pyborehole.deviation import Deviation
from pyborehole.design import WellDesign
from pyborehole.logs import LASLogs, DLISLogs
from pyborehole.litholog import LithoLog


class Borehole:
    """Class to initiate a borehole object.

    Parameters
    __________
        name : str
            Name of the Borehole, e.g. ``name='Weisweiler R1'``.

    Returns
    _______
        Borehole
            Borehole Object.

    Raises
    ______
        TypeError
            If the wrong input data types are provided.

    Examples
    ________
        >>> from pyborehole.borehole import Borehole
        >>> borehole = Borehole(name='Weisweiler R1')
        >>> borehole.name
        Weisweiler R1

    See Also
    ________
        add_deviation : Add deviation to the Borehole Object.
        add_litholog : Add LithoLog to the Borehole Object.
        add_well_logs : Add Well Logs to the Borehole Object.
        add_well_tops : Add Well Tops to the Borehole Object.
        create_df : Create DataFrame from Borehole Object Attributes.
        create_properties_df : Create Properties DataFrame from Borehole Object Attributes.
        init_properties : Initiate Borehole properties.
        to_gdf : Create GeoDataFrame from Well Object DataFrame.
        update_df : Update Well Object DataFrame with data from data_dict.
        update_value : Update attribute and value of Well Object DataFrame.


    .. versionadded:: 0.0.1
    """

    boreholes = []

    def __init__(self,
                 name: str):
        """Class to initiate a borehole object.

        Parameters
        __________
            name : str
                Name of the Borehole, e.g. ``name='Weisweiler R1'``.

        Returns
        _______
            Borehole
                Borehole Object.

        Raises
        ______
            TypeError
                If the wrong input data types are provided.

        Examples
        ________
            >>> from pyborehole.borehole import Borehole
            >>> borehole = Borehole(name='Weisweiler R1')
            >>> borehole.name
            Weisweiler R1

        See Also
        ________
            add_deviation : Add deviation to the Borehole Object.
            add_litholog : Add LithoLog to the Borehole Object.
            add_well_logs : Add Well Logs to the Borehole Object.
            add_well_tops : Add Well Tops to the Borehole Object.
            create_df : Create DataFrame from Borehole Object Attributes.
            create_properties_df : Create Properties DataFrame from Borehole Object Attributes.
            init_properties : Initiate Borehole properties.
            to_gdf : Create GeoDataFrame from Well Object DataFrame.
            update_df : Update Well Object DataFrame with data from data_dict.
            update_value : Update attribute and value of Well Object DataFrame.


        .. versionadded:: 0.0.1
        """

        # Append Boreholes
        self.__class__.boreholes.append(self)

        # Checking that the name is provided as string
        if not isinstance(name, str):
            raise TypeError('The name of the borehole must be provided as string')

        # Defining attributes
        self.name = name
        self.has_name = True

        # Defining emtpy attributes
        self.address = None
        self.has_address = None

        self.location = None
        self.has_location = None

        self.x = None
        self.y = None
        self.has_x = None
        self.has_y = None

        self.crs = None
        self.crs_pyproj = None
        self.has_crs = None
        self.has_crs_pyproj = None

        self.altitude_above_sea_level = None
        self.altitude_above_kb = None
        self.has_altitude_above_sea_level = None
        self.has_altitude_above_kb = None

        self.id = None
        self.has_id = None

        self.borehole_type = None
        self.has_borehole_type = None

        self.md = None
        self.tvd = None
        self.tvdss = None
        self.has_md = None
        self.has_tvd = None
        self.has_tvdss = None

        self.depth_unit = None
        self.has_depth_unit = None

        self.is_vertical = None

        self.contractree = None
        self.drilling_contractor = None
        self.logging_contractor = None
        self.field = None
        self.project = None
        self.has_contractree = None
        self.has_drilling_contractor = None
        self.has_logging_contractor = None
        self.has_field = None
        self.has_project = None

        self.start_drilling = None
        self.end_drilling = None
        self.start_logging = None
        self.end_logging = None
        self.has_start_drilling = None
        self.has_end_drilling = None
        self.has_start_logging = None
        self.has_end_logging = None

        # Adding Deviation, well logs and well tops
        self.deviation = None
        self.logs = None
        self.well_tops = None
        self.litholog = None
        self.well_design = None

        self.has_deviation = False
        self.has_logs = False
        self.has_well_tops = False
        self.has_litholog = False
        self.has_well_design = False

        # Creating borehole (Geo-)DataFrame
        self.df = None
        self.gdf = None
        self.properties = None

    def __str__(self):
        """Return name of borehole.

        Returns
        _______
            borehole.name : str
                Name of the borehole.

        Examples
        ________
            >>> from pyborehole.borehole import Borehole
            >>> borehole = Borehole(name='Weisweiler R1')
            >>> borehole
            Borehole: Weisweiler R1

        .. versionadded:: 0.0.1
        """
        return f"Borehole: {self.name}"

    def __repr__(self):
        """Return name of borehole.

        Returns
        _______
            borehole.name : str
                Name of the borehole.

        Examples
        ________
            >>> from pyborehole.borehole import Borehole
            >>> borehole = Borehole(name='Weisweiler R1')
            >>> borehole
            Borehole: Weisweiler R1

        .. versionadded:: 0.0.1
        """
        return f"Borehole: {self.name}"

    def init_properties(self,
                        address: str = None,
                        location: Tuple[float, float] = None,
                        crs: Union[str, pyproj.crs.crs.CRS] = None,
                        altitude_above_sea_level: Union[int, float] = None,
                        altitude_above_kb: Union[int, float] = None,
                        id: Union[str, int, float] = None,
                        borehole_type: str = None,
                        md: Union[int, float] = None,
                        tvd: Union[int, float] = None,
                        depth_unit: str = None,
                        vertical: bool = True,
                        contractee: str = None,
                        drilling_contractor: str = None,
                        logging_contractor: str = None,
                        field: str = None,
                        project: str = None,
                        start_drilling: str = None,
                        end_drilling: str = None,
                        start_logging: str = None,
                        end_logging: str = None):
        """Initiate Borehole properties.

        Parameters
        __________
            address : str
                Address of the Borehole, e.g. ``address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland'``.
            location : tuple
                Coordinates tuple representing the location of the Borehole, e.g. ``location=(6.313031, 50.835676)``.
            crs : Union[str, pyproj.crs.crs.CRS]
                Coordinate Reference System of the coordinates, e.g. ``crs='EPSG:4326'``.
            altitude_above_sea_level : Union[int, float]
                Altitude above sea level, e.g. ``altitude_above_sea_level=136``.
            altitude_above_kb : Union[int, float]
                Altitude above KB, e.g. ``altitude_above_kb=140``.
            id : Union[str, int, float]
                Unique identifier for this borehole, e.g. ``id='DABO123456'``.
            borehole_type : str
                Borehole type, e.g. ``borehole_type='exploration'``.
            md : Union[int, float]
                Measured depth of the borehole, e.g. ``md=100``.
            tvd : Union[int, float]
                True vertical depth of the borehole, e.g. ``tvd=95``.
            depth_unit : str
                Unit for the depth values, e.g. ``depth_values='m'``.
            vertical : bool, default is ``True``
                Variable to state if the borehole is vertical (True) or deviated (False), e.g. ``vertical=True``.
            contractee : str
                Contractee of the drilling operation, e.g. ``contractee='Fraunhofer IEG'``.
            drilling_contractor : str
                Drilling contractor who performed the drilling, e.g. ``drilling_contractor='RWE BOWA'``.
            logging_contractor : str
                Logging contractor who performed the logging, e.g. ``logging_contractor='DMT GmbH'``.
            field : str
                Name of the field the well was drilled in, e.g. ``field='Erdwärme Aachen'``.
            project : str
                Name of the project the borehole was drilled for, e.g. ``project='DGE Rollout'``.
            start_drilling : str
                Start date of the drilling operation, e.g. ``start_drilling='2023-10-18'``.
            end_drilling : str
                End date of the drilling operation, e.g. ``end_drilling='2023-10-28'``.
            start_logging : str
                Start date of the logging operation, e.g. ``start_logging='2023-10-18'``.
            end_logging : str
                End date of the logging operation, e.g. ``end_logging='2023-10-28'``.

        Raises
        ______
            TypeError
                If the wrong input data types are provided.

        Examples
        ________
            >>> from pyborehole.borehole import Borehole
            >>> borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland', location=(6.313031, 50.835676), crs='EPSG:4326', altitude_above_sea_level=136)
            >>> borehole.df
                                                    Value
                Name                                RWE EB1
                Address                             Am Kraftwerk 17, 52249 Eschweiler, Germany
                Location                            POINT (6.313031 50.835676)
                X                                   6.313031
                Y                                   50.835676
                Coordinate Reference System         EPSG:4326
                Coordinate Reference System PyProj  EPSG:4326
                Altitude above sea level            136
                Altitude above KB                   None

        .. versionadded:: 0.0.1
        """

        # Checking that the address is provided as string
        if not isinstance(address, (str, type(None))):
            raise TypeError('The address of the borehole must be provided as string')

        # Checking that the location is provided as tuple
        if not isinstance(location, (tuple, type(None))):
            raise TypeError('The location of the borehole must be provided as tuple')

        # Checking that the crs is provided as string or pyproj CRS
        if not isinstance(crs, (str, pyproj.crs.crs.CRS, type(None))):
            raise TypeError('The CRS of the borehole location must be provided as string or pyproject CRS')

        # Checking that the altitude is provided as int or float
        if not isinstance(altitude_above_sea_level, (int, float, type(None))):
            raise TypeError('The altitude of the borehole must be provided as int or float')

        # Checking that the altitude is provided as int or float
        if not isinstance(altitude_above_kb, (int, float, type(None))):
            raise TypeError('The altitude of the borehole above KB must be provided as int or float')

        # Checking that the id is provided as int, float or string
        if not isinstance(id, (str, int, float, type(None))):
            raise TypeError('The ID of the borehole must be provided as str, int, or float')

        # Checking that the borehole_type is of type string
        if not isinstance(borehole_type, (str, type(None))):
            raise TypeError('The borehole_type must be provided as string')

        # Checking that the borehole_type is one of the possible types
        if borehole_type:
            if borehole_type not in ['exploration', 'producer', 'injector', 'sidetrack', 'observatory',
                                     'heat exchanger']:
                raise ValueError(
                    'The borehole_type must be one of the following: exploration, producer, injector, sidetrack, observatory, heat exchanger')

        # Checking that the measured depth is provided as int or float
        if not isinstance(md, (int, float, type(None))):
            raise TypeError('The measured depth of the borehole must be provided as int or float')

        # Checking that the true vertical depth is provided as int or float
        if not isinstance(tvd, (int, float, type(None))):
            raise TypeError('The altitude of the borehole must be provided as int or float')

        # Checking that the depth_unit is provided as string
        if not isinstance(depth_unit, (str, type(None))):
            raise TypeError('The depth_unit must be provided as string')

        # Checking that the depth unit is one of the possible units
        if depth_unit:
            if depth_unit not in ['m', 'ft']:
                raise ValueError('The depth_unit must be one of the following: m, ft')

        # Checking that the variable vertical is a bool
        if not isinstance(vertical, (bool, type(None))):
            raise TypeError('The variable for defining a vertical borehole must be either True or False')

        # Checking that the contractee is provided as string
        if not isinstance(contractee, (str, type(None))):
            raise TypeError('The contractee of the borehole must be provided as string')

        # Checking that the drilling contractor is provided as string
        if not isinstance(drilling_contractor, (str, type(None))):
            raise TypeError('The drilling contractor of the borehole must be provided as string')

        # Checking that the logging contractor is provided as string
        if not isinstance(logging_contractor, (str, type(None))):
            raise TypeError('The logging contractor of the borehole must be provided as string')

        # Checking that the field is provided as string
        if not isinstance(field, (str, type(None))):
            raise TypeError('The field of the borehole must be provided as string')

        # Checking that the project is provided as string
        if not isinstance(project, (str, type(None))):
            raise TypeError('The project of the borehole must be provided as string')

        # Checking that the start date for drilling is provided as string
        if not isinstance(start_drilling, (str, type(None))):
            raise TypeError('The start date of the drilling must be provided as string')

        # Checking that the end date for drilling is provided as string
        if not isinstance(end_drilling, (str, type(None))):
            raise TypeError('The end date of the drilling must be provided as string')

        # Checking that the start date for logging is provided as string
        if not isinstance(start_logging, (str, type(None))):
            raise TypeError('The start date of the logging must be provided as string')

        # Checking that the end date for logging is provided as string
        if not isinstance(end_logging, (str, type(None))):
            raise TypeError('The end date of the logging must be provided as string')

        # Assigning attributes
        self.address = address

        if self.address:
            self.has_address = True
        else:
            self.has_address = False

        if location:
            self.location = Point(location)
            self.x = list(self.location.coords)[0][0]
            self.y = list(self.location.coords)[0][1]
            self.has_location = True
            self.has_x = True
            self.has_y = True
        else:
            self.location = location
            self.x = None
            self.y = None
            self.has_location = False
            self.has_x = False
            self.has_y = False

        self.crs = crs
        if crs:
            self.crs_pyproj = CRS.from_user_input(self.crs)
            self.has_crs = True
            self.has_crs_pyproj = True
        else:
            self.crs_pyproj = None
            self.has_crs = False
            self.has_crs_pyproj = False

        self.altitude_above_sea_level = altitude_above_sea_level
        self.altitude_above_kb = None

        if self.altitude_above_sea_level:
            self.has_altitude_above_sea_level = True
        else:
            self.has_altitude_above_sea_level = False

        if self.altitude_above_kb:
            self.has_altitude_above_kb = True
        else:
            self.has_altitude_above_kb = False

        self.id = id

        if self.id:
            self.has_id = True
        else:
            self.has_id = False

        self.borehole_type = borehole_type

        if self.borehole_type:
            self.has_borehole_type = True
        else:
            self.has_borehole_type = False

        self.md = md
        self.tvd = tvd

        if self.md:
            self.has_md = True
        else:
            self.has_md = False

        if self.tvd:
            self.has_tvd = True
        else:
            self.has_tvd = False

        if self.tvd:
            if self.altitude_above_sea_level:
                self.tvdss = self.tvd - self.altitude_above_sea_level
                self.has_tvdss = True
        else:
            self.tvdss = None
            self.has_tvdss = False

        self.depth_unit = depth_unit

        if self.depth_unit:
            self.has_depth_unit = True
        else:
            self.has_depth_unit = False

        if vertical:
            self.is_vertical = True
        else:
            self.is_vertical = False

        self.contractee = contractee
        self.drilling_contractor = drilling_contractor
        self.logging_contractor = logging_contractor
        self.field = field
        self.project = project
        self.start_drilling = start_drilling
        self.end_drilling = end_drilling
        self.start_logging = start_logging
        self.end_logging = end_logging

        if contractee:
            self.has_contractree = True
        else:
            self.has_contractree = False

        if self.drilling_contractor:
            self.has_drilling_contractor = True
        else:
            self.has_drilling_contractor = False

        if self.logging_contractor:
            self.has_logging_contractor = True
        else:
            self.has_logging_contractor = False

        if self.field:
            self.has_field = True
        else:
            self.has_field = False

        if self.project:
            self.has_project = True
        else:
            self.has_project = False

        if self.start_drilling:
            self.has_start_drilling = True
        else:
            self.has_start_drilling = False

        if self.end_drilling:
            self.has_end_drilling = True
        else:
            self.has_end_drilling = False

        if self.start_logging:
            self.has_start_logging = True
        else:
            self.has_start_logging = False

        if self.end_logging:
            self.has_end_logging = True
        else:
            self.has_end_logging = False

        # Add Deviation, well logs and well tops
        self.deviation = None
        self.logs = None
        self.well_tops = None
        self.litholog = None
        self.well_design = None

        self.has_deviation = False
        self.has_logs = False
        self.has_well_tops = False
        self.has_litholog = False
        self.has_well_design = False

        # Create borehole DataFrames
        self.df = self.create_df()
        self.properties = self.create_properties_df()

    def create_df(self):
        """Create DataFrame from Borehole Object Attributes.

        Returns
        _______
            df : pd.DataFrame
                DataFrame containing the Borehole Metadata.

        Examples
        ________
            >>> borehole.create_df()
            >>> borehole.df
                                                Value
            Name                                RWE EB1
            Address                             Am Kraftwerk 17, 52249 Eschweiler, Germany
            Location                            POINT (6.313031 50.835676)
            X                                   6.313031
            Y                                   50.835676
            Coordinate Reference System         EPSG:4326
            Coordinate Reference System PyProj  EPSG:4326
            Altitude above sea level            136
            Altitude above KB                   None

        .. versionadded:: 0.0.1
        """
        # Creating dict from attributes
        df_dict = {'ID': self.id,
                   'Name': self.name,
                   'Address': self.address,
                   'Location': self.location,
                   'X': self.x,
                   'Y': self.y,
                   'Coordinate Reference System': self.crs,
                   'Coordinate Reference System PyProj': self.crs_pyproj,
                   'Altitude above sea level': self.altitude_above_sea_level,
                   'Altitude above KB': self.altitude_above_kb,
                   'Measured Depth': self.md,
                   'True Vertical Depth': self.tvd,
                   'True Vertical Depth Sub Sea': self.tvdss,
                   'Depth Unit': self.depth_unit,
                   'Well is vertical': self.is_vertical,
                   'Drilling Contractee': self.contractee,
                   'Drilling Contractor': self.drilling_contractor,
                   'Logging Contractor': self.logging_contractor,
                   'Field': self.field,
                   'Project': self.project,
                   'Start Drilling': self.start_drilling,
                   'End Drilling': self.end_drilling,
                   'Start Logging': self.start_logging,
                   'End Logging': self.end_logging,
                   'Litholog': self.has_litholog,
                   'Well Tops': self.has_well_tops,
                   'Well Deviation': self.has_deviation,
                   'Well Logs': self.has_logs,
                   'Well Design': self.has_well_design
                   }

        # Creating DataFrame from dict
        df = pd.DataFrame.from_dict(data=df_dict,
                                    orient='index',
                                    columns=['Value'])

        return df

    def create_properties_df(self):
        """Create Properties DataFrame from Borehole Object Attributes.

        Returns
        _______
            df : pd.DataFrame
                DataFrame containing the Borehole Properties.

        Examples
        ________
            >>> borehole.create_properties_df()
            >>> borehole.properties
                                                Value
            Name                                True
            Address                             True
            Location                            True
            X                                   True
            Y                                   True
            Coordinate Reference System         True
            Coordinate Reference System PyProj  True
            Altitude above sea level            True
            Altitude above KB                   False

        .. versionadded:: 0.0.1
        """
        # Creating dict from attributes
        df_dict = {'ID': self.has_id,
                   'Name': self.has_name,
                   'Address': self.has_address,
                   'Location': self.has_location,
                   'X': self.has_x,
                   'Y': self.has_y,
                   'Coordinate Reference System': self.has_crs,
                   'Coordinate Reference System PyProj': self.has_crs_pyproj,
                   'Altitude above sea level': self.has_altitude_above_sea_level,
                   'Altitude above KB': self.has_altitude_above_kb,
                   'Measured Depth': self.has_md,
                   'True Vertical Depth': self.has_tvd,
                   'True Vertical Depth Sub Sea': self.has_tvdss,
                   'Depth Unit': self.has_depth_unit,
                   'Drilling Contractee': self.has_contractree,
                   'Drilling Contractor': self.has_drilling_contractor,
                   'Logging Contractor': self.has_logging_contractor,
                   'Field': self.has_field,
                   'Project': self.has_project,
                   'Start Drilling': self.has_start_drilling,
                   'End Drilling': self.has_end_drilling,
                   'Start Logging': self.has_start_logging,
                   'End Logging': self.has_end_logging,
                   'Litholog': self.has_litholog,
                   'Well Tops': self.has_well_tops,
                   'Well Deviation': self.has_deviation,
                   'Well Logs': self.has_logs,
                   'Well Design': self.has_well_design
                   }

        # Creating DataFrame from dict
        df = pd.DataFrame.from_dict(data=df_dict,
                                    orient='index',
                                    columns=['Value'])

        return df

    def update_df(self,
                  data_dict: dict):
        """Update well Object DataFrame with data from data_dict.

        Parameters
        __________
            data_dict : dict
                Dictionary containing the new data, e.g. ``data_dict={'Date': 2023}``.

        Raises
        ______
            TypeError
                If the wrong input data types are provided.

        Examples
        ________
            >>> borehole.update_df(data_dict={'Date': 2023})
            >>> borehole.df
                                                Value
            Name                                RWE EB1
            Address                             Am Kraftwerk 17, 52249 Eschweiler, Germany
            Location                            POINT (6.313031 50.835676)
            X                                   6.313031
            Y                                   50.835676
            Coordinate Reference System         EPSG:4326
            Coordinate Reference System PyProj  EPSG:4326
            Altitude above sea level            136
            Altitude above KB                   None
            Data                                2023

        .. versionadded:: 0.0.1
        """
        # Checking that the data dict is a dict
        if not isinstance(data_dict, dict):
            raise TypeError('data_dict must be a dict')

        # Create DataFrame from dict
        df = pd.DataFrame.from_dict(data=data_dict,
                                    orient='index',
                                    columns=['Value'])

        # Concatenating DataFrames
        self.df = pd.concat([self.df,
                             df])

    def update_value(self,
                     attribute: str,
                     value: Union[int, float, str, tuple],
                     crs: Union[str, pyproj.crs.crs.CRS] = None,
                     transform_coordinates: bool = None):
        """Update attribute and value of Well Object DataFrame.

        Parameters
        __________
            attribute : str
                Borehole object attribute provided as str, e.g. ``attribute='name'``.
            value : Union[int, float, str]
                Value of the attribute to be updated, e.g. ``value='RWE EB2'``.
            crs : Union[str, pyproj.crs.crs.CRS]
                Coordinate Reference System of the coordinates, e.g. ``crs='EPSG:4326'``.
            transform_coordinates : bool
                Boolean value to transform the coordinates if a new Coordinate Reference System is provided, e.g. ``transform_coordinates=True``.

        Raises
        ______
            TypeError
                If the wrong input data types are provided.

        Examples
        ________
            >>> borehole.name
            'RWE EB1'
            >>> borehole.update_value(attribute='name', value='RWE EB2')
            >>> borehole.name
            'RWE EB2'

        .. versionadded:: 0.0.1
        """
        # Checking that the attribute is of type string
        if not isinstance(attribute, str):
            raise TypeError('The attribute name must be provided as string')

        # Checking that the value is of type string, int or float
        if not isinstance(value, (int, float, str, tuple)):
            raise TypeError('The new value must be provided as int, float, or str')

        # Checking that the crs is provided as string or pyproj CRS
        if not isinstance(crs, (str, pyproj.crs.crs.CRS, type(None))):
            raise TypeError('The CRS of the borehole location must be provided as string or pyproject CRS')

        # Checking that the transform_coordinates is provided as bool
        if not isinstance(transform_coordinates, (bool, type(None))):
            raise TypeError('The transform_coordinates argument must be provided as bool')

        # Checking that the attribute is part of the borehole object
        if attribute in vars(self).keys():
            if attribute == 'crs':
                old_crs = self.crs
            vars(self)[attribute] = value
            vars(self)['has_' + attribute] = True

        if attribute == 'location':
            value = Point(value)
            self.location = value
            self.has_location = True
            self.x = list(value.coords)[0][0]
            self.y = list(value.coords)[0][1]
            self.df.loc['X', 'Value'] = self.x
            self.df.loc['Y', 'Value'] = self.y
            self.properties.loc['X', 'Value'] = True
            self.properties.loc['Y', 'Value'] = True

            if crs:
                # Checking that the crs is provided as string or pyproj CRS
                if not isinstance(crs, (str, pyproj.crs.crs.CRS, type(None))):
                    raise TypeError('The CRS of the borehole location must be provided as string or pyproject CRS')

                self.crs = crs
                self.has_crs = True
                self.crs_pyproj = CRS.from_user_input(crs)
                self.has_crs = True
                self.df.loc['Coordinate Reference System', 'Value'] = self.crs
                self.properties.loc['Coordinate Reference System', 'Value'] = True
                self.df.loc['Coordinate Reference System PyProj', 'Value'] = self.crs_pyproj
                self.properties.loc['Coordinate Reference System PyProj', 'Value'] = True
                self.deviation.crs = self.crs

        if attribute == 'crs':
            self.crs = value
            self.has_crs = True
            self.crs_pyproj = CRS.from_user_input(value)
            self.has_crs = True
            self.df.loc['Coordinate Reference System', 'Value'] = self.crs
            self.properties.loc['Coordinate Reference System', 'Value'] = True
            self.df.loc['Coordinate Reference System PyProj', 'Value'] = self.crs_pyproj
            self.properties.loc['Coordinate Reference System PyProj', 'Value'] = True
            self.deviation.crs = self.crs

            if transform_coordinates:
                coords_new = self.to_gdf(crs=old_crs).to_crs(self.crs)['geometry'].loc[0]
                self.location = coords_new
                self.has_location = True
                self.x = list(coords_new.coords)[0][0]
                self.y = list(coords_new.coords)[0][1]
                self.df.loc['X', 'Value'] = self.x
                self.df.loc['Y', 'Value'] = self.y
                self.df.loc['Location', 'Value'] = self.location
                self.properties.loc['X', 'Value'] = True
                self.properties.loc['Y', 'Value'] = True
                self.properties.loc['Location', 'Value'] = True

        # Creating attribute dict
        df_indices_dict = {'id': 'ID',
                           'name': 'Name',
                           'address': 'Address',
                           'location': 'Location',
                           'x': 'X',
                           'y': 'Y',
                           'crs': 'Coordinate Reference System',
                           'crs_pyproj': 'Coordinate Reference System PyProj',
                           'altitude_above_sea_level': 'Altitude above sea level',
                           'altitude_above_kb': 'Altitude above KB',
                           'md': 'Measured Depth',
                           'tvd': 'True Vertical Depth',
                           'tvdss': 'True Vertical Depth Sub Sea',
                           'depth_unit': 'Depth Unit',
                           'vertical': 'Well is vertical',
                           'contractee': 'Drilling Contractee',
                           'drilling_contractor': 'Drilling Contractor',
                           'logging_contractor': 'Logging Contractor',
                           'field': 'Field',
                           'project': 'Project',
                           'start_drilling': 'Start Drilling',
                           'end_drilling': 'End Drilling',
                           'start_logging': 'Start Logging',
                           'end_logging': 'End Logging',
                           }


        # Replace value in DataFrame
        self.df.loc[df_indices_dict[attribute], 'Value'] = value
        self.properties.loc[df_indices_dict[attribute], 'Value'] = True

    def to_gdf(self,
               crs: Union[str, pyproj.crs.crs.CRS] = None):
        """Create GeoDataFrame from Well Object DataFrame.

        Parameters
        __________
            crs : Union[str, pyproj.crs.crs.CRS]
                Coordinate Reference System of the coordinates, e.g. ``crs='EPSG:4326'``.

        Returns
        _______
            gpd.GeoDataFrame

        Examples
        ________
            >>> borehole.to_gdf()
                ID         Name    geometry
            0   DABO123456 RWE EB1 POINT (6.31303 50.83568)

        .. versionadded:: 0.0.1
        """


        # Checking that the crs is provided as string or pyproj CRS
        if not isinstance(crs, (str, pyproj.crs.crs.CRS, type(None))):
            raise TypeError('The CRS of the borehole location must be provided as string or pyproject CRS')

        # Transposing DataFrame
        df = self.df.T.reset_index(drop=True)

        # Setting the CRS if it is not provided
        if not crs:
            crs = df['Coordinate Reference System'].iloc[0]

        # Create GeoDataFrame
        self.gdf = gpd.GeoDataFrame(geometry=[df['Location'].iloc[0]],
                                    crs=crs,
                                    data=df)

        return self.gdf

    def add_deviation(self,
                      path: Union[str, pd.DataFrame],
                      delimiter: str = ',',
                      step: Union[float, int] = 1,
                      md_column: str = 'MD',
                      dip_column: str = 'DIP',
                      azimuth_column: str = 'AZI',
                      add_origin: bool = True):
        """Add deviation to the Borehole Object.

        Parameters
        __________
            path : str
                Path to the deviation file or DataFrame containing the deviation values, e.g. ``path='deviation.csv'``.
            delimiter : str, default: ``','``
                Delimiter to read the deviation file correctly, e.g. ``delimiter=';'``.
            step : Union[float, int], default: ``1``
                Step for resampling the deviation data, e.g. ``step=5``.
            md_column : str, default: ``'MD'``
                Column containing the measured depths, e.g. ``md_column='MD'``.
            dip_column : str, default: ``'DIP'``
                Column containing the dip values, e.g. ``dip_column='DIP'``.
            azimuth_column : str, default: ``'AZI'``
                Column containing the azimuth values, e.g. ``azimuth_column='AZI'``.
            add_origin: bool, default: ``True``
                Boolean value to add the location of the borehole to survey DataFrames.

        Raises
        ______
            TypeError
                If the wrong input data types are provided.
            ValueError
                If the wrong column names are provided.

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

        # Create deviation
        self.deviation = Deviation(borehole=self,
                                   path=path,
                                   delimiter=delimiter,
                                   step=step,
                                   md_column=md_column,
                                   dip_column=dip_column,
                                   azimuth_column=azimuth_column,
                                   add_origin=add_origin)

        self.has_deviation = True
        self.df.loc['Well Deviation', 'Value'] = self.has_deviation
        self.properties.loc['Well Deviation', 'Value'] = self.has_deviation

        # Updating DataFrame
        self.update_df(data_dict=self.deviation.data_dict)

    def add_well_logs(self,
                      path: str,
                      nodata: Union[int, float] = -9999):
        """Add Well Logs to the Borehole Object.

        Parameters
        __________
            path : str
                Path to the well log file, e.g. ``path='Well_Logs.las'``.
            nodata : Union[int, float], default: ``-9999``
                Nodata value to be replaces by `np.NaN`, e.g. ``nodata=-9999``.

        Raises
        ______
            TypeError
                If the wrong input data types are provided.
            ValueError
                If neither of the permitted file types are provided.

        Examples
        ________
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
        # Checking that the path is of type string
        if not isinstance(path, str):
            raise TypeError('path must be provided as str')

        # Opening LAS file if provided
        if path.endswith('.las'):

            # Creating well logs from LAS file
            self.logs = LASLogs(self,
                                path=path)

        # Opening DLIS file if provided
        elif path.endswith('.dlis'):
            # Creating well logs from DLIS file
            self.logs = DLISLogs(self,
                                 path=path,
                                 nodata=nodata)

        else:
            raise ValueError('Please provide a LAS file or DLIS file')

        self.has_logs = True
        self.df.loc['Well Logs', 'Value'] = self.has_logs

    def add_well_tops(self,
                      path: str,
                      delimiter: str = ',',
                      unit: str = 'm'):
        """Add Well Tops to the Borehole Object.

        Parameters
        __________
            path : str
                Path to the well top file, e.g. ``path='Well_Tops.csv'``.
            delimiter : str, default: ``','``
                Delimiter for the well top file, e.g. ``delimiter=','``.
            unit : str
                Unit of the depth measurements, e.g. ``unit='m'``.

        Raises
        ______
            TypeError
                If the wrong input data types are provided.

        Examples
        ________
            >>> borehole.add_well_tops(path='Well_Tops.csv', delimiter=';')
            >>> borehole.well_tops.df
                Top              MD
            0   Infill           3.0
            1   Base Quaternary  9.5
            2   Sand 1           28.5
            3   Clay             32.0

        .. versionadded:: 0.0.1
        """
        # Checking that the path is of type string
        if not isinstance(path, str):
            raise TypeError('The path must be provided as str')

        # Checking that the delimiter is of type str
        if not isinstance(delimiter, str):
            raise TypeError('The delimiter must be of type str')

        # Checking that the unit is provided as string
        if not isinstance(unit, str):
            raise TypeError('The unit must be provided as string')

        # Creating well tops
        self.well_tops = WellTops(path=path,
                                  delimiter=delimiter,
                                  unit=unit)

        self.has_well_tops = True
        self.df.loc['Well Tops', 'Value'] = self.has_well_tops

    def add_litholog(self,
                     path: str,
                     delimiter: str = ','):
        """Add LithoLog to the Borehole Object.

        Parameters
        __________
            path : str
                Path to the LitoLog file, e.g. ``path='LithoLog.csv'``.
            delimiter : str, default: ``','``
                Delimiter for the LithoLog file, e.g. ``delimiter=','``.

        Raises
        ______
            TypeError
                If the wrong input data types are provided.

        Examples
        ________
            >>> borehole.add_litholog(path='LithoLog.csv', delimiter=';')
            >>> borehole.litholog.df
                Top              MD
            0   Infill           3.0
            1   Base Quaternary  9.5
            2   Sand 1           28.5
            3   Clay             32.0

        .. versionadded:: 0.0.1
        """
        # Checking that the path is of type string
        if not isinstance(path, str):
            raise TypeError('path must be provided as str')

        # Checking that the delimiter is of type str
        if not isinstance(delimiter, str):
            raise TypeError('delimiter must be of type str')

        # Creating Litholog
        self.litholog = LithoLog(path=path,
                                 delimiter=delimiter)

        # Setting attributes
        self.has_litholog = True
        self.df.loc['Litholog', 'Value'] = self.has_litholog

    def add_well_design(self):
        """Add well design object to borehole.

        Examples
        ________
            >>> borehole.add_well_design()
            >>> borehole.well_design
            Pipes: {}
            Cements: {}

        .. versionadded:: 0.0.1
        """

        # Setting has well design variable
        self.has_well_design = True

        # Adding well design
        self.well_design = WellDesign(borehole=self)
