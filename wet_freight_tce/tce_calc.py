import numpy as np
import pandas as pd

from wet_freight_tce import route_consts as const


## TCE Calculation Notes
## https://www.balticexchange.com/content/balticexchange/consumer/en/my-baltic/downloads.html

# https://www.balticexchange.com/content/dam/balticexchange/consumer/members-area/documents/data_services/market_information/tce-dirty/TD2-TCE_Calculation.pdf
# https://www.balticexchange.com/content/dam/balticexchange/consumer/members-area/documents/data_services/market_information/tce_documents/TC2_37-TCE_Calculation.pdf

# From balticexchange.com -> my baltic -> documentation (left hand menu) -> Tanker TCE calculator
# https://www.balticexchange.com/content/dam/balticexchange/consumer/members-area/documents/data_services/documentation/tce/Baltic%20Exchange%20Tanker%20TCE%20Calculator%20v2.0%20.xlsx
# https://www.balticexchange.com/content/dam/balticexchange/consumer/members-area/documents/data_services/documentation/tce/2023%20Baltic%20Exchange%20Tanker%20TCE%20Calculator%20v3.0.xlsx


# Note: add +5 for bunker premium
def extract_bunker_prices(row, prem=5):
    vlsfo = row.VLSFO + prem
    mgo = row.MGO + prem
    # hsfo = row.HSFO + prem
    # return vlsfo, mgo, hsfo
    return vlsfo, mgo


def china_eca_fuel_history(row, voyage_days):
    vlsfo, mgo = extract_bunker_prices(row)

    if row.name.year >= 2020:  # IMO
        return vlsfo * voyage_days["voyage_noneca"] + mgo * voyage_days["voyage_eca"]
    # if row.name.year >= 2019:  # Pre-IMO, China ECA
    #     return hsfo * voyage_days['voyage_noneca'] + mgo * voyage_days['voyage_eca']
    # else:
    #     return hsfo * (voyage_days['voyage_noneca'] + voyage_days['voyage_eca'])


def eca_fuel_history(row):
    vlsfo, mgo = extract_bunker_prices(row, prem=0)
    voyage_eca = row["Total LSMGO ECA Cons"]
    voyage_noneca = row["Total IFO Non ECA Cons"]

    if row.name.year >= 2020:  # IMO
        return vlsfo * voyage_noneca + mgo * voyage_eca
    # if row.name.year >= 2014:  # Pre-IMO
    #     return hsfo * voyage_noneca + mgo * voyage_eca
    # if row.name >= pd.to_datetime('2010-07-06'):  # ECA 1%
    #     return hsfo * voyage_noneca + mgo * voyage_eca
    # else:
    #     return hsfo * (voyage_noneca + voyage_eca)


def non_eca_fuel_history(row, voyage_days):
    vlsfo, mgo = extract_bunker_prices(row)

    if row.name.year >= 2020:  # IMO
        return vlsfo * voyage_days["voyage_noneca"]
    # if row.name.year >= 2014:  # Pre-IMO
    #     return hsfo * voyage_days['voyage_noneca']


