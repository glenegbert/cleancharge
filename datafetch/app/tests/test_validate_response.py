from unittest.mock import patch

import pytest

from jobs.forecast import validate_response


VALID_RESPONSE = {
    "meta": {
        "region": "CAISO_NORTH",
        "signal_type": "co2_moer",
        "units": "lbs_co2_per_mwh",
        "generated_at": "2026-02-12T18:30:00+00:00",
    },
    "data": [
        {"point_time": "2026-02-12T18:30:00+00:00", "value": 100.5},
    ],
}


@patch("jobs.forecast.insert_alert")
def test_valid_response_no_alert(mock_alert):
    validate_response(VALID_RESPONSE)
    mock_alert.assert_not_called()


@patch("jobs.forecast.insert_alert")
def test_valid_response_with_extra_keys_no_alert(mock_alert):
    data = {
        "meta": {**VALID_RESPONSE["meta"], "new_field": "surprise"},
        "data": [{"point_time": "2026-02-12T18:30:00+00:00", "value": 100.5, "extra": 1}],
    }
    validate_response(data)
    mock_alert.assert_not_called()


@patch("jobs.forecast.insert_alert")
def test_missing_top_level_keys(mock_alert):
    with pytest.raises(ValueError):
        validate_response({"something": "else"})
    mock_alert.assert_called_once()
    assert "Missing top-level keys" in mock_alert.call_args[0][2]


@patch("jobs.forecast.insert_alert")
def test_missing_meta_keys(mock_alert):
    data = {
        "meta": {"region": "CAISO_NORTH"},
        "data": [{"point_time": "2026-02-12T18:30:00+00:00", "value": 100.5}],
    }
    validate_response(data)
    mock_alert.assert_called_once()
    assert "Meta keys changed" in mock_alert.call_args[0][2]


@patch("jobs.forecast.insert_alert")
def test_missing_point_keys(mock_alert):
    data = {
        "meta": VALID_RESPONSE["meta"],
        "data": [{"point_time": "2026-02-12T18:30:00+00:00"}],
    }
    validate_response(data)
    mock_alert.assert_called_once()
    assert "Point keys changed" in mock_alert.call_args[0][2]


@patch("jobs.forecast.insert_alert")
def test_empty_data_no_point_alert(mock_alert):
    data = {
        "meta": VALID_RESPONSE["meta"],
        "data": [],
    }
    validate_response(data)
    mock_alert.assert_not_called()
