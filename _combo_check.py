import re, ast
from pathlib import Path
text = Path('app.py').read_text(encoding='utf-8', errors='ignore')
regions_match = re.search(r'COUNTRY_REGIONS\s*=\s*(\{.*?\})\s*\n\n\s*CROP_CATALOG', text, re.S)
cat_match = re.search(r'CROP_CATALOG\s*=\s*(\[.*?\])\s*\n\n\s*CROP_CATALOG\.extend', text, re.S)
ext_match = re.search(r'CROP_CATALOG\.extend\s*\(\s*(\[.*?\])\s*\)\s*\n\n\s*def get_translation', text, re.S)
country_regions = ast.literal_eval(regions_match.group(1))
crops = ast.literal_eval(cat_match.group(1))
crops.extend(ast.literal_eval(ext_match.group(1)))
seasons = ['kharif','rabi','summer','year_round']
categories = ['vegetables','fruits','cash_crops','grains','pulses','millets']

# Current get_crop_matches behavior errors only if no relaxed matches in same country+category
for country, regions in country_regions.items():
    bad = []
    for region in regions:
        for season in seasons:
            for category in categories:
                matches = []
                for crop in crops:
                    if country not in crop['countries']:
                        continue
                    if category != crop['category']:
                        continue
                    # relaxed eventually allows any region and any season within same country/category
                    matches.append(crop)
                if not matches:
                    bad.append((region, season, category))
    print(f'## {country}')
    if not bad:
        print('NO_ERRORS')
        continue
    for region, season, category in bad:
        print(f'{country}|{region}|{season}|{category}')
