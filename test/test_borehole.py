import pytest
from shapely.geometry import Point
import pyproj
import pandas as pd
import geopandas as gpd
import numpy as np


def test_borehole_class():
    from pyborehole.borehole import Borehole

    borehole = Borehole(name='Weisweiler R1')

    assert borehole.name == 'Weisweiler R1'
    assert isinstance(borehole.name, str)
    assert borehole.has_name is True
    assert borehole.address is None
    assert borehole.has_address is None
    assert borehole.location is None
    assert borehole.has_location is None
    assert borehole.year is None
    assert borehole.has_year is None
    assert borehole.x is None
    assert borehole.y is None
    assert borehole.has_x is None
    assert borehole.has_y is None
    assert borehole.crs is None
    assert borehole.has_crs is None
    assert borehole.crs_pyproj is None
    assert borehole.has_crs_pyproj is None
    assert borehole.altitude_above_sea_level is None
    assert borehole.altitude_above_kb is None
    assert borehole.has_altitude_above_kb is None
    assert borehole.has_altitude_above_sea_level is None
    assert borehole.borehole_id is None
    assert borehole.has_borehole_id is None
    assert borehole.borehole_type is None
    assert borehole.has_borehole_type is None
    assert borehole.md is None
    assert borehole.tvd is None
    assert borehole.tvdss is None
    assert borehole.has_md is None
    assert borehole.has_tvd is None
    assert borehole.has_tvdss is None
    assert borehole.depth_unit is None
    assert borehole.has_depth_unit is None
    assert borehole.is_vertical is None
    assert borehole.contractee is None
    assert borehole.drilling_contractor is None
    assert borehole.logging_contractor is None
    assert borehole.field is None
    assert borehole.project is None
    assert borehole.has_contractee is None
    assert borehole.has_drilling_contractor is None
    assert borehole.has_logging_contractor is None
    assert borehole.has_field is None
    assert borehole.has_project is None
    assert borehole.start_drilling is None
    assert borehole.end_drilling is None
    assert borehole.start_logging is None
    assert borehole.end_logging is None
    assert borehole.has_start_drilling is None
    assert borehole.has_start_logging is None
    assert borehole.has_end_drilling is None
    assert borehole.has_end_logging is None
    assert borehole.deviation is None
    assert borehole.logs is None
    assert borehole.well_tops is None
    assert borehole.litholog is None
    assert borehole.well_design is None
    assert borehole.has_deviation is False
    assert borehole.has_logs is False
    assert borehole.has_well_tops is False
    assert borehole.has_litholog is False
    assert borehole.has_well_design is False
    assert borehole.df is None
    assert borehole.gdf is None
    assert borehole.properties is None


def test_borehole_class_error():
    from pyborehole.borehole import Borehole

    with pytest.raises(TypeError):
        Borehole(name=['Weisweiler R1'])


def test_borehole_class_str():
    from pyborehole.borehole import Borehole

    borehole = Borehole(name='Weisweiler R1')

    assert borehole.__str__() == 'Borehole: Weisweiler R1'
    assert isinstance(borehole.__str__(), str)


def test_borehole_class_repr():
    from pyborehole.borehole import Borehole

    borehole = Borehole(name='Weisweiler R1')

    assert borehole.__repr__() == 'Borehole: Weisweiler R1'
    assert isinstance(borehole.__repr__(), str)


