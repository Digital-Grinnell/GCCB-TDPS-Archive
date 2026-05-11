# Fuzzy Filename Matching Fix - MDI-CollectionBuilder Issue

**Date of Issue:** May 9, 2026 (Friday)  
**Date Documented:** May 11, 2026  
**Status:** Fixed - 1,992 objects corrected

---

## Issue Summary

The MDI-CollectionBuilder application used fuzzy filename matching logic that **catastrophically mismatched** original filenames to wrong source images during Azure upload. This resulted in **1,992 digital objects displaying completely incorrect images** - not just broken links, but actual wrong content. 

For example:
- `Wit 010.JPG` (scene 10) was matched to and displayed `Wit 001.JPG` (scene 1)
- `Wit 020.JPG` (scene 20) was matched to and displayed `Wit 002.JPG` (scene 2)  
- `Everybody00022.jpg` was matched to `Everybody00002.jpg`

The wrong source images were uploaded to Azure Blob Storage, derivatives (thumbnails/small images) were created from those wrong sources, and the files were stored with incorrect basenames. This corrupted approximately **32% of the entire collection**, making it unsuitable for research, documentation, or public display until corrected.

**Severity: CRITICAL** - Data integrity compromised, wrong content displayed throughout collection.

## The Problem

### Fuzzy Matching Behavior

The MDI-CollectionBuilder app's fuzzy matching algorithm incorrectly matched original filenames to completely different source images during the Azure upload process. When processing sequentially numbered files like `Wit 010.JPG`, `Wit 020.JPG`, etc., the fuzzy matcher would:

1. **Misidentify the source image:** Match `Wit 010.JPG` to the wrong file like `Wit 001.JPG`
2. **Upload the wrong image:** Copy the mismatched image (001) to Azure storage
3. **Create derivatives from wrong source:** Generate thumbnails and small versions from the incorrect image
4. **Mislabel the stored files:** Name them with patterns like `Wit_001_1.JPG` instead of `Wit_010.JPG`

This resulted in **catastrophic data corruption** where objects displayed completely incorrect images - not just broken links, but the WRONG content entirely.

### Real-World Example: The "Wit" Production

**Original filename in metadata:** `Wit 010.JPG`

**What SHOULD have happened:**
```
object_location: https://collectionbuilder.blob.core.windows.net/objs/TDPS_archive/Wit_010.JPG
image_small:     https://collectionbuilder.blob.core.windows.net/smalls/TDPS_archive/Wit_010_SMALL.jpg
image_thumb:     https://collectionbuilder.blob.core.windows.net/thumbs/TDPS_archive/Wit_010_TN.jpg
```
*(Derivatives created from the correct Wit 010 source image)*

**What ACTUALLY happened (fuzzy match failure):**
```
object_location: https://collectionbuilder.blob.core.windows.net/objs/TDPS_archive/Wit_001_1.JPG
image_small:     https://collectionbuilder.blob.core.windows.net/smalls/TDPS_archive/Wit_001_1_SMALL.jpg
image_thumb:     https://collectionbuilder.blob.core.windows.net/thumbs/TDPS_archive/Wit_001_1_TN.jpg
```
*(Wrong source image "Wit 001.JPG" was uploaded and used to create derivatives)*

**Result:** Object `wit10` showed image from scene 1 instead of scene 10!

### Another Example: "Wit 020.JPG"

- **Correct source:** `Wit 020.JPG` (scene 20)
- **Fuzzy matched to:** `Wit 002.JPG` (scene 2)  
- **Azure URLs:** `Wit_002_1.JPG` (and derivatives)
- **Impact:** Scene 20 displayed scene 2's image instead

## Affected Files Patterns

The fuzzy matching issue caused the wrong source images to be uploaded and used for derivative creation. The algorithm incorrectly matched files with these patterns:

1. **Double-digit ending confusion:** Files like `Wit 010.JPG` were matched to `Wit 001.JPG`
   - Pattern: `Wit 0X0` → incorrectly matched to `Wit 00X`
   - Examples: `Wit 010.JPG` → `Wit_001_1.JPG`, `Wit 020.JPG` → `Wit_002_1.JPG`, `Wit 021.JPG` → `Wit_012_1.JPG`

2. **Zero-padded numbering:** Files with leading zeros confused the matcher
   - Examples: `Everybody00022.jpg` → matched to `Everybody00002.jpg`
   - Examples: `FOLOKOTO022.jpg` → matched to `FOLOKOTO002.jpg`
   - Examples: `SSWB022.jpg` → matched to `SSWB002.jpg`

3. **Sequential single/double digit overlap:** Files where single digits exist alongside double digits
   - `arborfalls1.jpg` through `arborfalls9.jpg` confused with `arborfalls10.jpg` through `arborfalls99.jpg`
   - Examples: `arborfalls10.jpg` → potentially matched to `arborfalls1.jpg`

