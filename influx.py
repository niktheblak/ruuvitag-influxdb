import datetime
import os

from exporter import Exporter
from influxdb import InfluxDBClient

class InfluxDBExporter(Exporter):
    def __init__(self):
        cfg = InfluxDBConfig()
        self._client = InfluxDBClient(
            host=cfg.host,
            port=cfg.port,
            username=cfg.username,
            password=cfg.password,
            database=cfg.database,
            ssl=cfg.ssl,
            verify_ssl=cfg.ssl,
            path=cfg.path
        )
    
    def name(self):
        return "InfluxDB"
    
    def export(self, measurements, ts=None):
        if ts is None:
            ts = datetime.datetime.utcnow()
        for mac, content in measurements:
            points = to_influx_points(ts, mac, content)
            self._client.write_points(points)
    
    def close(self):
        self._client.close()


class InfluxDBConfig:
    def __init__(self):
        self.ssl = os.environ.get("RUUVITAG_INFLUXDB_SSL", "0") == "1"
        self.host = os.environ.get("RUUVITAG_INFLUXDB_HOST", "localhost")
        self.port = int(os.environ.get("RUUVITAG_INFLUXDB_PORT", "8086"))
        self.database = os.environ.get("RUUVITAG_INFLUXDB_DATABASE")
        self.username = os.environ.get("RUUVITAG_INFLUXDB_USERNAME", "root")
        self.password = os.environ.get("RUUVITAG_INFLUXDB_PASSWORD", "root")
        self.path = os.environ.get("RUUVITAG_INFLUXDB_PATH", "")

def to_influx_points(ts, mac, content):
    return [
        {
            "measurement": "values",
            "tags": {
                "name": content["name"],
                "mac": mac
            },
            "time": ts.isoformat(),
            "fields": {
                "temperature": float(content["temperature"]),
                "humidity": float(content["humidity"]),
                "pressure": float(content["pressure"])
            }
        }
    ]
