# Chase UK PDF bank statement to CSV converter

The [Chase UK retail bank](https://www.chase.co.uk/gb/en/) only allows exporting statements as PDFs. This is a very hacky Python script to convert them to CSVs for use in spreadsheet and accounting software.

This has no affiliation with Chase UK.

Last tested on statements from: Febuary 2024.

## Usage

1. Install Java, and check $JAVA_HOME is set

This script uses [tabula-py](https://tabula-py.readthedocs.io/en/latest/index.html), which is a wrapper for [tabula-java](https://github.com/tabulapdf/tabula-java).

Install Java. Then make sure that your $JAVA_HOME environment variable is set correctly ([Mac help](https://stackoverflow.com/a/66876903)).

See the [tabula-py FAQs](https://github.com/tabulapdf/tabula-java) for troubleshooting.

2. Install dependencies:
```
pip install -r requirements.txt
```
3. Copy PDF(s) to convert into the `pdf_inputs` directory

4. Run `python convert_pdf_inputs_to_csv_outputs.py`

5. Cross fingers that correctly-structured CSV(s) appear in `csv_outputs`