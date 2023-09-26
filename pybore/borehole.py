import pandas as pd
import numpy as np
from shapely.geometry import Point
from pyproj import CRS
import matplotlib.pyplot as plt


class Borehole:

    def __init__(self,
                 name,
                 address,
                 location,
                 crs,
                 altitude_above_sea_level):
        # Defining attributes
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
        # Creating dict from attributes
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
        df = pd.DataFrame.from_dict(df_dict,
                                    orient='index',
                                    columns=['Value'])

        return df

    def update_df(self, data_dict):
        # Creating DataFrame from dict
        df = pd.DataFrame.from_dict(data_dict,
                                    orient='index',
                                    columns=['Value'])

        # Concatenating DataFrames
        self.df = pd.concat([self.df, df])

    def add_deviation(self,
                      path,
                      delimiter,
                      step):
        # Create deviation
        self.deviation = Deviation(path=path,
                                   delimiter=delimiter,
                                   step=step)

        # Updating DataFrame
        self.update_df(self.deviation.data_dict)

    def add_well_logs(self,
                      path):
        # Creating well logs
        self.logs = Logs(path=path)

    #def get_mesh_along_borehole_path(self,
    #                                 log):



    # def read_boreholeml(self):
    # def write_boreholeml(self):


class Deviation():

    def __init__(self,
                 path,
                 delimiter,
                 step=5):

        # Importing wellpathpy
        try:
            import wellpathpy as wp
        except ModuleNotFoundError:
            ModuleNotFoundError('wellpathpy package not installed')

        # Opening deviation file
        md, inc, azi = wp.read_csv(path,
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

        # Creating data dict
        data_dict = {'Measured Depth': [self.md],
                     'Inclination': [self.inc],
                     'Azimuth': [self.azi],
                     'True Vertical Depth': [self.tvd],
                     'Northing_rel': [self.northing_rel],
                     'Easting_rel': [self.easting_rel]
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
                                  x=0,
                                  y=0,
                                  z=0):

        self.desurveyed_df['Northing'] = self.desurveyed_df['Northing_rel'] + y
        self.desurveyed_df['Easting'] = self.desurveyed_df['Easting_rel'] + x
        self.desurveyed_df['True Vertical Depth Below Sea Level'] = z - self.desurveyed_df['True Vertical Depth']

    def plot_deviation_polar_plot(self):
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)
        az = np.arctan2(self.easting_rel,
                        self.northing_rel)
        radius = np.sqrt(self.northing_rel ** 2 + self.easting_rel ** 2)
        ax.plot(az, radius)

        return fig, ax

    def plot_deviation_3d(self,
                          elev=45,
                          azim=45,
                          roll=0):

        fig, ax = plt.subplots(subplot_kw={'projection': '3d'})

        ax.plot(self.easting_rel,
                self.northing_rel,
                -self.tvd)

        ax.view_init(elev, azim, roll)
        ax.set_xlabel('Easting')
        ax.set_ylabel('Northing')
        ax.set_zlabel('TVD')

        plt.tight_layout()

        return fig, ax

    def get_borehole_tube(self,
                          radius=10,
                          x=0,
                          y=0):

        # Importing pyvista
        try:
            import pyvista as pv
        except ModuleNotFoundError:
            ModuleNotFoundError('PyVista package not installed')

        def lines_from_points(points):
            """Given an array of points, make a line set"""
            poly = pv.PolyData()
            poly.points = points
            cells = np.full((len(points) - 1, 3), 2, dtype=np.int_)
            cells[:, 1] = np.arange(0, len(points) - 1, dtype=np.int_)
            cells[:, 2] = np.arange(1, len(points), dtype=np.int_)
            poly.lines = cells
            return poly

        spline = lines_from_points(np.c_[self.easting_rel+x,
                                         self.northing_rel+y,
                                         self.tvd])

        tube = spline.tube(radius=radius)

        return tube


class Logs:

    def __init__(self, path):

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
                       tracks):

        df = self.df[tracks].reset_index()

        fig, ax = plt.subplots(1, len(tracks), figsize=(len(tracks) * 2, 8))

        for i in range(len(tracks)):
            ax[i].plot(df[tracks[i]], df['MD'])
            ax[i].grid()
            ax[i].invert_yaxis()
            buffer = (max(df['MD']) - min(df['MD'])) / 20
            ax[i].set_ylim(max(df['MD']) + buffer, min(df['MD']) - buffer)

        return fig, ax

    # def get_log_along_well_path(self):
    # see GemGIS function
