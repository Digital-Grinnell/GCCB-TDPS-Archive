# Deleting Objects from Azure Blob Storage

`utilities/delete_azure_objects.py` deletes all files in Azure Blob Storage that
belong to a list of `dg_xxx` object identifiers (e.g. `dg_1781104558`).

For each identifier, it searches the `objs`, `smalls`, and `thumbs` containers
(the standard CollectionBuilder image/derivative containers) for any blob
whose filename starts with that identifier, such as:

- `objs/TDPS-Archive/dg_1781104558.jpg`
- `smalls/TDPS-Archive/dg_1781104558_SMALL.jpg`
- `thumbs/TDPS-Archive/dg_1781104558_TN.jpg`
- `objs/TDPS-Archive/dg_1781104558_2.jpg` (compound-object pages)

Matching requires the identifier to be followed by end-of-name, `.`, or `_`,
so `dg_123` will never accidentally match `dg_1234...`.

## Setup

Install the Azure SDK package (one time):

```bash
pip3 install azure-storage-blob
```

Set your storage account connection string (find it in the Azure Portal under
the Storage Account → **Access keys**):

```bash
export AZURE_STORAGE_CONNECTION_STRING="<your connection string>"
```

## Preparing the identifier list

Create a plain text file with one `dg_xxx` identifier per line:

```
dg_1781104558
dg_1742490256
dg_1745949037
```

A CSV file (e.g. an exported metadata file with an `objectid` column) also
works — the script scans every line for `dg_\d+` tokens, so you can point it
directly at a CSV rather than building a separate list.

## Usage

Always run a dry-run first to review what will be deleted:

```bash
python3 utilities/delete_azure_objects.py --ids-file ids_to_delete.txt
```

This prints a summary and writes a CSV report to
`logfiles/azure_delete_report_<timestamp>.csv` listing every matched blob and
its status (`PENDING` in dry-run mode), plus any identifiers for which no
blobs were found.

Once you've reviewed the report, re-run with `--execute` to actually delete
the matched blobs:

```bash
python3 utilities/delete_azure_objects.py --ids-file ids_to_delete.txt --execute
```

## Options

| Flag | Description |
| --- | --- |
| `--ids-file` (required) | Path to a text or CSV file listing `dg_xxx` identifiers |
| `--containers` | Comma-separated list of containers to search (default: `objs,smalls,thumbs`) |
| `--connection-string` | Azure Storage connection string (defaults to `AZURE_STORAGE_CONNECTION_STRING` env var) |
| `--execute` | Actually delete matched blobs (omit for a dry-run) |
| `--report` | Path for the CSV report (default: `logfiles/azure_delete_report_<timestamp>.csv`) |

## Safety notes

- Deletion from Blob Storage is **irreversible** unless soft-delete/versioning
  is enabled on the storage account. Always review the dry-run report before
  adding `--execute`.
- Never commit your connection string to the repository — pass it via the
  `AZURE_STORAGE_CONNECTION_STRING` environment variable.
