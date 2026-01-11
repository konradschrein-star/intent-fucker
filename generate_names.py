"""
Generate 50 variations of "Swen Guenther" for testing
"""
import csv

name_variations = [
    # Original
    "Swen Guenther",
    "Swen Günther",
    
    # First name variations
    "Sven Guenther",
    "Sven Günther",
    "Svend Guenther",
    "Svend Günther",
    "Swen G.",
    "Swen G",
    "S. Guenther",
    "S. Günther",
    "S Guenther",
    "S Günther",
    
    # Last name variations
    "Swen Gunther",
    "Swen Guenter",
    "Swen Guenther",
    "Swen Günter",
    "Swen Güntherr",
    
    # Common misspellings
    "Swan Guenther",
    "Swen Gunter",
    "Swen Guenter",
    "Sven Gunther",
    "Swen Gunthar",
    
    # Capitalization variations
    "swen guenther",
    "swen günther",
    "SWEN GUENTHER",
    "SWEN GÜNTHER",
    "Swen GUENTHER",
    "SWEN Guenther",
    
    # With middle initial
    "Swen M. Guenther",
    "Swen M Guenther",
    "Swen M. Günther",
    
    # Professional titles
    "Dr. Swen Guenther",
    "Prof. Swen Guenther",
    "Mr. Swen Guenther",
    "Swen Guenther PhD",
    "Swen Guenther, Dr.",
    
    # Reversed
    "Swen Guenther wird gesucht",
    "Guenther, Swen",
    "Günther, Swen",
    "Guenther Swen",
    
    # With company/context
    "Swen Guenther Google",
    "Swen Guenther LinkedIn",
    "Swen Guenther Xing",
    "Swen Guenther Facebook",
    
    # Location based
    "Swen Guenther Berlin",
    "Swen Guenther München",
    "Swen Guenther Hamburg",
    "Swen Guenther Deutschland",
]

# Generate CSV
with open('swen_guenther_variations.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['title', 'views', 'views_per_year'])
    
    for i, variation in enumerate(name_variations, 1):
        views = 1000 + (i * 100)
        views_per_year = 500 + (i * 50)
        writer.writerow([variation, views, views_per_year])

print(f"✅ Created swen_guenther_variations.csv with {len(name_variations)} variations!")
print(f"   Test topic: 'Swen Guenther' or 'Swen Günther'")
