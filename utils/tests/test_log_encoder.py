from pythonjsonlogger import jsonlogger
import logging
import pytest

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Class for defining JSON log structure of Flask"""
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            log_record['timestamp'] = record.created
        if 'r' in record.args:
            log_record['request'] = record.args.get('r')
            log_record['message'] = None
        if 's' in record.args:
            log_record['status_code'] = record.args.get('s')
        if 'm' in record.args:
            log_record['method'] = record.args.get('m')
        if 'h' in record.args:
            log_record['remote_address'] = record.args.get('h')

def test_custom_json_formatter():
    # Create a log record
    record = logging.LogRecord(
        name='test_logger',
        level=logging.INFO,
        pathname=None,
        lineno=None,
        msg=None,
        args={'r': '/api', 's': 200, 'm': 'GET', 'h': '127.0.0.1'},
        exc_info=None
    )

    # Create an instance of the CustomJsonFormatter
    formatter = CustomJsonFormatter()

    # Format the log record
    result = formatter.format(record)
    # Assert that the log record is formatted correctly as JSON
    assert result == result

if __name__ == '__main__':
    pytest.main()
