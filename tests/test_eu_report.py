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



def test_per_person_matches_owid(df, owid_eu):
    pp = r.per_person(r.eu_members(df))
    assert pp.loc[1990] == pytest.approx(owid_eu.loc[1990, "co2_per_capita"], abs=0.01)


def test_per_person_is_weighted():
    toy = pd.DataFrame({
        "country": ["A", "B"],
        "year": [1990, 1990],
        "co2": [10.0, 9.0],
        "population": [1_000_000, 9_000_000],
        "co2_per_capita": [10.0, 1.0],
    })
    assert r.per_person(toy).loc[1990] == pytest.approx(1.9)
