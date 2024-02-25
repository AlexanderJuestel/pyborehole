import pytest
import numpy as np
import pandas as pd
import numpy


def test_deviation_class():
    from pyborehole.borehole import Borehole, Deviation

    data = np.array(([0, 50, 100], [0, 0, 0], [0, 0, 0])).T
    df = pd.DataFrame(data, columns=['MD', 'DIP', 'AZI'])

    borehole = Borehole(name='Weisweiler R1')

    borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland',
                             location=(3413031, 5835676),
                             year=2024,
                             crs='EPSG:25832')

    borehole.add_deviation(df)

    borehole.add_deviation(path='data/Well_Deviation.csv')

    assert isinstance(borehole.deviation.md, np.ndarray)
    assert isinstance(borehole.deviation.inc, np.ndarray)
    assert isinstance(borehole.deviation.azi, np.ndarray)
    assert isinstance(borehole.deviation.tvd, np.ndarray)
    assert isinstance(borehole.deviation.northing_rel, np.ndarray)
    assert isinstance(borehole.deviation.easting_rel, np.ndarray)
    assert isinstance(borehole.deviation.az, np.ndarray)
    assert isinstance(borehole.deviation.radius, np.ndarray)
    assert isinstance(borehole.deviation.deviation_df, pd.DataFrame)
    assert isinstance(borehole.deviation.desurveyed_df, pd.DataFrame)
    assert isinstance(borehole.deviation.northing, type(None))
    assert isinstance(borehole.deviation.easting, type(None))
    assert isinstance(borehole.deviation.tvdss, type(None))

    borehole = Borehole(name='Weisweiler R1')

    borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland',
                             location=(3413031, 5835676),
                             year=2024,
                             crs='EPSG:25832')

    with pytest.raises(TypeError):
        deviation = Deviation(borehole=borehole, path=np.array(df), delimiter=',')

    with pytest.raises(TypeError):
        deviation = Deviation(borehole=borehole, path=df, delimiter=[','])

    with pytest.raises(TypeError):
        deviation = Deviation(borehole=borehole, path=df, delimiter=',', step=[50])

    with pytest.raises(TypeError):
        deviation = Deviation(borehole=borehole, path=df, delimiter=',', step=50,
                              md_column=['MD'])

    with pytest.raises(TypeError):
        deviation = Deviation(borehole=borehole, path=df, delimiter=',', step=50,
                              dip_column=['DIP'])

    with pytest.raises(TypeError):
        deviation = Deviation(borehole=borehole, path=df, delimiter=',', step=50,
                              azimuth_column=['AZI'])

    with pytest.raises(ValueError):
        deviation = Deviation(borehole=borehole, path=df, delimiter=',', step=50,
                              md_column='Measured')

    with pytest.raises(TypeError):
        deviation = Deviation(borehole=borehole, path=df, delimiter=',', step=50,
                              add_origin='True')

    with pytest.raises(ValueError):
        borehole = Borehole(name='Weisweiler R1')

        borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland',
                                 location=(3413031, 5835676),
                                 year=2024,
                                 crs='EPSG:4326')
        deviation = Deviation(borehole=borehole, path=df, delimiter=',', step=50,
                              add_origin=True)


def test_deviation_class_add_origin_to_desurveying():
    from pyborehole.borehole import Borehole, Deviation

    data = np.array(([0, 50, 100], [0, 0, 0], [0, 0, 0])).T
    df = pd.DataFrame(data, columns=['MD', 'DIP', 'AZI'])

    borehole = Borehole(name='Weisweiler R1')

    borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland',
                             location=(1000, 1000),
                             altitude_above_sea_level=100,
                             year=2024,
                             crs='EPSG:25832')

    borehole.add_deviation(df)

    borehole.deviation.add_origin_to_desurveying()

    assert isinstance(borehole.deviation.northing, np.ndarray)
    assert isinstance(borehole.deviation.easting, np.ndarray)
    assert isinstance(borehole.deviation.tvdss, np.ndarray)

    with pytest.raises(TypeError):
        borehole.deviation.add_origin_to_desurveying(x=[5])
    with pytest.raises(TypeError):
        borehole.deviation.add_origin_to_desurveying(y=[5])
    with pytest.raises(TypeError):
        borehole.deviation.add_origin_to_desurveying(z=[5])

    with pytest.raises(ValueError):
        borehole.deviation.crs = 'EPSG:4326'
        borehole.deviation.add_origin_to_desurveying()