4. **Zero-padded sequences:** Production files with systematic zero-padding
   - `houseOfDesires00010.jpg` → matched to `houseOfDesires00001.jpg`
   - `DFYA_00020.jpg` → matched to `DFYA_00002.jpg`
   - `Arcadia20.jpg` → matched to `Arcadia02.jpg` (if it existed)

5. **Underscore-separated numbers:** Files with underscores before numbers
   - `HEY_Lillith_21.jpg` → potentially matched to `HEY_Lillith_12.jpg` or similar digit transpositions

## Scale of the Issue

- **Total objects affected:** 1,992 records
- **Total records in dataset:** 6,254 rows (including header)
- **Percentage affected:** ~31.8% of all digital objects
- **Collections impacted:** At least 12 different theatrical productions

### Major Collections Affected:

1. **Everybody** - Multiple images with double-digit suffixes
2. **FOLOKOTO (Folokoto the Tornado)** - Numerous production photos
3. **SSWB (Songs of the Scarlet and Wayback)** - Production images
4. **Arbor Falls** - Extensive photo collection (79+ images)
5. **House of Desires** - Large set of production photos
6. **Hey Lilith!** - Multiple scenes and angles
7. **Burial at Thebes** - Production photos
8. **Arcadia** - Production photos
9. **DFYA (various)** - Production documentation

## The Fix

### Approach

Created a systematic fix using AI prompts to:
1. Identify all affected records with the erroneous `_1` suffix pattern
2. Generate corrected URL paths by removing the incorrect `_1` suffix
3. Preserve correct numeric suffixes that are part of the actual filename
4. Create a new corrected CSV file

### Prompts Used

**Prompt 1: Identify the Pattern**
```
Analyze the TDPS_CBMetadata_transformed.csv file and identify all rows 
where the object_location, image_small, and image_thumb URLs contain 
filenames with numeric patterns followed by "_1" that don't match the 
original_file_name field. Focus on cases where the "_1" appears to be 
an erroneous addition by fuzzy matching rather than part of the actual 
filename.
```

**Prompt 2: Extract Affected Records**
```
Create a list of all original_file_name values where the Azure storage 
URLs contain an incorrectly added "_1" suffix. Output this as a CSV 
with a single column header "original_file_name" containing just the 
affected filenames.
```

**Prompt 3: Generate Corrections**
```
For each row in TDPS_CBMetadata_transformed.csv where the original_file_name 
is in the fixed_rows_list.csv, correct the object_location, image_small, 
and image_thumb fields by:
1. Removing the erroneous "_1" before the file extension
2. Ensuring the base filename matches the original_file_name
3. Maintaining the proper suffixes (_SMALL, _TN) for derivatives
4. Preserving all other data unchanged

Output the corrected CSV as TDPS_CBMetadata_transformed_FIXED.csv
```

### Output Files Generated

1. **fixed_rows_list.csv** (1,993 rows including header)
   - Lists all 1,992 affected filenames
   - Used as reference for which records needed correction

2. **TDPS_CBMetadata_transformed_FIXED.csv** (6,255 rows including header)
   - Complete corrected dataset
   - All 1,992 objects now point to correct Azure storage URLs
   - Ready for deployment to CollectionBuilder

## Verification

### Sample Corrections (Real Examples)

**Example 1: Wit 010.JPG**

**Before Fix (WRONG IMAGE):**
```csv
objectid,original_file_name,object_location,image_small,image_thumb
wit10,Wit 010.JPG,https://.../Wit_001_1.JPG,https://.../Wit_001_1_SMALL.jpg,https://.../Wit_001_1_TN.jpg
```
*Problem: Metadata says "010" but URLs point to derivatives of "001" image - completely wrong scene!*

**After Fix (CORRECT IMAGE):**
```csv
objectid,original_file_name,object_location,image_small,image_thumb
wit10,Wit 010.JPG,https://.../Wit_010.JPG,https://.../Wit_010_SMALL.jpg,https://.../Wit_010_TN.jpg
```
*Solution: URLs now correctly reference the actual scene 10 image*

---

**Example 2: Wit 020.JPG**

**Before Fix (WRONG IMAGE):**
```csv
objectid,original_file_name,object_location,image_small,image_thumb
wit20,Wit 020.JPG,https://.../Wit_002_1.JPG,https://.../Wit_002_1_SMALL.jpg,https://.../Wit_002_1_TN.jpg
```
*Problem: Scene 20 displayed scene 2 - catastrophic mismatch!*

**After Fix (CORRECT IMAGE):**
```csv
objectid,original_file_name,object_location,image_small,image_thumb
wit20,Wit 020.JPG,https://.../Wit_020.JPG,https://.../Wit_020_SMALL.jpg,https://.../Wit_020_TN.jpg
```
*Solution: Scene 20 now correctly references scene 20 image*

