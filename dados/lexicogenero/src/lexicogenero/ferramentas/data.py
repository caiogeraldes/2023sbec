"""
File: data.py
Author: Caio Geraldes
Email: caio.geraldes@usp.br
Github: https://github.com/caiogeraldes
Description: Ferramentas para trabalho com dataframes gerados a partir de ./diorisis_reader.py
"""

import pandas as pd
import numpy as np
from typing import Any, List


def gera_paragrafo(data: pd.DataFrame) -> pd.DataFrame:
    """docstring for gera_paragrafo"""

    loc_data = data.location.str.split(".", n=1, expand=True).rename({0: "div_sup", 1: "par"}, axis=1)

    data = pd.concat([data, loc_data], axis=1)

    data.dropna(inplace=True)

    j: Any = data.groupby(["author", "text", "file", "div_sup", "par", "genero"]).agg(
        {"lemma": lambda x: " ".join(x)}
    )

    i: Any = j.reset_index()

    return i.loc[:, :]


def gera_sent(data: pd.DataFrame) -> pd.DataFrame:
    """docstring for gera_sent"""

    loc_data = data.location.str.split(".", n=1, expand=True).rename({0: "div_sup", 1: "par"}, axis=1)

    data = pd.concat([data, loc_data], axis=1)

    data.dropna(inplace=True)
    j: Any = data.groupby(["author", "text", "file", "sent_id", "genero"]).agg(
        {"lemma": lambda x: " ".join(x)}
    )

    i: Any = j.reset_index()

    return i.loc[:, :]


def gera_hist_filo(data: pd.DataFrame, lst_hist: List[str]) -> pd.DataFrame:
    data["genero"] = np.nan
    data["genero"] = data["genero"].astype("str")
    data.loc[data.file.isin(lst_hist), "genero"] = "hist"
    data.genero.fillna("filo", inplace=True)
    return data