def test_deviation_class_plot_deviation_polar_plot():
    from pyborehole.borehole import Borehole, Deviation

    data = np.array(([0, 50, 100], [0, 0, 0], [0, 0, 0])).T
    df = pd.DataFrame(data, columns=['MD', 'DIP', 'AZI'])

    borehole = Borehole(name='Weisweiler R1')

    borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland',
                             location=(1000, 1000),
                             altitude_above_sea_level=100,
                             year=2024,
                             crs='EPSG:25832')

    borehole.add_deviation(df)

    borehole.deviation.plot_deviation_polar_plot()

    with pytest.raises(TypeError):
        borehole.deviation.plot_deviation_polar_plot(c='viridis')

    with pytest.raises(TypeError):
        borehole.deviation.plot_deviation_polar_plot(vmin=[0])

    with pytest.raises(TypeError):
        borehole.deviation.plot_deviation_polar_plot(vmax=[10])

    with pytest.raises(TypeError):
        borehole.deviation.plot_deviation_polar_plot(cmap=['viridis'])

    borehole.deviation.plot_deviation_polar_plot(c=borehole.deviation.tvd)


def test_deviation_class_plot_deviation_3d():
    from pyborehole.borehole import Borehole, Deviation

    data = np.array([[0., 0., 0.],
                     [10., 0., 0.],
                     [20., 0., 0.],
                     [30., 0., 0.],
                     [40., 0., 0.],
                     [50., 0., 0.],
                     [60., 0., 0.],
                     [70., 0., 0.],
                     [80., 0., 0.],
                     [90., 0., 0.],
                     [100., 0., 0.]])
    df = pd.DataFrame(data, columns=['MD', 'DIP', 'AZI'])

    borehole = Borehole(name='Weisweiler R1')

    borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland',
                             location=(1000, 1000),
                             altitude_above_sea_level=100,
                             year=2024,
                             crs='EPSG:25832')

    borehole.add_deviation(df)

    borehole.deviation.plot_deviation_3d()

    with pytest.raises(TypeError):
        borehole.deviation.plot_deviation_3d(elev=[45])

    with pytest.raises(TypeError):
        borehole.deviation.plot_deviation_3d(azim=[315])

    with pytest.raises(TypeError):
        borehole.deviation.plot_deviation_3d(roll=[5])

    with pytest.raises(TypeError):
        borehole.deviation.plot_deviation_3d(relative='True')

    with pytest.raises(ValueError):
        borehole.deviation.plot_deviation_3d(relative=False)

    borehole.deviation.add_origin_to_desurveying()
    borehole.deviation.plot_deviation_3d(relative=False)

def test_deviation_class_get_borehole_tube():
    from pyborehole.borehole import Borehole, Deviation

    data = np.array([[0., 0., 0.],
                     [10., 0., 0.],
                     [20., 0., 0.],
                     [30., 0., 0.],
                     [40., 0., 0.],
                     [50., 0., 0.],
                     [60., 0., 0.],
                     [70., 0., 0.],
                     [80., 0., 0.],
                     [90., 0., 0.],
                     [100., 0., 0.]])
    df = pd.DataFrame(data, columns=['MD', 'DIP', 'AZI'])

    borehole = Borehole(name='Weisweiler R1')

    borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland',
                             location=(1000, 1000),
                             altitude_above_sea_level=100,
                             year=2024,
                             crs='EPSG:25832')

    borehole.add_deviation(df)

    tube = borehole.deviation.get_borehole_tube()

    import pyvista as pv
    assert isinstance(tube, pv.core.pointset.PolyData)

    with pytest.raises(TypeError):
        borehole.deviation.get_borehole_tube(radius=[10])

    with pytest.raises(TypeError):
        borehole.deviation.get_borehole_tube(x=[10])

    with pytest.raises(TypeError):
        borehole.deviation.get_borehole_tube(y=[10])

    with pytest.raises(TypeError):
        borehole.deviation.get_borehole_tube(relative='True')

    with pytest.raises(ValueError):
        borehole.deviation.get_borehole_tube(relative=False)

    borehole.deviation.add_origin_to_desurveying()
    tube = borehole.deviation.get_borehole_tube(relative=False)

    import pyvista as pv
    assert isinstance(tube, pv.core.pointset.PolyData)
