# Parent-Child Image Updates

## Date: October 30, 2025

## Summary

Updated parent records in `TDPS_CBMetadata_transformed.csv` to include `image_small` and `image_thumb` values copied from their first child record. This enables parent compound objects to display representative images on the site.

## Methodology

For each parent record (compound objects with no `parentid`):
1. Identified all child records (rows with matching `parentid`)
2. Sorted children by `objectid` (alphabetical)
3. Copied `image_small` and `image_thumb` from the first child to the parent

## Changes Made

### 1. everybody_col (Everybody)
- **Parent Title:** Everybody
- **First Child:** everybody001 (Poster)
- **image_small:** `https://collectionbuilder.blob.core.windows.net/smalls/TDPS_archive/everybody_posterdraft_SMALL.jpg`
- **image_thumb:** `https://collectionbuilder.blob.core.windows.net/thumbs/TDPS_archive/everybody_posterdraft_TN.jpg`

### 2. folokoto_col (Folokoto the Tornado)
- **Parent Title:** Folokoto the Tornado
- **First Child:** folokoto001 (1)
- **image_small:** `https://collectionbuilder.blob.core.windows.net/smalls/TDPS_archive/FOLOKOTO001_SMALL.jpg`
- **image_thumb:** `https://collectionbuilder.blob.core.windows.net/thumbs/TDPS_archive/FOLOKOTO001_TN.jpg`

### 3. sswb_col (Songs of the Scarlet and Wayback)
- **Parent Title:** Songs of the Scarlet and Wayback
- **First Child:** SSWB001 (Poster)
- **image_small:** `https://collectionbuilder.blob.core.windows.net/smalls/TDPS_archive/SSWB_Poster_SMALL.jpg`
- **image_thumb:** `https://collectionbuilder.blob.core.windows.net/thumbs/TDPS_archive/SSWB_Poster_TN.jpg`

## Parents Not Updated

The following parent records were not updated because they have no children with images:

- **pity_col** (Pity) - No children in dataset
- **burn_col** (The Burn) - No children in dataset
- **watersedge_col** (At Water's Edge/Al Filo del Agua) - No children in dataset
- **magicacts_col** (A Memoir of Magic Acts) - No children in dataset

## Impact

### Benefits:
- ✅ Parent compound objects now display representative images on browse pages
- ✅ Homepage and search results show thumbnails for compound objects
- ✅ Improved visual navigation through the collection
- ✅ Consistent with CollectionBuilder best practices for compound objects

### Technical Notes:
- The "first child" is determined by alphabetical sorting of `objectid`
- For productions with multiple children, this typically selects the poster (e.g., `everybody001` for Everybody)
- For image-only productions, it selects the first image (e.g., `folokoto001` for Folokoto)
- Empty parent records remain unchanged
- This change does not affect the display of child items themselves

## Related Files Modified:
- `_data/TDPS_CBMetadata_transformed.csv` - Updated 3 parent records

## Testing Checklist:
- [ ] Verify parent records display images on browse page
- [ ] Check homepage carousel shows compound object images
- [ ] Confirm search results display parent thumbnails correctly
- [ ] Test that clicking parent images navigates to compound object pages
- [ ] Verify child items are still accessible and display correctly
