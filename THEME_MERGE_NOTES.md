# Theme.yml Merge Summary

## Source Files
- **tdps_theme.yml** - TDPS-specific customizations
- **GCCB_theme.yml** - Full GCCB template with OHD features

## Merged Result: theme.yml

### Key Decisions Made:

#### FROM TDPS (Preserved):
✅ **featured-image**: `assets/img/featured_image.jpg` (local TDPS image)
✅ **home-title-y-padding**: `10em` (larger padding for TDPS)
✅ **subjects-fields**: Complete TDPS production fields (17 fields including venue, playwright/composer, director, etc.)
✅ **metadata-export-fields**: TDPS-specific fields added (venue, playwright/composer, director)
✅ **metadata-facets-fields**: TDPS fields (subject, venue, director, format)

#### FROM GCCB (Added):
✅ **home-page-visualization**: Added (set to `false` since TDPS doesn't use it)
✅ **Browse PAGE section**: 
   - `advanced-search: true`
   - `faceted-search: true`
   - `default-sort-field: date`
✅ **auto-center-map**: `true` (better map functionality)
✅ **OHD OPTIONS**: Full Oral History as Data section (for future use)
✅ **base-layout**: `CB` (CollectionBuilder layout)
✅ **carousel-child-objects**: Added option
✅ **Enhanced icon comments**: Including panorama, markdown icons

#### Merged/Adjusted:
- **MAP PAGE**: Combined auto-center with manual coordinates
- **DATA section**: Merged export fields to include both GCCB and TDPS metadata
- **TIMELINE**: Used GCCB's clearer comments
- **Comments**: Kept more detailed GCCB comments for clarity

### What This Gives You:

1. **Better Search**: Advanced and faceted search from GCCB
2. **TDPS Customization**: All theatre/performance production fields
3. **Future-Ready**: OHD features available if needed
4. **Better UX**: Auto-centering map, enhanced browse options
5. **All Options**: Complete set of CollectionBuilder features

### Files Status:
- ✅ **theme.yml** - New merged file (ACTIVE)
- 📁 **tdps_theme.yml** - Original TDPS (can archive)
- 📁 **GCCB_theme.yml** - Original GCCB template (can archive)

### Testing Checklist:
- [ ] Site builds without errors
- [ ] Browse page shows advanced/faceted search
- [ ] Subjects page shows all TDPS production fields
- [ ] Map auto-centers correctly
- [ ] Timeline displays properly
- [ ] Data exports include TDPS fields
