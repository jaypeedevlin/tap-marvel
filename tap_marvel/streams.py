"""Stream type classes for tap-marvel."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable
import logging
from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_marvel.client import MarvelStream

# Reusable type properties
image_type = th.ObjectType(
    th.Property("path", th.StringType),
    th.Property("extension", th.StringType),
)

url_type = th.ObjectType(
    th.Property("type", th.StringType),
    th.Property("url", th.StringType),
)


class CharactersStream(MarvelStream):
    name = "characters"
    path = "/characters"
    primary_keys = ["id"]
    list_entities_to_unpack = ["comics", "stories", "events", "series"]

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("description", th.StringType),
        th.Property("modified", th.DateTimeType),
        th.Property("resourceURI", th.StringType),
        th.Property("thumbnail", image_type),
        th.Property("urls", th.ArrayType(url_type)),
        th.Property("comics", th.ArrayType(th.IntegerType)),
        th.Property("stories", th.ArrayType(th.IntegerType)),
        th.Property("events", th.ArrayType(th.IntegerType)),
        th.Property("series", th.ArrayType(th.IntegerType)),
    ).to_dict()

class ComicsStream(MarvelStream):
    name = "comics"
    path = "/comics"
    primary_keys = ["id"]
    list_entities_to_unpack = ["creators", "characters", "stories", "events"]
    entities_to_unpack = ["variants", "collections", "collectedIssues"]

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("digitalId", th.IntegerType),
        th.Property("title", th.StringType),
        th.Property("issueNumber", th.NumberType),
        th.Property("variantDescription", th.StringType),
        th.Property("description", th.StringType),
        th.Property("modified", th.DateTimeType),
        th.Property("isbn", th.StringType),
        th.Property("upc", th.StringType),
        th.Property("diamondCode", th.StringType),
        th.Property("ean", th.StringType),
        th.Property("issn", th.StringType),
        th.Property("format", th.StringType),
        th.Property("pageCount", th.IntegerType),
        th.Property("textObjects", th.ArrayType(th.ObjectType(
            th.Property("type", th.StringType),
            th.Property("language", th.StringType),
            th.Property("text", th.StringType),
        ))),
        th.Property("resourceURI", th.StringType),
        th.Property("urls", th.ArrayType(url_type)),
        th.Property("series", th.IntegerType),
        th.Property("variants", th.ArrayType(th.IntegerType)),
        th.Property("collections", th.ArrayType(th.IntegerType)),
        th.Property("collectedIssues", th.ArrayType(th.IntegerType)),
        th.Property("dates", th.ArrayType(th.ObjectType(
            th.Property("type", th.StringType),
            th.Property("date", th.DateTimeType),
        ))),
        th.Property("prices", th.ArrayType(th.ObjectType(
            th.Property("type", th.StringType),
            th.Property("price", th.NumberType),
        ))),
        th.Property("thumbnail", image_type),
        th.Property("images", th.ArrayType(image_type)),
        th.Property("creators", th.ArrayType(th.IntegerType)),
        th.Property("characters", th.ArrayType(th.IntegerType)),
        th.Property("stories", th.ArrayType(th.IntegerType)),
        th.Property("events", th.ArrayType(th.IntegerType)),
    ).to_dict()

    def post_process(self, row: dict, context: dict | None = None) -> dict | None:
        row = super().post_process(row, context)

        row["series"] = self.extract_id_from_entity(row["series"])

        return row

class CreatorsStream(MarvelStream):
    name = "creators"
    path = "/creators"
    primary_keys = ["id"]
    list_entities_to_unpack = ["series", "comics", "stories", "events"]

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("firstName", th.StringType),
        th.Property("middleName", th.StringType),
        th.Property("lastName", th.StringType),
        th.Property("suffix", th.StringType),
        th.Property("fullName", th.StringType),
        th.Property("modified", th.DateTimeType),
        th.Property("resourceURI", th.StringType),
        th.Property("urls", th.ArrayType(url_type)),
        th.Property("thumbnail", image_type),
        th.Property("series", th.ArrayType(th.IntegerType)),
        th.Property("stories", th.ArrayType(th.IntegerType)),
        th.Property("comics", th.ArrayType(th.IntegerType)),
        th.Property("events", th.ArrayType(th.IntegerType)),
    ).to_dict()

    def post_process(self, row: dict, context: dict | None = None) -> dict | None:
        row = super().post_process(row, context)

        return row

class EventsStream(MarvelStream):
    name = "events"
    path = "/events"
    primary_keys = ["id"]
    list_entities_to_unpack = ["comics", "stories", "series", "characters", "creators"]

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("title", th.StringType),
        th.Property("description", th.StringType),
        th.Property("resourceURI", th.StringType),
        th.Property("urls", th.ArrayType(url_type)),
        th.Property("modified", th.DateTimeType),
        th.Property("start", th.DateTimeType),
        th.Property("end", th.DateTimeType),
        th.Property("thumbnail", image_type),
        th.Property("comics", th.ArrayType(th.IntegerType)),
        th.Property("stories", th.ArrayType(th.IntegerType)),
        th.Property("series", th.ArrayType(th.IntegerType)),
        th.Property("characters", th.ArrayType(th.IntegerType)),
        th.Property("creators", th.ArrayType(th.IntegerType)),
        th.Property("next", th.IntegerType),
        th.Property("previous", th.IntegerType),
    ).to_dict()

    def post_process(self, row: dict, context: dict | None = None) -> dict | None:
        row = super().post_process(row, context)

        for column in ["next", "previous"]:
            if row[column] is not None:
                row[column] = self.extract_id_from_entity(row[column])

        return row

class SeriesStream(MarvelStream):
    name = "series"
    path = "/series"
    primary_keys = ["id"]
    list_entities_to_unpack = ["comics", "stories", "events", "characters", "creators"]

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("title", th.StringType),
        th.Property("type", th.StringType),
        th.Property("description", th.StringType),
        th.Property("resourceURI", th.StringType),
        th.Property("urls", th.ArrayType(url_type)),
        th.Property("startYear", th.IntegerType),
        th.Property("endYear", th.IntegerType),
        th.Property("rating", th.StringType),
        th.Property("modified", th.DateTimeType),
        th.Property("thumbnail", image_type),
        th.Property("comics", th.ArrayType(th.IntegerType)),
        th.Property("stories", th.ArrayType(th.IntegerType)),
        th.Property("events", th.ArrayType(th.IntegerType)),
        th.Property("characters", th.ArrayType(th.IntegerType)),
        th.Property("creators", th.ArrayType(th.IntegerType)),
        th.Property("next", th.IntegerType),
        th.Property("previous", th.IntegerType),
    ).to_dict()

    def post_process(self, row: dict, context: dict | None = None) -> dict | None:
        row = super().post_process(row, context)

        for column in ["next", "previous"]:
            if row[column] is not None:
                row[column] = self.extract_id_from_entity(row[column])

        return row

class StoriesStream(MarvelStream):
    name = "stories"
    path = "/stories"
    primary_keys = ["id"]
    list_entities_to_unpack = ["comics", "series", "events", "characters", "creators"]

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("title", th.StringType),
        th.Property("description", th.StringType),
        th.Property("resourceURI", th.StringType),
        th.Property("type", th.StringType),
        th.Property("modified", th.DateTimeType),
        th.Property("thumbnail", image_type),
        th.Property("comics", th.ArrayType(th.IntegerType)),
        th.Property("series", th.ArrayType(th.IntegerType)),
        th.Property("events", th.ArrayType(th.IntegerType)),
        th.Property("characters", th.ArrayType(th.IntegerType)),
        th.Property("creators", th.ArrayType(th.IntegerType)),
        th.Property("originalIssue", th.IntegerType),
    ).to_dict()

    def post_process(self, row: dict, context: dict | None = None) -> dict | None:
        row = super().post_process(row, context)

        if row["originalIssue"] is not None:
            row["originalIssue"] = self.extract_id_from_entity(row["originalIssue"])

        return row