def test_borehole_class_init_properties():
    from pyborehole.borehole import Borehole

    borehole = Borehole(name='Weisweiler R1')

    borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland',
                             location=(6.313031, 50.835676),
                             year=2024,
                             crs='EPSG:4326',
                             altitude_above_sea_level=136.0,
                             altitude_above_kb=140.0,
                             borehole_id='DABO123456',
                             borehole_type='exploration',
                             md=100,
                             tvd=100,
                             depth_unit='m',
                             vertical=True,
                             contractee='RWE Power AG',
                             drilling_contractor='RWE BOWA',
                             logging_contractor='DMT GmbH',
                             field='RWE Geothermie',
                             project='DGE Rollout',
                             start_drilling='2023-10-18',
                             end_drilling='2023-10-28',
                             start_logging='2023-10-28',
                             end_logging='2023-10-29'
                             )

    # Asserting address
    assert borehole.address == 'Am Kraftwerk 17, 52249 Eschweiler, Deutschland'
    assert isinstance(borehole.address, str)
    assert borehole.has_address is True
    assert isinstance(borehole.has_address, bool)

    # Asserting location
    assert borehole.location == Point(6.313031, 50.835676)
    assert isinstance(borehole.location, Point)
    assert borehole.has_location is True
    assert isinstance(borehole.has_location, bool)

    # Asserting coordinates
    assert borehole.x == 6.313031
    assert borehole.y == 50.835676
    assert isinstance(borehole.x, float)
    assert isinstance(borehole.y, float)
    assert borehole.has_x is True
    assert isinstance(borehole.has_x, bool)
    assert borehole.has_y is True
    assert isinstance(borehole.has_y, bool)

    # Asserting year
    assert borehole.year == 2024
    assert isinstance(borehole.year, int)
    assert borehole.has_year is True
    assert isinstance(borehole.has_year, bool)

    # Asserting CRS
    assert borehole.crs == 'EPSG:4326'
    assert borehole.crs_pyproj.name == 'WGS 84'
    assert borehole.crs_pyproj.srs == 'EPSG:4326'
    assert isinstance(borehole.crs, str)
    assert isinstance(borehole.crs_pyproj, pyproj.crs.crs.CRS)
    assert borehole.has_crs is True
    assert isinstance(borehole.has_crs, bool)
    assert borehole.has_crs_pyproj is True
    assert isinstance(borehole.has_crs_pyproj, bool)

    # Asserting altitudes
    assert borehole.altitude_above_sea_level == 136.0
    assert isinstance(borehole.altitude_above_sea_level, float)
    assert borehole.altitude_above_kb == 140.0
    assert isinstance(borehole.altitude_above_kb, float)
    assert borehole.has_altitude_above_sea_level is True
    assert isinstance(borehole.has_altitude_above_sea_level, bool)
    assert borehole.has_altitude_above_kb is True
    assert isinstance(borehole.has_altitude_above_kb, bool)

    # Asserting borehole id
    assert borehole.borehole_id == 'DABO123456'
    assert isinstance(borehole.borehole_id, str)
    assert borehole.has_borehole_id is True
    assert isinstance(borehole.has_borehole_id, bool)

    # Asserting borehole type
    assert borehole.borehole_type == 'exploration'
    assert isinstance(borehole.borehole_type, str)
    assert borehole.has_borehole_type is True
    assert isinstance(borehole.has_borehole_type, bool)

    # Asserting depths
    assert borehole.md == 100
    assert isinstance(borehole.md, int)
    assert borehole.has_md is True
    assert isinstance(borehole.has_md, bool)

    assert borehole.tvd == 100
    assert isinstance(borehole.tvd, int)
    assert borehole.has_tvd is True
    assert isinstance(borehole.has_tvd, bool)

    assert borehole.tvdss == -36
    assert isinstance(borehole.tvdss, float)
    assert borehole.has_tvdss is True
    assert isinstance(borehole.has_tvdss, bool)

    # Asserting depth unit
    assert borehole.depth_unit == 'm'
    assert isinstance(borehole.depth_unit, str)
    assert borehole.has_depth_unit is True
    assert isinstance(borehole.has_depth_unit, bool)

    # Asserting vertical
    assert borehole.is_vertical == True
    assert isinstance(borehole.is_vertical, bool)

    # Asserting meta data
    assert borehole.contractee == 'RWE Power AG'
    assert isinstance(borehole.contractee, str)
    assert borehole.has_contractee is True
    assert isinstance(borehole.has_contractee, bool)

    assert borehole.drilling_contractor == 'RWE BOWA'
    assert isinstance(borehole.drilling_contractor, str)
    assert borehole.has_drilling_contractor is True
    assert isinstance(borehole.has_drilling_contractor, bool)

    assert borehole.logging_contractor == 'DMT GmbH'
    assert isinstance(borehole.logging_contractor, str)
    assert borehole.has_logging_contractor is True
    assert isinstance(borehole.has_logging_contractor, bool)

    assert borehole.field == 'RWE Geothermie'
    assert isinstance(borehole.field, str)
    assert borehole.has_field is True
    assert isinstance(borehole.has_field, bool)

    assert borehole.project == 'DGE Rollout'
    assert isinstance(borehole.project, str)
    assert borehole.has_project is True
    assert isinstance(borehole.has_project, bool)

    assert borehole.start_drilling == '2023-10-18'
    assert isinstance(borehole.start_drilling, str)
    assert borehole.has_start_drilling is True
    assert isinstance(borehole.has_start_drilling, bool)

    assert borehole.end_drilling == '2023-10-28'
    assert isinstance(borehole.end_drilling, str)
    assert borehole.has_end_drilling is True
    assert isinstance(borehole.has_end_drilling, bool)

    assert borehole.start_logging == '2023-10-28'
    assert isinstance(borehole.start_logging, str)
    assert borehole.has_start_logging is True
    assert isinstance(borehole.has_start_logging, bool)

    assert borehole.end_logging == '2023-10-29'
    assert isinstance(borehole.end_logging, str)
    assert borehole.has_end_logging is True
    assert isinstance(borehole.has_end_logging, bool)

    assert borehole.deviation is None
    assert borehole.logs is None
    assert borehole.well_tops is None
    assert borehole.litholog is None
    assert borehole.well_design is None

    assert borehole.has_deviation is False
    assert isinstance(borehole.has_deviation, bool)
    assert borehole.has_logs is False
    assert isinstance(borehole.has_logs, bool)
    assert borehole.has_litholog is False
    assert isinstance(borehole.has_litholog, bool)
    assert borehole.has_well_tops is False
    assert isinstance(borehole.has_well_tops, bool)
    assert borehole.has_well_design is False
    assert isinstance(borehole.has_well_design, bool)

    assert isinstance(borehole.df, pd.DataFrame)
    assert isinstance(borehole.properties, pd.DataFrame)

    borehole.init_properties(address=None,
                             location=None,
                             year=None,
                             crs=None,
                             altitude_above_sea_level=None,
                             altitude_above_kb=None,
                             borehole_id=None,
                             borehole_type=None,
                             md=None,
                             tvd=None,
                             depth_unit=None,
                             vertical=False,
                             contractee=None,
                             drilling_contractor=None,
                             logging_contractor=None,
                             field=None,
                             project=None,
                             start_drilling=None,
                             end_drilling=None,
                             start_logging=None,
                             end_logging=None
                             )

    # Asserting address
    assert borehole.address is None
    assert isinstance(borehole.address, type(None))
    assert borehole.has_address is False
    assert isinstance(borehole.has_address, bool)

    # Asserting location
    assert borehole.location is None
    assert isinstance(borehole.location, type(None))
    assert borehole.has_location is False
    assert isinstance(borehole.has_location, bool)

    # Asserting coordinates
    assert borehole.x is None
    assert borehole.y is None
    assert isinstance(borehole.x, type(None))
    assert isinstance(borehole.y, type(None))
    assert borehole.has_x is False
    assert isinstance(borehole.has_x, bool)
    assert borehole.has_y is False
    assert isinstance(borehole.has_y, bool)

    # Asserting year
    assert borehole.year is None
    assert isinstance(borehole.year, type(None))
    assert borehole.has_year is False
    assert isinstance(borehole.has_year, bool)

    # Asserting CRS
    assert borehole.crs is None
    assert borehole.crs_pyproj is None
    assert isinstance(borehole.crs, type(None))
    assert isinstance(borehole.crs_pyproj, type(None))
    assert borehole.has_crs is False
    assert isinstance(borehole.has_crs, bool)
    assert borehole.has_crs_pyproj is False
    assert isinstance(borehole.has_crs_pyproj, bool)

    # Asserting altitudes
    assert borehole.altitude_above_sea_level is None
    assert isinstance(borehole.altitude_above_sea_level, type(None))
    assert borehole.altitude_above_kb is None
    assert isinstance(borehole.altitude_above_kb, type(None))
    assert borehole.has_altitude_above_sea_level is False
    assert isinstance(borehole.has_altitude_above_sea_level, bool)
    assert borehole.has_altitude_above_kb is False
    assert isinstance(borehole.has_altitude_above_kb, bool)

    # Asserting borehole id
    assert borehole.borehole_id is None
    assert isinstance(borehole.borehole_id, type(None))
    assert borehole.has_borehole_id is False
    assert isinstance(borehole.has_borehole_id, bool)

    # Asserting borehole type
    assert borehole.borehole_type is None
    assert isinstance(borehole.borehole_type, type(None))
    assert borehole.has_borehole_type is False
    assert isinstance(borehole.has_borehole_type, bool)

    # Asserting depths
    assert borehole.md is None
    assert isinstance(borehole.md, type(None))
    assert borehole.has_md is False
    assert isinstance(borehole.has_md, bool)

    assert borehole.tvd is None
    assert isinstance(borehole.tvd, type(None))
    assert borehole.has_tvd is False
    assert isinstance(borehole.has_tvd, bool)

    assert borehole.tvdss is None
    assert isinstance(borehole.tvdss, type(None))
    assert borehole.has_tvdss is False
    assert isinstance(borehole.has_tvdss, bool)

    # Asserting depth unit
    assert borehole.depth_unit is None
    assert isinstance(borehole.depth_unit, type(None))
    assert borehole.has_depth_unit is False
    assert isinstance(borehole.has_depth_unit, bool)

    # Asserting vertical
    assert borehole.is_vertical is False
    assert isinstance(borehole.is_vertical, bool)

    # Asserting meta data
    assert borehole.contractee is None
    assert isinstance(borehole.contractee, type(None))
    assert borehole.has_contractee is False
    assert isinstance(borehole.has_contractee, bool)

    assert borehole.drilling_contractor is None
    assert isinstance(borehole.drilling_contractor, type(None))
    assert borehole.has_drilling_contractor is False
    assert isinstance(borehole.has_drilling_contractor, bool)

    assert borehole.logging_contractor is None
    assert isinstance(borehole.logging_contractor, type(None))
    assert borehole.has_logging_contractor is False
    assert isinstance(borehole.has_logging_contractor, bool)

    assert borehole.field is None
    assert isinstance(borehole.field, type(None))
    assert borehole.has_field is False
    assert isinstance(borehole.has_field, bool)

    assert borehole.project is None
    assert isinstance(borehole.project, type(None))
    assert borehole.has_project is False
    assert isinstance(borehole.has_project, bool)

    assert borehole.start_drilling is None
    assert isinstance(borehole.start_drilling, type(None))
    assert borehole.has_start_drilling is False
    assert isinstance(borehole.has_start_drilling, bool)

    assert borehole.end_drilling is None
    assert isinstance(borehole.end_drilling, type(None))
    assert borehole.has_end_drilling is False
    assert isinstance(borehole.has_end_drilling, bool)

    assert borehole.start_logging is None
    assert isinstance(borehole.start_logging, type(None))
    assert borehole.has_start_logging is False
    assert isinstance(borehole.has_start_logging, bool)

    assert borehole.end_logging is None
    assert isinstance(borehole.end_logging, type(None))
    assert borehole.has_end_logging is False
    assert isinstance(borehole.has_end_logging, bool)

    assert borehole.deviation is None
    assert borehole.logs is None
    assert borehole.well_tops is None
    assert borehole.litholog is None
    assert borehole.well_design is None

    assert borehole.has_deviation is False
    assert isinstance(borehole.has_deviation, bool)
    assert borehole.has_logs is False
    assert isinstance(borehole.has_logs, bool)
    assert borehole.has_litholog is False
    assert isinstance(borehole.has_litholog, bool)
    assert borehole.has_well_tops is False
    assert isinstance(borehole.has_well_tops, bool)
    assert borehole.has_well_design is False
    assert isinstance(borehole.has_well_design, bool)

    assert isinstance(borehole.df, pd.DataFrame)
    assert isinstance(borehole.properties, pd.DataFrame)


