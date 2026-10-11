#!/bin/bash

echo "=========================================="
echo "ATTEMPTING TO DOWNLOAD REAL CENSUS DATA"
echo "=========================================="
echo ""
echo "Found two copies of census_2021_hier_v2.csv:"
echo "  1. Root folder: 15p3cy8R3jt2xrhwrTKFnSxG0-zYRmw8b"
echo "  2. Core Data:   1N-kgImCjzN7LFXpe7hrN3hOut5PQyFb5"
echo ""
echo "Both files: 212.8 MB, ~930,000 Census records"
echo ""

# Try wget with both IDs
for file_id in "15p3cy8R3jt2xrhwrTKFnSxG0-zYRmw8b" "1N-kgImCjzN7LFXpe7hrN3hOut5PQyFb5"; do
    echo "Trying file ID: $file_id"
    
    # Try direct download
    wget --no-check-certificate \
         "https://drive.google.com/uc?export=download&id=$file_id" \
         -O /workspace/data/raw/census_2021_hier_real.csv \
         2>&1 | head -20
    
    # Check if successful
    if [ -f /workspace/data/raw/census_2021_hier_real.csv ]; then
        size=$(stat -f%z /workspace/data/raw/census_2021_hier_real.csv 2>/dev/null || stat -c%s /workspace/data/raw/census_2021_hier_real.csv)
        if [ "$size" -gt 100000000 ]; then
            echo ""
            echo "✓ SUCCESS! Downloaded $size bytes"
            exit 0
        fi
    fi
    
    rm -f /workspace/data/raw/census_2021_hier_real.csv
    echo "  Failed, trying next..."
    echo ""
done

echo "❌ Both download attempts failed"
echo ""
echo "The file needs to be publicly shared or manually downloaded."
exit 1

