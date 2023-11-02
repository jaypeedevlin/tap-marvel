"""Marvel tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_marvel.streams import (
    CharactersStream,
    ComicsStream,
    CreatorsStream,
    EventsStream,
    SeriesStream,
    StoriesStream,
)

STREAM_TYPES = [
    CharactersStream,
    ComicsStream,
    CreatorsStream,
    EventsStream,
    SeriesStream,
    StoriesStream,
]

class TapMarvel(Tap):
    """Marvel tap class."""
    name = "tap-marvel"
    config_jsonschema = th.PropertiesList(
        th.Property(
            "public_key",
            th.StringType,
            required=True,
            description="Your public key for the Marvel API",
            secret=True
        ),
        th.Property(
            "private_key",
            th.StringType,
            required=True,
            description="Your private key for the Marvel API",
            secret=True
        ),
        th.Property(
            "developer_mode",
            th.BooleanType,
            description="Whether to turn develop mode on, which fetches only the first page of each stream.",
            default=False
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]


if __name__ == "__main__":
    TapMarvel.cli()
