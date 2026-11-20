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
    assert (counts.loc[r.BASE_YEAR:] == 27).all()


def test_eu_total_matches_owid(df, owid_eu):
    totals = r.eu_totals(r.eu_members(df))
    assert totals.loc[1990, "co2"] == pytest.approx(owid_eu.loc[1990, "co2"], abs=0.1)


def test_report_includes_2024(df, owid_eu):
    totals = r.eu_totals(r.eu_members(df))
    assert totals.loc[2024, "co2"] == pytest.approx(owid_eu.loc[2024, "co2"], abs=0.1)


def test_missing_consumption_stays_missing(df):
    totals = r.eu_totals(r.eu_members(df))
    assert pd.isna(totals.loc[2024, "consumption_co2"])


def test_report_has_no_nan(capsys):
    r.main()
    assert "nan" not in capsys.readouterr().out
