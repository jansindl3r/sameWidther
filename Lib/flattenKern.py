"""
Flatten a font's GPOS kerning.
"""
from fontTools.ttLib import TTFont


def _kerning_lookup_indexes(ttfont):
    """Return the lookup ids for the kern feature"""
    for feat in ttfont['GPOS'].table.FeatureList.FeatureRecord:
        if feat.FeatureTag == 'kern':
            return feat.Feature.LookupListIndex
    return None


def _flatten_format1_subtable(table):
    """Flatten pair on pair kerning"""
    flattened_table = []
    first_glyphs = {idx: g for idx, g in enumerate(table.Coverage.glyphs)}

    for idx, pairset in enumerate(table.PairSet):
        first_glyph = first_glyphs[idx]

        for record in pairset.PairValueRecord:
            flattened_table.append((first_glyph, record.SecondGlyph, record.Value1.XAdvance))
    return flattened_table


def _flatten_format2_subtable(table):
    """Flatten class on class kerning"""
    flattened_table = []
    classes1 = _kern_class(table.ClassDef1.classDefs)
    classes2 = _kern_class(table.ClassDef2.classDefs)

    for idx1, class1 in enumerate(table.Class1Record):
        for idx2, class2 in enumerate(class1.Class2Record):

            if idx1 not in classes1:
                continue
            if idx2 not in classes2:
                continue

            if class2.Value1.XAdvance != 0:
                for glyph1 in classes1[idx1]:
                    for glyph2 in classes2[idx2]:
                        flattened_table.append((glyph1, glyph2, class2.Value1.XAdvance))
    return flattened_table


def _kern_class(class_definition):
    """Transpose a ttx classDef

    {glyph_name: idx, glyph_name: idx} --> {idx: [glyph_name, glyph_name]}"""
    classes = {}
    for glyph,idx in class_definition.items():
        if idx not in classes:
            classes[idx] = []
        classes[idx].append(glyph)
    return classes


def flatten_gpos_kerning(ttfont):

    if not 'GPOS' in ttfont:
        raise Exception("Font doesn's have GPOS table")

    kerning_lookup_indexes = _kerning_lookup_indexes(ttfont)
    if not kerning_lookup_indexes:
        return
        # raise Exception("Font doesn't have a GPOS kern feature")

    kern_table = []
    for lookup_idx in kerning_lookup_indexes:
        lookup = ttfont['GPOS'].table.LookupList.Lookup[lookup_idx]

        for sub_table in lookup.SubTable:
            if sub_table.Format == 1:
                kern_table += _flatten_format1_subtable(sub_table)
            if sub_table.Format == 2:
                kern_table += _flatten_format2_subtable(sub_table)
    return kern_table


if __name__ == '__main__':
    font = TTFont('/Users/marc/Documents/googlefonts/manual_font_cleaning/anaheimFont/fonts/ttf/Anaheim-Regular.ttf')
    kerning = flatten_gpos_kerning(font)
