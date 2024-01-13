import pandas as pd

class WellTops:
    """Class to initiate Well Tops.

    Parameters
    __________
        path : str
            Path to the well tops, e.g. ``path='Well_Tops.csv'``.
        delimiter : str
            Delimiter to read the well tops file correctly, e.g. ``delimiter=','``.
        unit : str
            Unit of the depth measurements, e.g. ``unit='m'``.

    Returns
    _______
        WellTops
            Well tops object.

    Examples
    ________
        >>> borehole.add_well_tops(path='Well_Tops.csv', delimiter=',', unit='m')
        >>> borehole.well_tops

    .. versionadded:: 0.0.1
    """
    def __init__(self,
                 path: str,
                 delimiter: str = ',',
                 unit: str = 'm'):
        """Class to initiate Well Tops.

            Parameters
            __________
                path : str
                    Path to the well tops, e.g. ``path='Well_Tops.csv'``.
                delimiter : str
                    Delimiter to read the well tops file correctly, e.g. ``delimiter=','``.
                unit : str
                    Unit of the depth measurements, e.g. ``unit='m'``.

            Returns
            _______
                WellTops
                    Well tops object.

            Examples
            ________
                >>> borehole.add_well_tops(path='Well_Tops.csv', delimiter=',', unit='m')
                >>> borehole.well_tops.df

            .. versionadded:: 0.0.1
            """

        # Checking that the path is of type str
        if not isinstance(path, str):
            raise TypeError('The path must be provided as string')

        # Checking that the delimiter is of type str
        if not isinstance(delimiter, str):
            raise TypeError('The delimiter must be provided as string')

        # Checking that the unit is provided as string
        if not isinstance(unit, str):
            raise TypeError('The unit must be provided as string')

        self.df = pd.read_csv(path, delimiter=delimiter)

        self.df['Unit'] = unit
