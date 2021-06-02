from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple


class SortOrder(str, Enum):
    ASC = "ASC"
    DESC = "DESC"


@dataclass
class Sort:
    clause: str
    order: SortOrder

    def to_solr(self) -> str:
        return f"{self.clause} ${self.order.value}"


@dataclass
class SolrQuery:
    """ A Solr query representation reflecting Solr's query params"""

    # the query
    q: str

    # the filter queries
    fq: List[str] = None

    # the sort clause
    sort: List[Sort] = None

    # the returned fields
    fl: List[str] = None

    # the number of docs to return
    rows: int = 10

    # any other param
    other_params: List[Tuple[str, str]] = None

    def to_url_params(self) -> List[Tuple[str, str]]:
        url_params = []

        url_params.append(("q", self.q))
        url_params.extend([("fq", filter_query) for filter_query in self.fq])

        if self.sort is not None:
            url_params.append(("sort", self.sort))

        if self.fl is not None and len(self.fl) > 0:
            url_params.append(("fl", ','.join(self.fl)))

        if self.rows is not None:
            url_params.append(("rows", self.rows))

        url_params.extend(self.other_params)

        return url_params
