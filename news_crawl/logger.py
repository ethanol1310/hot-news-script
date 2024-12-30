import logging

from pythonjsonlogger import json


class RequestIDJsonFormatter(json.JsonFormatter):
    def add_fields(self, log_record, record: logging.LogRecord, message_dict):
        super(RequestIDJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp"):
            log_record["timestamp"] = self.formatTime(record)

        if not log_record.get("level"):
            log_record["level"] = record.levelname
        else:
            log_record["level"] = log_record["level"].upper()

        if not log_record.get("caller"):
            log_record["caller"] = f"{record.filename}:{record.lineno}"

        if not log_record.get("message"):
            log_record["message"] = self.formatMessage(record)


logger = logging.getLogger(__name__)
logger.setLevel("INFO")
formatter = RequestIDJsonFormatter("%(timestamp)s %(level)s %(caller)s %(message)s")
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
