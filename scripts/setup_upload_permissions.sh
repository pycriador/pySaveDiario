#!/bin/bash

###############################################################################
# Setup Secure Upload Permissions
#
# This script configures correct permissions for the uploads directory
# Run with appropriate privileges (sudo if needed)
###############################################################################

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Setup Upload Permissions ===${NC}\n"

# Get the project root directory (parent of scripts/)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UPLOAD_DIR="${PROJECT_ROOT}/app/static/uploads"

echo "Project root: ${PROJECT_ROOT}"
echo "Upload directory: ${UPLOAD_DIR}"
echo ""

# Check if directory exists
if [ ! -d "$UPLOAD_DIR" ]; then
    echo -e "${YELLOW}Upload directory does not exist. Creating...${NC}"
    mkdir -p "${UPLOAD_DIR}/products"
    touch "${UPLOAD_DIR}/products/.gitkeep"
fi

# Get web server user (auto-detect)
if id "www-data" &>/dev/null; then
    WEB_USER="www-data"
elif id "nginx" &>/dev/null; then
    WEB_USER="nginx"
elif id "apache" &>/dev/null; then
    WEB_USER="apache"
else
    echo -e "${YELLOW}Could not detect web server user. Using current user.${NC}"
    WEB_USER=$(whoami)
fi

echo "Web server user: ${WEB_USER}"
echo ""

# Confirm before proceeding
read -p "Continue with permission setup? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${RED}Aborted.${NC}"
    exit 1
fi

echo -e "${GREEN}Setting up permissions...${NC}"

# Set ownership
echo "1. Setting ownership to ${WEB_USER}..."
if [ "$WEB_USER" != "$(whoami)" ]; then
    sudo chown -R "${WEB_USER}:${WEB_USER}" "$UPLOAD_DIR"
else
    chown -R "${WEB_USER}:${WEB_USER}" "$UPLOAD_DIR"
fi

# Set directory permissions: 755 (rwxr-xr-x)
echo "2. Setting directory permissions to 755..."
find "$UPLOAD_DIR" -type d -exec chmod 755 {} \;

# Set file permissions: 644 (rw-r--r--)
echo "3. Setting file permissions to 644..."
find "$UPLOAD_DIR" -type f -exec chmod 644 {} \;

# Remove execute permission from all files, but keep for directories
echo "4. Removing execute permission from files..."
chmod -R -x+X "$UPLOAD_DIR"

# Verify permissions
echo ""
echo -e "${GREEN}=== Verification ===${NC}"
echo ""
echo "Upload directory permissions:"
ls -lah "$UPLOAD_DIR"

echo ""
echo "Products directory permissions:"
ls -lah "${UPLOAD_DIR}/products" 2>/dev/null || echo "No files yet"

echo ""
echo -e "${GREEN}✓ Permissions setup complete!${NC}"
echo ""
echo -e "${YELLOW}Important:${NC}"
echo "1. Ensure your Flask app runs as user: ${WEB_USER}"
echo "2. Verify web server configuration blocks script execution in uploads/"
echo "3. Test with: python scripts/test_upload_security.py"

