from server.auth.sheets_client import GoogleSheetsClient

from thinksoft.core.logger import thinksoft_logger


def test_import():
    assert thinksoft_logger is not None
    assert GoogleSheetsClient is not None
