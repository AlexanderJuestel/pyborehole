import pytest
from shapely.geometry import Point
import pyproj
import pandas as pd


def test_borehole_class():
    from pyborehole.borehole import Borehole

    borehole = Borehole(name='Weisweiler R1',
                        address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland',
                        location=(6.313031, 50.835676),
                        crs='EPSG:4326',
                        altitude_above_sea_level=136.0)

    assert borehole.name == 'Weisweiler R1'
    assert isinstance(borehole.name, str)
    assert borehole.address == 'Am Kraftwerk 17, 52249 Eschweiler, Deutschland'
    assert isinstance(borehole.address, str)
    assert borehole.location == Point(6.313031, 50.835676)
    assert isinstance(borehole.location, Point)
    assert borehole.x == 6.313031
    assert borehole.y == 50.835676
    assert isinstance(borehole.x, float)
    assert isinstance(borehole.y, float)
    assert borehole.crs == 'EPSG:4326'
    assert isinstance(borehole.crs, str)
    assert isinstance(borehole.crs_pyproj, pyproj.crs.crs.CRS)
    assert borehole.altitude_above_sea_level == 136
    assert isinstance(borehole.altitude_above_sea_level, float)
    assert borehole.deviation is None
    assert borehole.logs is None
    assert isinstance(borehole.df, pd.DataFrame)
    assert borehole.__str__() == 'Weisweiler R1'

    borehole.update_df({'newname': 'Weisweiler R2'})
    assert borehole.df.T['newname'].iloc[0] == 'Weisweiler R2'

    data = {'MD': [0, 50, 100],
            'DIP': [2, 2, 2],
            'AZI': [5, 5, 5]}

    df_dev = pd.DataFrame.from_dict(data)

    borehole.add_deviation(path=df_dev,
                           step=25,
                           md_column='MD',
                           dip_column='DIP',
                           azimuth_column='AZI')


def test_borehole_class_error():
    from pyborehole.borehole import Borehole

    with pytest.raises(TypeError):
        borehole = Borehole(name=['Weisweiler R1'],
                            address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland',
                            location=(6.313031, 50.835676),
                            crs='EPSG:4326',
                            altitude_above_sea_level=136.0)
    with pytest.raises(TypeError):
        borehole = Borehole(name='Weisweiler R1',
                            address=['Am Kraftwerk 17, 52249 Eschweiler, Deutschland'],
                            location=(6.313031, 50.835676),
                            crs='EPSG:4326',
                            altitude_above_sea_level=136.0)

    with pytest.raises(TypeError):
        borehole = Borehole(name='Weisweiler R1',
                            address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland',
                            location=[6.313031, 50.835676],
                            crs='EPSG:4326',
                            altitude_above_sea_level=136.0)

    with pytest.raises(TypeError):
        borehole = Borehole(name='Weisweiler R1',
                            address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland',
                            location=(6.313031, 50.835676),
                            crs=['EPSG:4326'],
                            altitude_above_sea_level=136.0)

    with pytest.raises(TypeError):
        borehole = Borehole(name='Weisweiler R1',
                            address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland',
                            location=(6.313031, 50.835676),
                            crs='EPSG:4326',
                            altitude_above_sea_level=[136.0])

# def test_create_df():
#    assert False


# def test_update_df():
#    assert False


# def test_add_deviation():
#    assert False


# def test_add_well_logs():
#    assert False