def route_eca_calcs(c, data):
    days_loading, days_discharging, days_waiting, days_canal = (
        c["Days-Loading"],
        c["Days-Discharging"],
        c["Days-Waiting"],
        c["Days-Canal"],
    )
    weather_fac, knots_ballast, knots_laden = (
        c["Weather Factor:"],
        c["Knots Ballast"],
        c["Knots Laden"],
    )
    loadingfuel, dischargefuel, waiting_fuel = (
        c["LoadingFuel"],
        c["DischargeFuel"],
        c["WaitingFuel"],
    )

    # non eca
    days_ballast_non_eca = (
        c["Ballast Miles Non ECA"] * (1 + weather_fac) / (knots_ballast * 24)
    )
    days_laden_non_eca = (
        c["Laden Miles Non ECA"] * (1 + weather_fac) / (knots_laden * 24)
    )
    ballast_ifo_non_eca = (days_ballast_non_eca + days_canal) * c["IFO-Ballast"]
    laden_ifo_non_eca = (days_laden_non_eca + days_canal) * c["IFO-Laden"]
    loading_ifo = (
        (days_loading * c["IFO-Port (Loading)"]) if loadingfuel == "IFO" else 0
    )
    discharge_ifo = (
        (days_discharging * c["IFO-Port (Discharging)"])
        if dischargefuel == "IFO"
        else 0
    )
    waiting_ifo = (days_waiting * c["IFO-Anchor"]) if waiting_fuel == "IFO" else 0

    data["Total IFO Non ECA Cons"] = (
        ballast_ifo_non_eca
        + laden_ifo_non_eca
        + loading_ifo
        + discharge_ifo
        + waiting_ifo
    )

    # eca
    days_ballast_eca = c["Ballast Miles ECA"] * (1 + weather_fac) / (knots_ballast * 24)
    days_laden_eca = c["Laden Miles ECA"] * (1 + weather_fac) / (knots_laden * 24)
    ballast_lsmgo_eca = (days_ballast_eca) * c["IFO-Ballast"]
    laden_lsmgo_eca = (days_laden_eca) * c["IFO-Laden"]
    loading_lsmgo = (
        (days_loading * c["IFO-Port (Loading)"]) if loadingfuel == "LSMGO" else 0
    )
    discharge_lsmgo = (
        (days_discharging * c["IFO-Port (Discharging)"])
        if dischargefuel == "LSMGO"
        else 0
    )
    waiting_lsmgo = (days_waiting * c["IFO-Anchor"]) if waiting_fuel == "LSMGO" else 0

    data["Total LSMGO ECA Cons"] = (
        ballast_lsmgo_eca
        + laden_lsmgo_eca
        + loading_lsmgo
        + discharge_lsmgo
        + waiting_lsmgo
    )
    data["Total voyage days"] = (
        days_ballast_non_eca
        + days_laden_non_eca
        + days_ballast_eca
        + days_laden_eca
        + days_loading
        + days_discharging
        + days_waiting
        + days_canal
    )
    return data


def calc(route, data):
    route = route.upper()
    if "Freight_USDMT" not in data.columns:
        data["Freight_USDMT"] = data.FlatRate * (data.WorldScale / 100)

    c = const.route_data[route]
    dwt = c["Cargo Quantity (Mts)"]

    data["GrossFreight"] = dwt * data["Freight_USDMT"]

    grt = const.route_data[route]["$ per GRT"]
    if pd.notnull(grt):
        data["GrossFreight"] = data["GrossFreight"] + (c["GRT"] * c["$ per GRT"])

    wx_fixed_differential = const.route_data[route]["WS Fixed Differential"]
    if pd.notnull(wx_fixed_differential):
        data["GrossFreight"] = data["GrossFreight"] + (dwt * wx_fixed_differential)

    ls = c["Lumpsum"]

    if ls == "YES":
        data["GrossFreight"] = data["WorldScale"]

    # Bunker costs
    # if route in const.route_using_sing_fuels:  # convert Sing MGO to bbl
    #    data['MGO'] = data['MGO'] * 7.45

    data = route_eca_calcs(c, data)

    data["BunkerCost"] = data.apply(lambda x: eca_fuel_history(x), 1)

    # Net Freight
    data["NetFreight"] = data["GrossFreight"] * ((100 - c["Commission %"]) / 100)
    # Total Costs
    data["TotalExpenses"] = (
        data.BunkerCost + c["Charges - Load port"] + c["Charges - Discharge port"]
    )
    # TCE
    data["NetIncome"] = data.NetFreight - data.TotalExpenses
    data["TCE"] = data.NetIncome / data["Total voyage days"]

    return data


def get_tce_calc_raw_data():
    f = r"2023 Baltic Exchange Tanker TCE Calculator v3.0.xlsx"
    df = pd.read_excel(
        f, sheet_name="Default settings", skiprows=[0, 1, 2, 3], index_col="Description"
    )
    df = df[~df.index.isin(["WS Flat Rate", "WS %", np.NaN])]
    df = df.replace(to_replace=np.NaN, value=0)
    d = df.to_dict()
    import pprint

    pprint.pprint(d, sort_dicts=False)
    return d


if __name__ == "__main__":
    get_tce_calc_raw_data()
