import pandas as pd
import pytest

from wet_freight_tce import tce_calc


def test_tc2():
    ds = '2021-10-08'
    dd = {'FlatRate': 12.31,
          'WorldScale': 100.0,
          'MGO': 705.25,
          'VLSFO': 565.25,
          'HSFO': 560.25,
          }
    data = pd.DataFrame(dd, index=[pd.to_datetime(ds)])
    res = tce_calc.calc('TC2_37', data)

    assert res['GrossFreight'][ds] == pytest.approx(486042.91, abs=1e-1)
    assert res['BunkerCost'][ds] == pytest.approx(413495.95, abs=1e-1)
    assert res['TCE'][ds] == pytest.approx(-1436.96, abs=1e-1)


def test_tc5():
    ds = '2021-10-06'

    dd = {
        'FlatRate': 20.46,
        'WorldScale': 103.14,
        'MGO': 355.001,
        'VLSFO': 577.27,
        'HSFO': 225.79,
    }

    data = pd.DataFrame(dd, index=[pd.to_datetime(ds)])
    res = tce_calc.calc('tc5', data)

    assert res['GrossFreight'][ds] == pytest.approx(1175484.42, abs=1e-1)
    assert res['BunkerCost'][ds] == pytest.approx(846632.20, abs=1e-1)
    assert res['TCE'][ds] == pytest.approx(4137.76, abs=1e-1)


def test_tc6():
    ds = '2021-10-06'

    dd = {
        'FlatRate': 20.46,
        'WorldScale': 103.14,
        'MGO': 300.00,
        'VLSFO': 300.00,
        'HSFO': 300.00,
    }

    data = pd.DataFrame(dd, index=[pd.to_datetime(ds)])
    res = tce_calc.calc('tc6', data)

    assert res['GrossFreight'][ds] == pytest.approx(633073.32, abs=1e-1)
    assert res['BunkerCost'][ds] == pytest.approx(35721.95, abs=1e-1)
    assert res['TCE'][ds] == pytest.approx(54612.99, abs=1e-1)


def test_tc7():
    ds = '2021-10-06'

    dd = {
        'FlatRate': 20.46,
        'WorldScale': 103.14,
        'MGO': 300.00,
        'VLSFO': 300.00,
        'HSFO': 300.00,
    }

    data = pd.DataFrame(dd, index=[pd.to_datetime(ds)])
    res = tce_calc.calc('tc7', data)

    assert res['GrossFreight'][ds] == pytest.approx(738585.54, abs=1e-1)
    assert res['BunkerCost'][ds] == pytest.approx(251519.11, abs=1e-1)
    assert res['TCE'][ds] == pytest.approx(10653.90, abs=1e-1)


def test_tc12():
    ds = '2021-10-06'

    dd = {
        'FlatRate': 20.46,
        'WorldScale': 103.14,
        'MGO': 300.00,
        'VLSFO': 300.00,
        'HSFO': 300.00,
    }

    data = pd.DataFrame(dd, index=[pd.to_datetime(ds)])
    res = tce_calc.calc('tc12', data)

    assert res['GrossFreight'][ds] == pytest.approx(746985.54, abs=1e-1)
    assert res['BunkerCost'][ds] == pytest.approx(316151.05, abs=1e-1)
    assert res['TCE'][ds] == pytest.approx(7288.96, abs=1e-1)


def test_tc14():
    ds = '2021-10-06'

    dd = {
        'FlatRate': 20.46,
        'WorldScale': 103.14,
        'MGO': 300.00,
        'VLSFO': 300.00,
        'HSFO': 300.00,
    }

    data = pd.DataFrame(dd, index=[pd.to_datetime(ds)])
    res = tce_calc.calc('tc14', data)

    assert res['GrossFreight'][ds] == pytest.approx(801892.87, abs=1e-1)
    assert res['BunkerCost'][ds] == pytest.approx(286288.24, abs=1e-1)
    assert res['TCE'][ds] == pytest.approx(9701.94, abs=1e-1)


def test_td3c():
    ds = '2021-10-06'

    dd = {
        'FlatRate': 20.46,
        'WorldScale': 103.14,
        'MGO': 300.00,
        'VLSFO': 300.00,
        'HSFO': 300.00,
    }

    data = pd.DataFrame(dd, index=[pd.to_datetime(ds)])
    res = tce_calc.calc('td3 c', data)

    assert res['GrossFreight'][ds] == pytest.approx(5770559.88, abs=1e-1)
    assert res['BunkerCost'][ds] == pytest.approx(828927.18, abs=1e-1)
    assert res['TCE'][ds] == pytest.approx(95881.53, abs=1e-1)


def test_td7():
    ds = '2021-10-06'

    dd = {
        'FlatRate': 20.46,
        'WorldScale': 103.14,
        'MGO': 300.00,
        'VLSFO': 300.00,
        'HSFO': 300.00,
    }

    data = pd.DataFrame(dd, index=[pd.to_datetime(ds)])
    res = tce_calc.calc('td7', data)

    assert res['GrossFreight'][ds] == pytest.approx(1688195.52, abs=1e-1)
    assert res['BunkerCost'][ds] == pytest.approx(75808.78, abs=1e-1)
    assert res['TCE'][ds] == pytest.approx(169852.40, abs=1e-1)


def test_td20():
    ds = '2021-10-06'

    dd = {
        'FlatRate': 20.46,
        'WorldScale': 103.14,
        'MGO': 300.00,
        'VLSFO': 300.00,
        'HSFO': 300.00,
    }

    data = pd.DataFrame(dd, index=[pd.to_datetime(ds)])
    res = tce_calc.calc('td20', data)

    assert res['GrossFreight'][ds] == pytest.approx(2854205.71, abs=1e-1)
    assert res['BunkerCost'][ds] == pytest.approx(497147.02, abs=1e-1)
    assert res['TCE'][ds] == pytest.approx(59488.38, abs=1e-1)


def test_td22():
    ds = '2021-10-06'

    dd = {
        'FlatRate': 20.46,
        'WorldScale': 103.14,
        'MGO': 300.00,
        'VLSFO': 300.00,
        'HSFO': 300.00,
    }

    data = pd.DataFrame(dd, index=[pd.to_datetime(ds)])
    res = tce_calc.calc('td22', data)

    assert res['GrossFreight'][ds] == pytest.approx(103.14, abs=1e-1)
    assert res['BunkerCost'][ds] == pytest.approx(2009377.42, abs=1e-1)
    assert res['TCE'][ds] == pytest.approx(-20053.24, abs=1e-1)


def test_td25():
    ds = '2021-10-06'

    dd = {
        'FlatRate': 20.46,
        'WorldScale': 103.14,
        'MGO': 300.00,
        'VLSFO': 300.00,
        'HSFO': 300.00,
    }

    data = pd.DataFrame(dd, index=[pd.to_datetime(ds)])
    res = tce_calc.calc('td25', data)

    assert res['GrossFreight'][ds] == pytest.approx(1549726.08, abs=1e-1)
    assert res['BunkerCost'][ds] == pytest.approx(454951.02, abs=1e-1)
    assert res['TCE'][ds] == pytest.approx(22829.36, abs=1e-1)