# Smoke test plugin design doc

## Requirements
- Smoke test clusters
- `victoria smoke test uksprod1 uksprod2 useprod1 useprod2`
- Supports nonprod envs like stage, qa etc

## Process
- `test` subcommand is run
- Get index of attachment library files
- Read templates and generate emails based on specs
- Send each email through every cluster specified with unique from address based on spec (to identify Tx ID)
- Wait a little bit
- From log analytics, get transaction IDs for each email sent
- Trace these transaction IDs through the system and report any fails
- If any fails are detected, save failed templated specs to appdirs under directory with exec time and report to stdout

## Config
- Will need tenant IDs for clusters
- Location of templates
- Location of attachment library
- Stuff necessary for log analytics integration

## Templates
- YAML files which are preprocessed by jinja2
```yaml
headers: <headers obj as in sremail>
body: |-
    <body>
attach:
    <attachment-spec>
```
- Templates can be previewed with `template` subcommand:
  `victoria smoke template template.yaml [-o OUTPUT-FILE]`
- Templates can be rendered into MIME with `render` subcommand:
  `victoria smoke render template.yaml [-o OUTPUT-FILE]`

## Replay spec
- Templated specs can be replayed using `replay` subcommand:
  `victoria smoke replay failed-spec.yaml`
- This is to support checking failed emails again

## Body templating
- Can be raw string
- Function to generate lorem ipsum
- Function to generate random ASCII
- Function to generate random UTF-8
- Use [Faker](https://faker.readthedocs.io/en/master/)

## Attachment templating
- Filter by filename
- Filter by filetype
- Filter by directory
- Filter by size
- Filter by count
- Random choice