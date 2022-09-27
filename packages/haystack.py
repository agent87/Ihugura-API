from haystack.utils import launch_es
import time
import os
from haystack.document_stores import ElasticsearchDocumentStore



launch_es()

time.sleep(30)

# Get the host where Elasticsearch is running, default to localhost
host = os.environ.get("ELASTICSEARCH_HOST", "localhost")
document_store = ElasticsearchDocumentStore(host=host, username="", password="", index="document")