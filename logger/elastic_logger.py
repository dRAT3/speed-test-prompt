import logging
from logstash_formatter import LogstashFormatterV1
from elasticsearch import Elasticsearch

# Setup Elasticsearch client
es_client = Elasticsearch(["http://localhost:9200"])

# Create a logging handler that sends logs to Elasticsearch
class ElasticsearchHandler(logging.Handler):
    def __init__(self, es_client, index_name="python-logs"):
        super().__init__()
        self.es_client = es_client
        self.index_name = index_name

    def emit(self, record):
        try:
            # Format the record and send it to Elasticsearch
            log_entry = self.format(record)
            self.es_client.index(index=self.index_name, body=log_entry)
        except Exception as e:
            print(f"Error sending log to Elasticsearch: {e}")

# Set up logger
logger = logging.getLogger('elastic_logger')
logger.setLevel(logging.INFO)

# Use the Logstash format for structured logs
formatter = LogstashFormatterV1()

# Create the ElasticsearchHandler
es_handler = ElasticsearchHandler(es_client)
es_handler.setFormatter(formatter)

# Add the Elasticsearch handler to the logger
logger.addHandler(es_handler)

# Log messages
logger.info('This is an info message to Elasticsearch!')