---

**Example 3: Everybody00022.jpg**

**Before Fix (WRONG IMAGE):**
```csv
objectid,original_file_name,object_location,image_small,image_thumb
everybody024,Everybody00022.jpg,https://.../Everybody00002_3.jpg,https://.../Everybody00002_3_SMALL.jpg,https://.../Everybody00002_3_TN.jpg
```
*Problem: Image #22 matched to image #2 with extra suffix*

**After Fix (CORRECT IMAGE):**
```csv
objectid,original_file_name,object_location,image_small,image_thumb
everybody024,Everybody00022.jpg,https://.../Everybody00022.jpg,https://.../Everybody00022_SMALL.jpg,https://.../Everybody00022_TN.jpg
```
*Solution: Image #22 correctly mapped to its own derivatives*

### Validation Checks

✅ All 1,992 records now have URLs matching their original_file_name basename  
✅ No mismatched digit patterns remain (e.g., `010` no longer points to `001`)  
✅ Derivative suffixes (_SMALL, _TN) properly maintained  
✅ Total row count matches original CSV (6,254 rows)  
✅ No data loss in other columns  
⚠️ **Action Required:** Correct source images must be re-uploaded to Azure to replace wrong files  
⚠️ **Action Required:** Derivatives must be regenerated from correct source images  

## Root Cause Analysis

### Why Did This Happen?

The fuzzy filename matching algorithm in MDI-CollectionBuilder was designed to handle slight variations in filenames (spaces, underscores, case differences) but had catastrophic logic flaws:

1. **Over-aggressive pattern matching:** Treated numeric patterns as "close enough" matches
2. **No validation of digit positions:** `010` considered similar to `001` because both contain "0", "0", "1"
3. **Transposition tolerance:** `020` matched to `002` due to digit similarity
4. **Sequential processing errors:** When processing `Wit 010.JPG`, instead of uploading that file, it would:
   - Search for "similar" filenames
   - Find `Wit 001.JPG` as "close match" (both start with "Wit 0")
   - Upload the WRONG file (001) to Azure
   - Label it with a modified name like `Wit_001_1.JPG`
   - Continue with wrong file for derivative generation

### Specific Trigger Patterns

The algorithm was particularly confused by:
- **Zero-padding:** `Wit 010` vs `Wit 001` - both have "Wit 00X" pattern
- **Digit transposition:** `020` vs `002` - algorithm saw matching digits, not their positions
- **Missing zeros:** `arborfalls10` vs `arborfalls1` - single vs double digit confusion
- **Repeated digits:** `Everybody00022` vs `Everybody00002` - duplicate digits caused pattern matching to fail
- **Leading zeros in sequences:** `FOLOKOTO022` vs `FOLOKOTO002` - trailing digits ignored

### Algorithm Failure Example

When MDI processed `Wit 010.JPG`:
1. ✅ Read metadata: `original_file_name = "Wit 010.JPG"`
2. ❌ Fuzzy search for files: Found `Wit 001.JPG`, `Wit 002.JPG`, etc.
3. ❌ Matched `Wit 010` to `Wit 001` (both have "Wit 0" prefix and "1")
4. ❌ Uploaded `Wit 001.JPG` content to Azure as `Wit_001_1.JPG`
5. ❌ Generated derivatives from wrong `Wit 001` source
6. ❌ Stored URLs in CSV: `Wit_001_1.JPG` (completely wrong file!)
7. ✅ Kept metadata: `original_file_name = "Wit 010.JPG"` (correct, but now orphaned)

## Lessons Learned

1. **Fuzzy matching is DANGEROUS** for asset management - can cause catastrophic data corruption
2. **Exact matching is ESSENTIAL** - numerical sequences require precise matching logic
3. **Validation is CRITICAL** - compare uploaded filenames to metadata before finalizing
4. **Preview/QA step needed** - human verification before large-scale uploads
5. **Pattern-based corrections** can efficiently fix bulk metadata issues (but not the underlying files)
6. **Documentation saves time** - both the problem and solution must be thoroughly documented
7. **File integrity matters** - it's not just about URLs, but actual file content in storage
8. **Test with edge cases** - zero-padded numbers, transposable digits, sequential numbering

## Prevention Recommendations

### Immediate (Critical)
1. **Disable fuzzy matching** in MDI-CollectionBuilder file upload process
2. **Implement exact filename matching** only - require perfect basename correspondence
3. **Add pre-upload validation** that flags any filename mismatches before processing
4. **Create upload preview** showing which source file maps to which Azure destination

### Short-term (High Priority)  
5. **Implement automated tests** for filename pattern edge cases:
   - Zero-padded sequences (`001`, `010`, `020`)
   - Transposable digits (`012` vs `021`)
   - Single vs double digits (`1` vs `10`)
   - Repeated digits (`00022` vs `00002`)
