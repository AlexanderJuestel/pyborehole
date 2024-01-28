import pandas as pd
import pytest


def test_well_tops_class():
    from pyborehole.borehole import Borehole, WellTops

    borehole = Borehole(name='Weisweiler R1')

    borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland',
                             location=(3413031, 5835676),
                             year=2024,
                             crs='EPSG:25832')

    borehole.add_well_tops(path='data/Well_Tops.csv',
                           delimiter=';',
                           top_column='Top',
                           depth_column='MD')

    assert isinstance(borehole.well_tops.df, pd.DataFrame)
    assert isinstance(borehole.well_tops.top_column, str)
    assert isinstance(borehole.well_tops.depth_column, str)
    assert borehole.well_tops.top_column == 'Top'
    assert borehole.well_tops.depth_column == 'MD'

    borehole = Borehole(name='Weisweiler R1')

    borehole.init_properties(address='Am Kraftwerk 17, 52249 Eschweiler, Deutschland',
                             location=(3413031, 5835676),
                             year=2024,
                             crs='EPSG:25832')

    with pytest.raises(TypeError):
        well_tops = WellTops(path=['data/Well_Tops.csv'], delimiter=';', top_column='Top', depth_column='MD')

    with pytest.raises(TypeError):
        well_tops = WellTops(path='data/Well_Tops.csv', delimiter=[';'], top_column='Top', depth_column='MD')

    with pytest.raises(TypeError):
        well_tops = WellTops(path='data/Well_Tops.csv', delimiter=';', top_column=['Top'], depth_column='MD')

    with pytest.raises(TypeError):
        well_tops = WellTops(path='data/Well_Tops.csv', delimiter=';', top_column='Top', depth_column=['MD'])

    with pytest.raises(TypeError):
        well_tops = WellTops(path='data/Well_Tops.csv', delimiter=';', top_column='Top', depth_column='MD', unit=['m'])

    with pytest.raises(ValueError):
        well_tops = WellTops(path='data/Well_Tops.csv', delimiter=';', top_column='Tops', depth_column='MD')

    with pytest.raises(ValueError):
        well_tops = WellTops(path='data/Well_Tops.csv', delimiter=';', top_column='Top', depth_column='Depth')
