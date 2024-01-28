import pandas as pd


class WellTops:
    """Class to initiate Well Tops.

    Parameters
    __________
        path : str
            Path to the well tops, e.g. ``path='Well_Tops.csv'``.
        delimiter : str, default: ``','``
            Delimiter to read the well tops file correctly, e.g. ``delimiter=','``.
        top_column : str, default: ``'Top'``
            Name of the column that contains the names of the well tops, e.g. ``top_column='Top'``.
        depth_column : str, default: ``'MD'``
            Name of the column holding the depths, e.g. ``depth_column='MD'``.
        unit : str. default: ``'m'``
            Unit of the depth measurements, e.g. ``unit='m'``.

    Attributes
    __________
        df : pd.DataFrame
            DataFrame containing the loaded Well Tops information. Data columns are as follows:

            ======= ==============================================
            Index   Index of each Well Top
            Top     Name of each Well Top
            MD      Measured depth of each Well Top
            Unit    Unit of the Measured depth of each Well Top
            ======= ==============================================

        top_column : str
            Name of the Well Tops column.
        depth_column : str
            Name of the Depth column.

    Returns
    _______
        WellTops
            Well tops object.

    Raises
    ______
        TypeError
            If the wrong input data types are provided.

    Examples
    ________
        >>> borehole.add_well_tops(path='Well_Tops.csv', delimiter=',', top_column='Top', depth_column='MD', unit='m')
        >>> borehole.well_tops

        ======= ================= ====== ======
        Index   Top	              MD     Unit
        ======= ================= ====== ======
        0       Infill            3.0    m
        1       Base Quaternary   9.5    m
        2       Sand 1            28.5   m
        3       Clay              32.0   m
        4       Sand 2            34.0   m
        5       Lignite 1         36.0   m
        6       Sand 3            44.0   m
        7       Lignite 2         45.2   m
        8       Sand/Clay         50.0   m
        9       GW Level          59.0   m
        10      Base Tertiary     70.0   m
        11      Upper Carb.       100.0  m
        ======= ================= ====== ======

    See Also
    ________
        pyborehole.borehole.Borehole.add_deviation : Add deviation to the Borehole Object.
        pyborehole.borehole.Borehole.add_litholog : Add LithoLog to the Borehole Object.
        pyborehole.borehole.Borehole.add_well_logs : Class to initiate a Well Log Object.
        pyborehole.borehole.Borehole.add_well_design : Add Well Design to the Borehole Object.

    .. versionadded:: 0.0.1
    """

    def __init__(self,
                 path: str,
                 delimiter: str = ',',
                 top_column: str = 'Top',
                 depth_column: str = 'MD',
                 unit: str = 'm'):
        """Class to initiate Well Tops.

        Parameters
        __________
            path : str
                Path to the well tops, e.g. ``path='Well_Tops.csv'``.
            delimiter : str, default: ``','``
                Delimiter to read the well tops file correctly, e.g. ``delimiter=','``.
            top_column : str, default: ``'Top'``
                Name of the column that contains the names of the well tops, e.g. ``top_column='Top'``.
            depth_column : str, default: ``'MD'``
                Name of the column holding the depths, e.g. ``depth_column='MD'``.
            unit : str. default: ``'m'``
                Unit of the depth measurements, e.g. ``unit='m'``.

        Attributes
        __________
            df : pd.DataFrame
                DataFrame containing the loaded Well Tops information
            top_column : str
                Name of the Well Tops column.
            depth_column : str
                Name of the Depth column.

        Returns
        _______
            WellTops
                Well tops object.

        Raises
        ______
            TypeError
                If the wrong input data types are provided.
            Value Error
                If the columns are not present in the DataFrame.

        Examples
        ________
            >>> borehole.add_well_tops(path='Well_Tops.csv', delimiter=',', top_column='Top', depth_column='MD', unit='m')
            >>> borehole.well_tops.df

            ======= ================= ====== ======
            Index   Top	              MD     Unit
            ======= ================= ====== ======
            0       Infill            3.0    m
            1       Base Quaternary   9.5    m
            2       Sand 1            28.5   m
            3       Clay              32.0   m
            4       Sand 2            34.0   m
            5       Lignite 1         36.0   m
            6       Sand 3            44.0   m
            7       Lignite 2         45.2   m
            8       Sand/Clay         50.0   m
            9       GW Level          59.0   m
            10      Base Tertiary     70.0   m
            11      Upper Carb.       100.0  m
            ======= ================= ====== ======

        See Also
        ________
            pyborehole.borehole.Borehole.add_deviation : Add deviation to the Borehole Object.
            pyborehole.borehole.Borehole.add_litholog : Add LithoLog to the Borehole Object.
            pyborehole.borehole.Borehole.add_well_logs : Class to initiate a Well Log Object.
            pyborehole.borehole.Borehole.add_well_design : Add Well Design to the Borehole Object.

        .. versionadded:: 0.0.1
        """

        # Checking that the path is of type str
        if not isinstance(path, str):
            raise TypeError('The path must be provided as string')

        # Checking that the delimiter is of type str
        if not isinstance(delimiter, str):
            raise TypeError('The delimiter must be provided as string')

        # Checking that the top column is of type string
        if not isinstance(top_column, str):
            raise TypeError('Top_column must be provided as string')

        # Checking that the depth column is of type string
        if not isinstance(depth_column, str):
            raise TypeError('Depth_column must be provided as string')

        # Checking that the unit is provided as string
        if not isinstance(unit, str):
            raise TypeError('The unit must be provided as string')

        # Opening Well Tops file
        self.df = pd.read_csv(path, delimiter=delimiter)

        # Checking that the top column is in the DataFrame
        if not {top_column}.issubset(self.df):
            raise ValueError('The Top_column is not part of the Well Tops')

        # Checking that the depth column is in the DataFrame
        if not {depth_column}.issubset(self.df):
            raise ValueError('The depth_column is not part of the Well Tops')

        # Assigning attributes
        self.top_column = top_column
        self.depth_column = depth_column

        # Assigning unit to DataFrame
        self.df['Unit'] = unit
