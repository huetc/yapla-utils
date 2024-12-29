import unicodedata

import pandas as pd

INPUT_FILE = "TO_BE_REPLACED_IN"
OUTPUT_FILE = "TO_BE_REPLACED_OUT"

MEMBERSHIP_TYPE_MAPPING_ID = 1000  # to be replaced, use the id provided by Yapla

input_df = pd.read_excel(INPUT_FILE)

# Name standardisation:
# - replace specific characters (e.g. accents)
# - replace "-" with white spaces
# - write in upper case
input_df["standardised_name"] = (
    input_df["name"]
    .apply(
        lambda name: "".join(
            [
                character
                for character in unicodedata.normalize("NFKD", name)
                if not unicodedata.combining(character)
            ]
        )
    )
    .replace("-", " ", regex=True)
    .str.upper()
)

# First name standardisation
# - replace missing values with ""
# - replace the "-" with whitespaces
# - replace specific characters (e.g. accents)
# - write in capital case
input_df["standardised_first_name"] = (
    input_df["first_name"]
    .fillna("")
    .apply(
        lambda first_name: "".join(
            [
                character
                for character in unicodedata.normalize("NFKD", first_name)
                if not unicodedata.combining(character)
            ]
        )
    )
    .replace("-", " ", regex=True)
    .str.capitalize()
)

# With names and first names standardised the unique ID can be retrieved
# by checking all (name, first name) combinations
# This ID is then 0-padded to be 6 characters long
input_df["id"] = (
    (input_df.groupby(["standardised_name", "standardised_first_name"]).ngroup() + 1)
    .astype("str")
    .str.pad(width=6, fillchar="0")
)

# Computing the end date by adding one year to the initial date
input_df["end_date"] = input_df["date"] + pd.DateOffset(years=1)

# There can be multiple membership types.
# Here there is only one, the same for all members.
# An ID is provided by Yapla for each membership type.
input_df["membership_type"] = MEMBERSHIP_TYPE_MAPPING_ID

# Dates must be standardised to YYYY-MM-DD format
input_df["standardised_start_date"] = input_df["date"].dt.strftime("%Y-%m-%d")
input_df["standardised_end_date"] = input_df["end_date"].dt.strftime("%Y-%m-%d")

# Deriving the membership DataFrame by keeping the latest membership record by
# member ID.
member_df = (
    input_df.sort_values(by=["id", "date"], ascending=[True, False])
    .groupby("id")
    .first()
    .reset_index("id")
)

# Standardising the phone numbers
# - replace the missing phone numbers to ""
# - cast to string
# - remove all whitespaces
# - add a missing leading 0 if the phone number is 9 character-long
member_df["standardised_phone_number"] = (
    member_df["phone_number"]
    .apply(lambda tel: tel if tel is not None else "")
    .astype("str")
    .str.replace(" ", "")
    .apply(lambda tel: "0" + tel if len(tel) == 9 and tel[0] != "0" else tel)
)

# Exporting
member_df[
    [
        "id",
        "standardised_name",
        "standardised_first_name",
        "standardised_start_date",
        "standardised_end_date",
        "membership_type",
        "standardised_phone_number",
        "email",
        "address",
        "zip_code",
    ]
].to_excel(OUTPUT_FILE, header=True, index=False)
