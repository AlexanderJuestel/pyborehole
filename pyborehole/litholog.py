import pandas as pd

class LithoLog:
    """Class to initiate the LithoLog.

    Parameters
    __________
        path : str
            Path to the litholog, e.g. ``path='LithoLog.csv'``.
        delimiter : str
            Delimiter to read the litholog file correctly, e.g. ``delimiter=','``.

    Returns
    _______
        LithoLog
            Litho log object.

    Raises
    ______
        TypeError
            If the wrong input data types are provided.

    Examples
    ________
        >>> borehole.add_litholog(path='LithoLog.csv', delimiter=',', unit='m')
        >>> borehole.litholog.df

    .. versionadded:: 0.0.1
    """

    def __init__(self,
                 path: str,
                 delimiter: str = ',', ):
        """Class to initiate the LithoLog.

            Parameters
            __________
                path : str
                    Path to the litholog, e.g. ``path='LithoLog.csv'``.
                delimiter : str
                    Delimiter to read the litholog file correctly, e.g. ``delimiter=','``.

            Returns
            _______
                LithoLog
                    Litho log object.

            Raises
            ______
                TypeError
                    If the wrong input data types are provided.

            Examples
            ________
                >>> borehole.add_litholog(path='LithoLog.csv', delimiter=',', unit='m')
                >>> borehole.litholog.df

            .. versionadded:: 0.0.1
            """

        # Checking that the path is of type str
        if not isinstance(path, str):
            raise TypeError('The path must be provided as string')

        # Checking that the delimiter is of type str
        if not isinstance(delimiter, str):
            raise TypeError('The delimiter must be provided as string')

        self.df = pd.read_csv(path, delimiter=delimiter)

