#!/usr/bin/env python3
"""
Transform TDPS_CBMetadata.csv to match the verified CSV headings structure.
Maps existing fields and appends unique TDPS fields at the end.
"""

import csv

# Define the verified headings structure
VERIFIED_HEADINGS = [
    'objectid', 'originating_system_id', 'original_file_name', 'short_filename',
    'sort_index', 'parentid', 'admin_notes', 'title', 'interviewer', 'interviewee',
    'date', 'description', 'subject', 'people', 'location', 'latitude', 'longitude',
    'source', 'identifier', 'type', 'format', 'language', 'rights', 'rightsstatement',
    'display_template', 'WORKSPACE1', 'WORKSPACE2', 'WORKSPACE3', 'object_location',
    'image_small', 'image_thumb', 'image_alt_text', 'object_transcript'
]

# Field mappings from TDPS to verified structure
FIELD_MAPPING = {
    'objectid': 'objectid',
    'parentid': 'parentid',
    'filename': 'original_file_name',
    'title': 'title',
    'date': 'date',
    'description': 'description',
    'subject': 'subject',
    'location': 'location',
    'latitude': 'latitude',
    'longitude': 'longitude',
    'source': 'source',
    'identifier': 'identifier',
    'type': 'type',
    'format': 'format',
    'language': 'language',
    'rights': 'rights',
    'rightsstatement': 'rightsstatement',
    'display_template': 'display_template',
    'object_location': 'object_location',
    'image_small': 'image_small',
    'image_thumb': 'image_thumb',
    'image_alt_text': 'image_alt_text',
    'object_transcript': 'object_transcript'
}

# Read TDPS file and get its headers
with open('_data/TDPS_CBMetadata.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    tdps_headers = reader.fieldnames
    tdps_rows = list(reader)

# Find unique TDPS fields not in verified structure
unique_tdps_fields = []
for header in tdps_headers:
    if header not in FIELD_MAPPING:
        unique_tdps_fields.append(header)

# Create final header list: verified structure + unique TDPS fields
final_headers = VERIFIED_HEADINGS + unique_tdps_fields

print(f"Verified headings: {len(VERIFIED_HEADINGS)}")
print(f"TDPS headings: {len(tdps_headers)}")
print(f"Unique TDPS fields to append: {unique_tdps_fields}")
print(f"Final header count: {len(final_headers)}")

# Write new CSV with transformed data
with open('_data/TDPS_CBMetadata_transformed.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=final_headers)
    writer.writeheader()
    
    for row in tdps_rows:
        new_row = {}
        
        # Map verified fields from TDPS data
        for tdps_field, verified_field in FIELD_MAPPING.items():
            if tdps_field in row:
                new_row[verified_field] = row[tdps_field]
        
        # Add unique TDPS fields
        for field in unique_tdps_fields:
            if field in row:
                new_row[field] = row[field]
        
        writer.writerow(new_row)

print(f"\nTransformed {len(tdps_rows)} rows")
print(f"Output written to: _data/TDPS_CBMetadata_transformed.csv")
