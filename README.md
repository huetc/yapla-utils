# yapla-utils
Gather tools useful to work with the Yapla platform.

## Historical Membership Data Preparation

The aim of this project is to retrieve the list of members from historical membership records.

All members are then associated with an unique ID based on the first name + name combination (assumed to be unique).

Additional curation processing is also applied before export.

### Getting Started

With Python installed run the following command:

```bash
pip install -r requirements.txt
```

### Launching

After configuring the file locations directly in `migrate_membership_records.py` run:

```bash
python migrate_membership_records.py
```