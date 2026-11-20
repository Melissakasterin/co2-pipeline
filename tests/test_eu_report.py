import matplotlib

matplotlib.use("Agg")  # draw charts without opening a window

import pandas as pd
import pytest

import eu_report as r


@pytest.fixture(scope="module")
def df():
    return r.load()


@pytest.fixture(scope="module")
def owid_eu(df):
    """Our World in Data's own row for the 27 member states."""
    return df[df["country"] == "European Union (27)"].set_index("year")


def test_report_runs():
    r.main()


def test_eu_has_27_members(df):
    counts = r.eu_members(df).groupby("year")["country"].nunique()
    assert (counts == 27).all()


def test_eu_total_matches_owid(df, owid_eu):
    totals = r.eu_totals(r.eu_members(df))
    assert totals.loc[1990, "co2"] == pytest.approx(owid_eu.loc[1990, "co2"], abs=0.1)
