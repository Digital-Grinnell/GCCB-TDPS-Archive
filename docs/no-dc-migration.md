# No-DC Field Migration

## Summary

This repository migrated metadata field references from `dc_*` names to unprefixed names.

Examples:

- `dc_title` -> `title`
- `dc_date` -> `date`
- `dc_description` -> `description`
- `dc_subject` -> `subject`
- `dc_source` -> `source`
- `dc_identifier` -> `identifier`
- `dc_format` -> `format`
- `dc_rights` -> `rights`

## What Was Updated

The no-dc update touched active project files in these areas:

- Metadata CSV headers and browse/search/table/transcript configs in `_data/`
- Liquid templates and item includes in `_includes/` and `_layouts/`
- Data generation templates in `assets/data/` and `utilities/oai.xml`
- Ruby helper/rake logic in `_plugins/` and `rakelib/`
- Documentation references in `docs/`

A follow-up fix also adjusted browse date sorting so records missing `date` are sorted to the end when sorting by Date (latest first for valid dates).

## Scope Guardrails

To avoid rewriting historical snapshots, files with backup-style names were intentionally not mass-updated.

Examples of excluded patterns:

- `*backup*`
- hidden backup snapshots such as `_data/.TDPS_DART_Core.backup_*`

## Verification

- Searched active tracked files for remaining `dc_` references and resolved matches.
- Rebuilt site with `bundle exec jekyll build` after migration.

## Notes

If additional archival backup files must also be normalized, run a separate controlled pass so provenance files can be reviewed independently.