def test_borehole_class_init_properties_error():
    from pyborehole.borehole import Borehole

    borehole = Borehole(name='Weisweiler R1')

    with pytest.raises(TypeError):
        borehole.init_properties(address=['Am Kraftwerk 17, 52249 Eschweiler, Deutschland'])

    with pytest.raises(TypeError):
        borehole.init_properties(location=[6.313031, 50.835676])

    with pytest.raises(TypeError):
        borehole.init_properties(year=[2024])

    with pytest.raises(TypeError):
        borehole.init_properties(crs=['EPSG:4326'])

    with pytest.raises(TypeError):
        borehole.init_properties(altitude_above_sea_level=[136.0])

    with pytest.raises(TypeError):
        borehole.init_properties(altitude_above_kb=[140.0])

    with pytest.raises(TypeError):
        borehole.init_properties(borehole_id=['DABO123456'])

    with pytest.raises(TypeError):
        borehole.init_properties(borehole_type=['exploration'])

    with pytest.raises(ValueError):
        borehole.init_properties(borehole_type='Erkundung')

    with pytest.raises(TypeError):
        borehole.init_properties(md='100')

    with pytest.raises(TypeError):
        borehole.init_properties(tvd='100')

    with pytest.raises(TypeError):
        borehole.init_properties(depth_unit=['m'])

    with pytest.raises(ValueError):
        borehole.init_properties(depth_unit='mm')

    with pytest.raises(TypeError):
        borehole.init_properties(vertical='True')

    with pytest.raises(TypeError):
        borehole.init_properties(contractee=['RWE Power AG'])

    with pytest.raises(TypeError):
        borehole.init_properties(drilling_contractor=['RWE BOWA'])

    with pytest.raises(TypeError):
        borehole.init_properties(logging_contractor=['DMT GmbH'])

    with pytest.raises(TypeError):
        borehole.init_properties(field=['RWE Geothermie'])

    with pytest.raises(TypeError):
        borehole.init_properties(project=['DGE Rollout'])

    with pytest.raises(TypeError):
        borehole.init_properties(start_drilling=['2023-10-18'])

    with pytest.raises(TypeError):
        borehole.init_properties(end_drilling=['2023-10-28'])

    with pytest.raises(TypeError):
        borehole.init_properties(start_logging=['2023-10-28'])

    with pytest.raises(TypeError):
        borehole.init_properties(end_logging=['2023-10-29'])


