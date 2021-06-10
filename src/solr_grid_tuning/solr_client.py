import json
import requests

from typing import Tuple, Optional
from urllib.parse import urlencode, quote

from solr_grid_tuning.solr_query import SolrQuery


class SolrClient:

    def __init__(self, base_url: str, auth: Optional[Tuple[str, str]], collection: str, request_handler):
        self.base_url = base_url
        self.auth = auth
        self.request_handler = request_handler
        self.collection = collection

    def query(self, q: SolrQuery):
        url = f"{self.base_url}/{self.collection}/{self.request_handler}"
        params_encoded = urlencode(q.to_url_params(), quote_via=quote)
        response = requests.get(url, auth=self.auth, params=params_encoded)
        response_js = json.loads(response.text.replace('tuning(', '').replace(')', ''))

        return {
            "statuscode": response.status_code,
            "QTime": response_js["responseHeader"]["QTime"] if response.status_code == 200 else None,
            "numFound": response_js["response"]["numFound"] if response.status_code == 200 else None,
            "docs": response_js["response"]["docs"] if response.status_code == 200 else None
        }
