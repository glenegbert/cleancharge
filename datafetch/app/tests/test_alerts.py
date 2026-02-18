from unittest.mock import patch, MagicMock

from lib.alerts import insert_alert, alert_from_exception


@patch("lib.alerts.get_client")
def test_insert_alert(mock_get_client):
    mock_ch = MagicMock()
    mock_get_client.return_value = mock_ch

    insert_alert("schema_change", "forecast_job", "Keys changed", "extra details")

    mock_ch.insert.assert_called_once()
    args = mock_ch.insert.call_args
    assert args[0][0] == "alerts"
    row = args[0][1][0]
    assert row[1] == "schema_change"
    assert row[2] == "forecast_job"
    assert row[3] == "Keys changed"
    assert row[4] == "extra details"


@patch("lib.alerts.get_client")
def test_insert_alert_default_details(mock_get_client):
    mock_ch = MagicMock()
    mock_get_client.return_value = mock_ch

    insert_alert("test_type", "test_source", "test message")

    row = mock_ch.insert.call_args[0][1][0]
    assert row[4] == ""


@patch("lib.alerts.insert_alert")
def test_alert_from_exception(mock_insert):
    try:
        raise ValueError("something broke")
    except Exception as e:
        alert_from_exception("my_source", e)

    mock_insert.assert_called_once()
    kwargs = mock_insert.call_args[1]
    assert kwargs["alert_type"] == "unhandled_error"
    assert kwargs["source"] == "my_source"
    assert kwargs["message"] == "something broke"
    assert "ValueError" in kwargs["details"]