def test_borehole_class_update_df():
    from pyborehole.borehole import Borehole

    borehole = Borehole(name='Weisweiler R1')
    borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland')
    borehole.update_df(data_dict={'Date': 2023})

    borehole.df.loc['Data', 'Value'] = 2023

    with pytest.raises(TypeError):
        borehole.update_df(data_dict='Date')

    with pytest.raises(ValueError):
        borehole = Borehole(name='Weisweiler R1')
        borehole.update_df(data_dict='Date')


def test_borehole_class_update_value():
    from pyborehole.borehole import Borehole

    borehole = Borehole(name='Weisweiler R1')

    borehole.init_properties(location=(6.313031, 50.835676),
                             crs='EPSG:4326')

    data = {'MD': [0, 50, 100],
            'DIP': [2, 2, 2],
            'AZI': [5, 5, 5]}

    df_dev = pd.DataFrame.from_dict(data)

    borehole.add_deviation(path=df_dev,
                           step=25,
                           md_column='MD',
                           dip_column='DIP',
                           azimuth_column='AZI',
                           add_origin=False)
    borehole.update_value(attribute='name', value='RWE EB2')
    assert borehole.name == 'RWE EB2'

    borehole.update_value(attribute='location', value=(6, 50))
    assert borehole.x == 6
    assert borehole.y == 50

    borehole.update_value(attribute='location', value=(6, 50), crs='EPSG:25832')
    assert borehole.x == 6
    assert borehole.y == 50
    assert borehole.crs == 'EPSG:25832'

    borehole.update_value(attribute='crs', value='EPSG:25832', transform_coordinates=True)

    with pytest.raises(TypeError):
        borehole.update_value(attribute=['name'], value='RWE EB2')

    with pytest.raises(TypeError):
        borehole.update_value(attribute='name', value=['RWE EB2'])

    with pytest.raises(TypeError):
        borehole.update_value(attribute='name', value='RWE EB2', transform_coordinates='True')

    with pytest.raises(TypeError):
        borehole.update_value(attribute='location', value=(6, 50), crs=4326)

    with pytest.raises(ValueError):
        borehole = Borehole(name='Weisweiler R1')
        borehole.update_value(attribute='name', value='RWE EB2')