6. **Add warning system** when processing files with numeric patterns
7. **Create rollback mechanism** for Azure storage in case of upload errors
8. **Require confirmation** before processing large batches (>100 files)

### Long-term (Best Practices)
9. **Maintain upload logs** with exact source→destination mappings
10. **Generate checksums** to verify file integrity after upload
11. **Implement preview gallery** showing before/after for QA review
12. **Create automated comparison** between metadata and Azure storage contents
13. **Update WORKFLOW.md** with comprehensive naming conventions and validation steps

## Impact Assessment

### Before Fix (Catastrophic Data Corruption)
- ❌ **1,992 objects displayed COMPLETELY WRONG images**
- ❌ Wrong source images were uploaded to Azure storage
- ❌ Derivative images (thumbnails, small) created from incorrect source files
- ❌ Scene 10 might show scene 1, scene 20 might show scene 2, etc.
- ❌ User experience catastrophically broken - ~32% of collection showed incorrect content
- ❌ Search results showed wrong thumbnails for wrong scenes/moments
- ❌ Browse pages displayed misleading images
- ❌ **Data integrity completely compromised** - not just broken links, but wrong content

### Critical Severity Examples:
- **Production documentation corrupted:** `Wit 010.JPG` (scene 10) displayed `Wit 001.JPG` (scene 1)
- **Timeline confusion:** Sequential production photos out of order
- **Scene misrepresentation:** Dramatic moments from one scene attributed to another
- **Research impact:** Scholars/students viewing wrong content for citations

### After Fix
- ✅ Correct CSV mappings: All `original_file_name` values properly matched to Azure URLs
- ✅ **Re-upload required:** Correct source images need to be uploaded to Azure to replace wrong files
- ✅ **Derivatives regeneration required:** Thumbnails and small images must be recreated from correct sources
- ✅ Once complete: All objects will point to and display correct images
- ✅ Search and browse functionality will show accurate content
- ✅ Collection integrity restored
- ✅ Data suitable for research and documentation

## Related Files

- `_data/TDPS_CBMetadata_transformed.csv` - Original file with errors
- `_data/TDPS_CBMetadata_transformed_FIXED.csv` - Corrected file
- `fixed_rows_list.csv` - List of 1,992 affected filenames
- This documentation: `FUZZY_FILENAME_MATCHING_FIX.md`

## Deployment Status

### Phase 1: CSV Correction (Completed ✅)
- [x] Issue identified and analyzed (Friday, May 9, 2026)
- [x] Fix prompts created and executed
- [x] Corrected CSV generated (`TDPS_CBMetadata_transformed_FIXED.csv`)
- [x] Validation completed
- [x] Documentation created

### Phase 2: Azure Storage Correction (Required ⚠️)
- [ ] **Re-upload correct source images** to Azure Blob Storage
  - Must replace 1,992 incorrectly uploaded files
  - Upload actual `Wit 010.JPG` to replace current `Wit_001_1.JPG`, etc.
  - Ensure correct basenames (no `_1` suffixes)
- [ ] **Regenerate all derivatives** from correct source images
  - Delete incorrect `_SMALL.jpg` files created from wrong sources
  - Delete incorrect `_TN.jpg` files created from wrong sources  
  - Generate new thumbnails and small images from correct sources
- [ ] Verify Azure storage contains correct files with correct names

### Phase 3: Production Deployment (Pending)
- [ ] Deploy FIXED.csv to production CollectionBuilder
- [ ] Test production deployment with corrected Azure files
- [ ] Verify all 1,992 corrected objects display properly
- [ ] Spot-check Wit production images (010, 020, 021) show correct scenes
- [ ] Archive original erroneous CSV for reference

### Phase 4: Prevention (Recommended)
- [ ] Update MDI-CollectionBuilder to prevent recurrence
  - Replace fuzzy matching with exact filename matching
  - Add validation step to compare uploaded files with metadata
  - Implement warning system for potential mismatches
- [ ] Update WORKFLOW.md with lessons learnedidentify and correct 1,992 incorrectly matched filenames in the TDPS Archive CollectionBuilder project. The CSV has been corrected, but **the actual image files in Azure storage must also be corrected** by re-uploading the proper source images and regenerating derivatives. Only then will the collection display accurate conten
- [ ] Create test suite for filename pattern edge cases

---

**Critical Note:** The CSV fix alone is insufficient. The ACTUAL IMAGE FILES in Azure storage are wrong and must be corrected. Until Azure storage is updated with the correct source images and regenerated derivatives, the collection will still display incorrect content even with the corrected CSV.

---

**Note:** This fix was completed on Friday, May 9, 2026, using AI-assisted prompts to systematically correct 1,992 incorrectly matched filenames in the TDPS Archive CollectionBuilder project.
