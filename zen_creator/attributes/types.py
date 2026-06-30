from typing import Union

import pandas as pd

# Type aliases for better readability
DataFrame = Union[pd.DataFrame, pd.Series]
DefaultValue = Union[float, list, None]