def test_borehole_class_to_gdf():
    from pyborehole.borehole import Borehole

    with pytest.raises(ValueError):
        borehole = Borehole(name='Weisweiler R1')
        borehole.to_gdf()

    with pytest.raises(TypeError):
        borehole = Borehole(name='Weisweiler R1')
        borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland',
                                 location=(6.313031, 50.835676),
                                 year=2024,
                                 crs='EPSG:4326')
        borehole.to_gdf(crs=['EPSG:25832'])

    borehole = Borehole(name='Weisweiler R1')
    borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland',
                             location=(6.313031, 50.835676),
                             year=2024,
                             crs='EPSG:4326')

    gdf = borehole.to_gdf()

    assert isinstance(gdf, gpd.GeoDataFrame)
    assert gdf.crs == 'EPSG:4326'


def test_borehole_class_add_deviation():
    from pyborehole.borehole import Borehole, Deviation

    data = np.array(([0, 50, 100], [0, 0, 0], [0, 0, 0])).T
    df = pd.DataFrame(data, columns=['MD', 'DIP', 'AZI'])

    with pytest.raises(ValueError):
        borehole = Borehole(name='Weisweiler R1')
        borehole.add_deviation(df)

    with pytest.raises(TypeError):
        borehole = Borehole(name='Weisweiler R1')
        borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland',
                                 location=(6.313031, 50.835676),
                                 year=2024,
                                 crs='EPSG:4326')
        borehole.add_deviation(np.array(df))

    with pytest.raises(TypeError):
        borehole = Borehole(name='Weisweiler R1')
        borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland',
                                 location=(6.313031, 50.835676),
                                 year=2024,
                                 crs='EPSG:4326')
        borehole.add_deviation(df, delimiter=5)

    with pytest.raises(TypeError):
        borehole = Borehole(name='Weisweiler R1')
        borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland',
                                 location=(6.313031, 50.835676),
                                 year=2024,
                                 crs='EPSG:4326')
        borehole.add_deviation(df, step='5')

    with pytest.raises(TypeError):
        borehole = Borehole(name='Weisweiler R1')
        borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland',
                                 location=(6.313031, 50.835676),
                                 year=2024,
                                 crs='EPSG:4326')
        borehole.add_deviation(df, md_column=5)

    with pytest.raises(TypeError):
        borehole = Borehole(name='Weisweiler R1')
        borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland',
                                 location=(6.313031, 50.835676),
                                 year=2024,
                                 crs='EPSG:4326')
        borehole.add_deviation(df, dip_column=5)

    with pytest.raises(TypeError):
        borehole = Borehole(name='Weisweiler R1')
        borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland',
                                 location=(6.313031, 50.835676),
                                 year=2024,
                                 crs='EPSG:4326')
        borehole.add_deviation(df, azimuth_column=5)

    with pytest.raises(ValueError):
        borehole = Borehole(name='Weisweiler R1')
        borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland',
                                 location=(6.313031, 50.835676),
                                 year=2024,
                                 crs='EPSG:4326')
        borehole.add_deviation(df, md_column='Measured_Depth')

    borehole = Borehole(name='Weisweiler R1')
    borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland',
                             location=(3413039, 5835676),
                             year=2024,
                             crs='EPSG:25832')
    borehole.add_deviation(df)

    assert borehole.has_properties is True
    assert isinstance(borehole.deviation, Deviation)
    assert borehole.has_deviation is True
    assert borehole.df.loc['Well Deviation', 'Value'] is True


