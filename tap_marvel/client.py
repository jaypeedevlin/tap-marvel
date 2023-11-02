"""REST client handling, including MarvelStream base class."""

import requests
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable
from abc import abstractmethod
from dateutil import parser
import logging

from memoization import cached
import time
from hashlib import md5

from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream
from singer_sdk.pagination import BaseOffsetPaginator

class MarvelPaginator(BaseOffsetPaginator):
    def __init__(
        self,
        start_value: int,
        page_size: int,
        developer_mode: bool,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Create a new paginator.
        Args:
            start_value: Initial value.
            page_size: Constant page size.
            args: Paginator positional arguments.
            kwargs: Paginator keyword arguments.
        """
        super().__init__(start_value, page_size, *args, **kwargs)
        self.developer_mode = developer_mode

    def has_more(self, response: requests.Response) -> bool:
        """Override this method to check if the endpoint has any pages left.
        Args:
            response: API response object.
        Returns:
            Boolean flag used to indicate if the endpoint has more pages.
        """
        if self.developer_mode:
            return False

        count = response.json()['data']['count']

        if count < self._page_size:
            return False
        else:
            return True

class MarvelStream(RESTStream):
    """Marvel stream class."""

    url_base = "https://gateway.marvel.com/v1/public"
    records_jsonpath = "$.data.results[*]"
    replication_key = "modified"
    list_entities_to_unpack: list = []
    entities_to_unpack: list = []

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")

        return headers

    def get_new_paginator(self):
        return MarvelPaginator(start_value=0, page_size=100, developer_mode=self.config.get('developer_mode'))

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        # Auth params
        ts = str(time.time())
        public_key = self.config.get("public_key")
        private_key = self.config.get("private_key")
        hash = md5((ts + private_key + public_key).encode('utf-8')).hexdigest()

        params = {
            'ts': ts,
            'apikey': public_key,
            'hash': hash,
            'modifiedSince': self.get_starting_replication_key_value(context),
            'orderBy': 'modified',
            'offset': next_page_token,
            'limit': 100,
        }

        return params

    def extract_id_from_entity(self, entity: dict) -> int:
        uri = entity['resourceURI']
        return int(uri.split('/')[-1])

    def post_process(self, row: dict, context: dict | None = None) -> dict | None:
        for column_name in self.list_entities_to_unpack:
            row[column_name] = [self.extract_id_from_entity(i) for i in row[column_name]['items']]

        for column_name in self.entities_to_unpack:
            row[column_name] = [self.extract_id_from_entity(i) for i in row[column_name]]

        # Handle Invalid Dates
        try:
            parser.isoparse(row["modified"])
        except ValueError:
            row["modified"] == "1970-01-01T00:00:00+0000"

        # Handle Non-stringy String Values
        string_columns = [column for column, value
                          in self.schema["properties"].items()
                          if 'string' in value['type']]

        for column in string_columns:
            value = row[column]
            if not isinstance(value, str) and value is not None:
                row[column] = str(value)

        return row
