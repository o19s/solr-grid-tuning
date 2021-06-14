import json
import requests

from typing import Tuple, Optional
from urllib.parse import urlencode, quote

from solr_grid_tuning.solr_query import SolrQuery


class SolrClient:

    def __init__(self, base_url: str, auth: Optional[Tuple[str, str]] = None, collection: Optional[str] = None,
                 request_handler: Optional[str] = None):
        self.base_url = base_url
        self.auth = auth
        self.request_handler = request_handler
        self.collection = collection

    def query(self, q: SolrQuery):
        url = "/".join(url_element for url_element in [self.base_url, self.collection, self.request_handler] if url_element)
        params_encoded = urlencode(q.to_url_params(), quote_via=quote)
        response = requests.get(url, auth=self.auth, params=params_encoded)
        response_text = response.text

        # some adjustments for "noisy" response (e.g. when passing json.wrf)
        if not response_text.startswith("{"):
            response_text = response_text[response_text.find("{"):]
        if not response_text.endswith("}"):
            response_text = response_text[:response_text.rfind("}")+1]

        response_js = json.loads(response_text)

        return {
            "statuscode": response.status_code,
            "QTime": response_js["responseHeader"]["QTime"] if response.status_code == 200 else None,
            "numFound": response_js["response"]["numFound"] if response.status_code == 200 else None,
            "docs": response_js["response"]["docs"] if response.status_code == 200 else None
        }
