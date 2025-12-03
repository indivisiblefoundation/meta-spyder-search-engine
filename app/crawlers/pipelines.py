# app/crawlers/pipelines.py
from elasticsearch import Elasticsearch
from es_client import ES_HOST # Import the shared ES host variable

class ElasticsearchPipeline:
    ES_INDEX = "web_pages"

    def open_spider(self, spider):
        self.client = Elasticsearch(hosts=[ES_HOST])
        # Ensure the index exists, assuming init_es.py was run or auto-created
        if not self.client.indices.exists(index=self.ES_INDEX):
             spider.logger.warning(f"Index {self.ES_INDEX} does not exist!")

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # Index the item into Elasticsearch
        try:
            self.client.index(
                index=self.ES_INDEX,
                document={
                    'url': item['url'],
                    'title': item['title'],
                    'content': item['content'],
                    'timestamp': item['timestamp']
                },
                id=item['url_hash'] # Use a hash for unique document IDs
            )
            spider.logger.info(f"Indexed item: {item['url']}")
        except Exception as e:
            spider.logger.error(f"Failed to index item {item['url']}: {e}")
        return item

