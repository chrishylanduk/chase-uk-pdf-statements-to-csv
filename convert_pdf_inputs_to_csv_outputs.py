import tabula
import pandas as pd
import glob
import os


def find_pdf_files(directory: str):
    pdf_files = glob.glob(directory + "/*.pdf")
    return pdf_files


def chase_uk_pdf_statement_to_df(pdf_path: str) -> pd.DataFrame:
    statement_df = tabula.read_pdf(
        pdf_path, pages="all", multiple_tables=False, guess=False, stream=True
    )[0]

    # Automatic splitting into columns can be inconsistent page-by-page, so
    # combine them into one column and we'll manually parse
    statement_df["Combined"] = statement_df.apply(
        lambda x: " ".join(x.fillna("").astype(str)), axis=1
    )
    statement_df = statement_df[["Combined"]]

    # Chop off all lines above and including "Opening balance", and those below 
    # and including "Closing balance"
    last_opening_balance_location = (
        statement_df.iloc[::-1]["Combined"]
        .fillna("")
        .astype(str)
        .str.contains("Opening balance")
    ).idxmax()
    last_closing_balance_location = (
        statement_df.iloc[::-1]["Combined"]
        .fillna("")
        .astype(str)
        .str.contains("Closing balance")
    ).idxmax()
    statement_df = statement_df.loc[
        last_opening_balance_location + 1 : last_closing_balance_location - 1
    ]

    # Drop column heading rows, and the rows immediately beneath them (date ranges)
    column_headings_rows_mask = statement_df["Combined"].isin(
        [
            "Date Transaction details Amount Balance",
            "Date Transaction details Amount Balance ",
        ]
    )
    date_ranges_mask = column_headings_rows_mask.shift(-1, fill_value=False)
    statement_df = statement_df[~(column_headings_rows_mask + date_ranges_mask)]

    # Drop other non-transaction rows
    terms_to_exclude_rows_that_contain = ["Account statement", "Sort code", "Page"]
    main_mask = (
        statement_df["Combined"]
        .fillna("")
        .astype(str)
        .str.contains("|".join(terms_to_exclude_rows_that_contain))
    )
    statement_df = statement_df[~main_mask]

    statement_df = statement_df.reset_index(drop=True)

    # Bring up the type field (light grey) under some transaction lines into the
    # row above, then delete their original row
    type_field_possible_starts = [
        "Purchase",
        "Interest",
        "Refund",
        "Payment",
        "Transfer",
    ]
    for i in range(0, len(statement_df)):
        row_value = statement_df.at[i, "Combined"]
        if any(
            row_value.startswith(type_start)
            for type_start in type_field_possible_starts
        ):
            statement_df.at[i - 1, "Type"] = row_value
            statement_df.at[i, "Delete"] = True

    statement_df = statement_df[statement_df["Delete"] != True]
    statement_df = statement_df.drop("Delete", axis=1)

    # Split out the transaction date, the first three words of each line
    split_date = statement_df["Combined"].str.split(" ", n=3, expand=True)
    statement_df["Combined"] = split_date[3]
    statement_df["Date"] = split_date[0] + " " + split_date[1] + " " + split_date[2]

    # Split off transaction details from amount and balance, by looking
    # for "-£" or "+£"
    transaction_vs_money_split = statement_df["Combined"].str.extract(
        r"^(.*?)(\+£.*|-£.*)$"
    )
    # Split off amount from balance, by splitting on the first space"
    amount_vs_balance_split = transaction_vs_money_split[1].str.split(
        " ", n=1, expand=True
    )

    statement_df["Transaction details"] = transaction_vs_money_split[0]
    statement_df["Amount"] = amount_vs_balance_split[0]
    statement_df["Balance"] = amount_vs_balance_split[1]

    # We should have extracted everything, drop Combined
    statement_df = statement_df.drop("Combined", axis=1)

    # Type can contain currency conversion details, if so split these out
    split_type = statement_df["Type"].str.split("|", n=2, expand=True)
    if len(split_type.columns) == 3:
        statement_df[["Type", "Currency value", "Currency conversion"]] = split_type

    # Strip whitespace at start/end of strings
    statement_df = statement_df.map(lambda x: x.strip() if isinstance(x, str) else x)

    return statement_df


input_pdf_files = find_pdf_files("pdf_inputs")

for input_pdf_file in input_pdf_files:
    input_pdf_file_name = os.path.splitext(os.path.basename(input_pdf_file))[0]

    statement_df = chase_uk_pdf_statement_to_df(input_pdf_file)
    statement_df.to_csv(
        f"csv_outputs/{input_pdf_file_name}.csv", encoding="utf-8-sig", index=False
    )