def test_borehole_class_add_well_logs():
    from pyborehole.borehole import Borehole, LASLogs, DLISLogs

    with pytest.raises(ValueError):
        borehole = Borehole(name='Weisweiler R1')
        borehole.add_well_logs(path='Well_Log.las')

    with pytest.raises(TypeError):
        borehole = Borehole(name='Weisweiler R1')
        borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland',
                                 location=(6.313031, 50.835676),
                                 year=2024,
                                 crs='EPSG:4326')
        borehole.add_well_logs(path=['Well_Log.las'])

    with pytest.raises(TypeError):
        borehole = Borehole(name='Weisweiler R1')
        borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland',
                                 location=(6.313031, 50.835676),
                                 year=2024,
                                 crs='EPSG:4326')
        borehole.add_well_logs(path='data/dlis.dlis', nodata=[9999])

    with pytest.raises(ValueError):
        borehole = Borehole(name='Weisweiler R1')
        borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland',
                                 location=(6.313031, 50.835676),
                                 year=2024,
                                 crs='EPSG:4326')
        borehole.add_well_logs(path='data/dlis.xls')

    borehole = Borehole(name='Weisweiler R1')
    borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland',
                             location=(6.313031, 50.835676),
                             year=2024,
                             crs='EPSG:4326')
    borehole.add_well_logs(path='data/las.las')

    assert borehole.has_properties is True
    assert isinstance(borehole.logs, LASLogs)
    assert borehole.has_logs is True
    assert borehole.df.loc['Well Logs', 'Value'] is True

    borehole = Borehole(name='Weisweiler R1')
    borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland',
                             location=(6.313031, 50.835676),
                             year=2024,
                             crs='EPSG:4326')
    borehole.add_well_logs(path='data/dlis.dlis', nodata=9999)

    assert borehole.has_properties is True
    assert isinstance(borehole.logs, DLISLogs)
    assert borehole.has_logs is True
    assert borehole.df.loc['Well Logs', 'Value'] is True

