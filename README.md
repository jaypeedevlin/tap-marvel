# tap-marvel

`tap-marvel` is a Singer tap for the [Marvel Developer API](https://developer.marvel.com/).

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

## Installation
Install from GitHub:

```bash
pipx install git+https://github.com/japeedevlin/tap-marvel.git@main
```

-->

## Configuration

### Accepted Config Options

- `public_key`
- `private_key`

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

## Usage

You can easily run `tap-marvel` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-marvel --version
tap-marvel --help
tap-marvel --config CONFIG --discover > ./catalog.json
```

## Developer Resources

Follow these instructions to contribute to this project.

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tap_marvel/tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-marvel` CLI interface directly using `poetry run`:

```bash
poetry run tap-marvel --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-marvel
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-marvel --version
# OR run a test `elt` pipeline:
meltano elt tap-marvel target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
