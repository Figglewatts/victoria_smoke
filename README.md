# victoria_smoke

**Note:** This repository is quite old, and was mainly used as an experiment into
generating mail and fuzzing MIME. A lot of this code now exists in other
Glasswall SRE projects in a more advanced form.

This is the smoke testing plugin for Victoria.

## User guide

### Prerequisites
- Python
- Pip
- You've set up the [SRE package feed](https://dev.azure.com/glasswall/Glasswall%20Cloud/_wiki/wikis/Service%20Reliability%20Engineering%20Wiki/393/Using-SRE-Python-Packages)

### Installation
```terminal
pip install victoria_smoke --extra-index-url $SRE_PACKAGE_FEED
```

## Development guide

### Prerequisites
- Python
- Pipenv

### Quick start
1. Clone the repo.
2. Run `pipenv install`.
3. You're good to go.