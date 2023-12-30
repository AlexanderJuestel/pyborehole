import pandas as pd
import pyborehole


class Boreholes:
    """Class to initiate multiple borehole objects.

    Parameters
    __________
        boreholes : list
            List of PyBorehole borehole objects.

    Returns
    _______
        Boreholes

    Raises
    ______
        TypeError
            If the wrong input data types are provided.

    """
    def __init__(self,
                 boreholes: pyborehole.borehole.Borehole):
        """Initiate Boreholes class.

        Parameters
        __________
            boreholes : list
                List of PyBorehole borehole objects.

        Raises
        ______
            TypeError
                If the wrong input data types are provided.

        Examples
        ________
            >>> from pyborehole.boreholes import Boreholes
            >>> boreholes = Boreholes(Borehole.boreholes)
            >>> boreholes

        .. versionadded:: 0.0.1
        """
        # Checking that the boreholes are of type list
        if not isinstance(boreholes, list):
            raise TypeError('The borehole objects must be provided as list, use Borehole.boreholes')

        # Setting borehole attributes
        self.boreholes = boreholes

        # Creating GeoDataFrame for boreholes
        self.gdf = pd.concat([borehole.to_gdf() for borehole in self.boreholes],
                             axis=0).reset_index(drop=True)

        # Getting names of boreholes
        self.names = [borehole.name for borehole in self.boreholes]
