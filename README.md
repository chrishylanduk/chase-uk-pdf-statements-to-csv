# Chase UK PDF bank statement to CSV converter

The [Chase UK retail bank](https://www.chase.co.uk/gb/en/) only allows exporting statements as PDFs. This is a very hacky Python script to convert them to CSVs for use in spreadsheet and accounting software.

This has no affiliation with Chase UK.

Last tested on statements from: Febuary 2024.

## Getting started

### Requirements

1. Python 3.13+ installed
2. Java installed, and $JAVA_HOME set
    This script uses [tabula-py](https://tabula-py.readthedocs.io/en/latest/index.html), which is a wrapper for [tabula-java](https://github.com/tabulapdf/tabula-java).

    Install Java. Then make sure that your $JAVA_HOME environment variable is set correctly ([Mac help](https://stackoverflow.com/a/66876903)).

    See the [tabula-py FAQs](https://github.com/tabulapdf/tabula-java) for troubleshooting.
3. [uv](https://docs.astral.sh/uv/) installed. [Installation instructions](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer).

### Usage

1. Install dependencies and set up a virtual environment:
```
uv sync
```

2. Copy PDF(s) to convert into the `data/pdf_inputs` directory

3. Run:
```uv run src/chase_uk_pdf_bank_statements_to_csv/run_pipeline.py```

4. Cross fingers that correctly-structured CSV(s) appear in `outputs/csv_outputs`

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md).

## Acknowledgements

This project was created using [Chris Python data science and AI Copier template](https://github.com/chrishylanduk/chris_python_data_science_ai_copier_template).
