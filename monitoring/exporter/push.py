from prometheus_client import REGISTRY
from google.cloud import monitoring_v3
import time, os

PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
client  = monitoring_v3.MetricServiceClient()

def push_to_cloudmonitoring():
    # iterate Prom metrics and push as custom metrics every 30 s
    ts = time.time()

    for metric in REGISTRY.collect():
        for sample in metric.samples:
            series = monitoring_v3.TimeSeries()
            series.metric.type = f"custom.googleapis.com/{sample.name}"
            series.resource.type = "global"
            series.points.add(value={"double_value": sample.value},
                              interval={
                                  "end_time": {"seconds": int(ts)}
                              })
            client.create_time_series(name=f"projects/{PROJECT}",
                                      time_series=[series]) 