def test_borehole_class_add_well_tops():
    from pyborehole.borehole import Borehole, WellTops

    with pytest.raises(ValueError):
        borehole = Borehole(name='Weisweiler R1')
        borehole.add_well_tops(path='Well_Tops.csv')

    with pytest.raises(TypeError):
        borehole = Borehole(name='Weisweiler R1')
        borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland',
                                 location=(6.313031, 50.835676),
                                 year=2024,
                                 crs='EPSG:4326')
        borehole.add_well_tops(path=['Well_Tops.csv'])

    with pytest.raises(TypeError):
        borehole = Borehole(name='Weisweiler R1')
        borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland',
                                 location=(6.313031, 50.835676),
                                 year=2024,
                                 crs='EPSG:4326')
        borehole.add_well_tops(path='Well_Tops.csv', delimiter=[','])

    with pytest.raises(TypeError):
        borehole = Borehole(name='Weisweiler R1')
        borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland',
                                 location=(6.313031, 50.835676),
                                 year=2024,
                                 crs='EPSG:4326')
        borehole.add_well_tops(path='Well_Tops.csv', unit=['m'])

    borehole = Borehole(name='Weisweiler R1')
    borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland',
                             location=(6.313031, 50.835676),
                             year=2024,
                             crs='EPSG:4326')
    borehole.add_well_tops(path='data/Well_Tops.csv')

    assert borehole.has_properties is True
    assert isinstance(borehole.well_tops, WellTops)
    assert borehole.has_well_tops is True
    assert borehole.df.loc['Well Tops', 'Value'] is True


def test_borehole_class_add_litholog():
    from pyborehole.borehole import Borehole, LithoLog

    with pytest.raises(ValueError):
        borehole = Borehole(name='Weisweiler R1')
        borehole.add_litholog(path='Well_Tops.csv')

    with pytest.raises(TypeError):
        borehole = Borehole(name='Weisweiler R1')
        borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland',
                                 location=(6.313031, 50.835676),
                                 year=2024,
                                 crs='EPSG:4326')
        borehole.add_litholog(path=['Well_Tops.csv'])

    with pytest.raises(TypeError):
        borehole = Borehole(name='Weisweiler R1')
        borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland',
                                 location=(6.313031, 50.835676),
                                 year=2024,
                                 crs='EPSG:4326')
        borehole.add_litholog(path='Well_Tops.csv', delimiter=[','])

    borehole = Borehole(name='Weisweiler R1')
    borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland',
                             location=(6.313031, 50.835676),
                             year=2024,
                             crs='EPSG:4326')
    borehole.add_litholog(path='data/Well_Tops.csv')

    assert borehole.has_properties is True
    assert isinstance(borehole.litholog, LithoLog)
    assert borehole.has_litholog is True
    assert borehole.df.loc['Litholog', 'Value'] is True


def test_borehole_class_add_well_design():
    from pyborehole.borehole import Borehole, WellDesign

    with pytest.raises(ValueError):
        borehole = Borehole(name='Weisweiler R1')
        borehole.add_well_design()

    borehole = Borehole(name='Weisweiler R1')
    borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland',
                             location=(6.313031, 50.835676),
                             year=2024,
                             crs='EPSG:4326')
    borehole.add_well_design()

    assert borehole.has_properties is True
    assert borehole.has_well_design is True
    assert isinstance(borehole.well_design, WellDesign)
    assert borehole.df.loc['WellDesign', 'Value'] is True
