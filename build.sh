#!/bin/bash
# Build script for Chrome Web Store submission
# Creates a clean ZIP file with only the extension files
# Works on both Linux/Mac (zip) and Windows (PowerShell)

set -e

EXTENSION_NAME="hintcode"
VERSION=$(grep '"version"' manifest.json | head -1 | sed 's/.*: "\(.*\)".*/\1/')
ZIP_NAME="${EXTENSION_NAME}-v${VERSION}.zip"

echo "Building ${ZIP_NAME}..."

# Remove old zip if exists
rm -f "$ZIP_NAME"

if command -v zip &> /dev/null; then
  zip -r "$ZIP_NAME" \
    manifest.json \
    background/ \
    content-scripts/ \
    icons/ \
    lib/ \
    options/ \
    popup/ \
    sidepanel/ \
    styles/ \
    -x "*.DS_Store" "*__MACOSX*"
else
  # Windows fallback using PowerShell
  powershell -Command "
    \$files = @(
      'manifest.json',
      'background',
      'content-scripts',
      'icons',
      'lib',
      'options',
      'popup',
      'sidepanel',
      'styles'
    )
    if (Test-Path '$ZIP_NAME') { Remove-Item '$ZIP_NAME' }
    Compress-Archive -Path \$files -DestinationPath '$ZIP_NAME'
  "
fi

echo ""
echo "Created: $ZIP_NAME"
ls -lh "$ZIP_NAME" | awk '{print "Size:", $5}'
echo ""
echo "Upload this file to: https://chrome.google.com/webstore/devconsole"
