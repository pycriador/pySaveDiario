#!/usr/bin/env python3
"""
Security Test Script for Image Upload

This script tests the security measures implemented in the upload system.
Run from the project root: python scripts/test_upload_security.py
"""

import io
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.utils.upload import (
    allowed_file,
    validate_image_content,
    validate_image_with_pil,
    generate_secure_filename,
    ALLOWED_EXTENSIONS,
    MAX_FILE_SIZE
)


class Colors:
    """ANSI color codes"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'


def print_header(text):
    """Print colored header"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}{text:^60}{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}\n")


def print_test(name, passed, message=""):
    """Print test result"""
    status = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if passed else f"{Colors.RED}✗ FAIL{Colors.RESET}"
    print(f"  {status} - {name}")
    if message:
        print(f"         {message}")


def test_extension_validation():
    """Test 1: Extension Validation"""
    print_header("TEST 1: Extension Validation")
    
    # Valid extensions
    valid_files = ['image.jpg', 'photo.png', 'pic.gif', 'img.jpeg', 'photo.webp']
    for filename in valid_files:
        result = allowed_file(filename)
        print_test(f"Valid: {filename}", result)
    
    # Invalid extensions
    invalid_files = ['malware.exe', 'script.php', 'hack.sh', 'virus.bat', 'code.py']
    for filename in invalid_files:
        result = not allowed_file(filename)
        print_test(f"Invalid: {filename}", result, "Should be blocked")
    
    # Edge cases
    print_test("No extension", not allowed_file('filename'), "Should be blocked")
    print_test("Multiple dots", allowed_file('image.backup.jpg'), "Should be allowed")
    print_test("Uppercase", allowed_file('IMAGE.JPG'), "Should be allowed (case insensitive)")


def test_secure_filename_generation():
    """Test 2: Secure Filename Generation"""
    print_header("TEST 2: Secure Filename Generation")
    
    # Test path traversal prevention
    dangerous_names = [
        '../../etc/passwd.jpg',
        '../../../root/.ssh/id_rsa.png',
        '..\\..\\windows\\system32\\config\\sam.jpg',
        '<script>alert(1)</script>.jpg',
    ]
    
    for dangerous in dangerous_names:
        safe = generate_secure_filename(dangerous)
        # Check that it doesn't contain path separators
        has_no_traversal = '..' not in safe and '/' not in safe and '\\' not in safe
        # Check that it's a valid hex token
        is_random = len(safe.split('.')[0]) == 32  # 16 bytes = 32 hex chars
        passed = has_no_traversal and is_random
        print_test(f"Sanitize: {dangerous[:30]}...", passed, f"Generated: {safe}")
    
    # Test uniqueness
    names = [generate_secure_filename('test.jpg') for _ in range(10)]
    all_unique = len(names) == len(set(names))
    print_test("Filename uniqueness", all_unique, f"10 files generated, all unique: {all_unique}")


def test_file_size_limit():
    """Test 3: File Size Limit"""
    print_header("TEST 3: File Size Limit")
    
    # Test max file size setting
    max_mb = MAX_FILE_SIZE / (1024 * 1024)
    print_test(f"Max file size configured", True, f"{max_mb:.1f} MB")
    
    # Show size limits
    print(f"\n  Configuration:")
    print(f"    MAX_FILE_SIZE = {MAX_FILE_SIZE:,} bytes")
    print(f"    MAX_FILE_SIZE = {max_mb:.1f} MB")
    print(f"\n  Note: Size validation is performed in save_image() function")


def test_allowed_extensions():
    """Test 4: Allowed Extensions"""
    print_header("TEST 4: Allowed Extensions")
    
    print(f"  Allowed extensions: {', '.join(sorted(ALLOWED_EXTENSIONS))}")
    print(f"  Total: {len(ALLOWED_EXTENSIONS)} image formats")
    
    # Verify common image formats are included
    required = {'jpg', 'jpeg', 'png', 'gif'}
    has_required = required.issubset(ALLOWED_EXTENSIONS)
    print_test("Has common formats (jpg, jpeg, png, gif)", has_required)
    
    # Verify dangerous formats are excluded
    dangerous = {'exe', 'php', 'sh', 'py', 'bat', 'cmd', 'js'}
    has_no_dangerous = len(dangerous.intersection(ALLOWED_EXTENSIONS)) == 0
    print_test("No dangerous extensions", has_no_dangerous)


def test_directory_structure():
    """Test 5: Directory Structure"""
    print_header("TEST 5: Directory Structure")
    
    base_dir = Path('app/static/uploads')
    products_dir = base_dir / 'products'
    
    print_test("Base uploads directory exists", base_dir.exists())
    print_test("Products directory exists", products_dir.exists())
    
    # Check .gitignore
    gitignore = base_dir / '.gitignore'
    gitignore_exists = gitignore.exists()
    print_test(".gitignore exists", gitignore_exists)
    
    if gitignore_exists:
        content = gitignore.read_text()
        ignores_all = '*' in content
        print_test(".gitignore blocks uploads", ignores_all)
    
    # Check .gitkeep
    gitkeep = products_dir / '.gitkeep'
    print_test(".gitkeep in products/ exists", gitkeep.exists())


def test_permissions():
    """Test 6: File Permissions (Unix only)"""
    print_header("TEST 6: File Permissions")
    
    if os.name != 'posix':
        print(f"  {Colors.YELLOW}⊘ SKIPPED{Colors.RESET} - Not a Unix system")
        return
    
    base_dir = Path('app/static/uploads')
    
    if not base_dir.exists():
        print(f"  {Colors.YELLOW}⊘ SKIPPED{Colors.RESET} - Upload directory doesn't exist")
        return
    
    # Check directory permissions
    stat = os.stat(base_dir)
    perms = oct(stat.st_mode)[-3:]
    
    print(f"  Upload directory permissions: {perms}")
    
    # Ideal: 755 (rwxr-xr-x)
    is_755 = perms == '755'
    print_test("Directory permissions are 755", is_755, f"Current: {perms}")
    
    # Check if any files exist
    files = list(base_dir.rglob('*'))
    files = [f for f in files if f.is_file() and not f.name.startswith('.')]
    
    if files:
        print(f"\n  Checking {len(files)} file(s):")
        for file in files[:5]:  # Check first 5
            stat = os.stat(file)
            perms = oct(stat.st_mode)[-3:]
            is_644 = perms == '644'
            print_test(f"{file.name}", is_644, f"Permissions: {perms}")
    else:
        print(f"  {Colors.YELLOW}⊘ INFO{Colors.RESET} - No uploaded files to check")


def test_import_dependencies():
    """Test 7: Dependencies"""
    print_header("TEST 7: Dependencies")
    
    # Test PIL import
    try:
        from PIL import Image
        print_test("PIL (Pillow) installed", True, "Required for image validation")
    except ImportError:
        print_test("PIL (Pillow) installed", False, "Install with: pip install Pillow")
    
    # Note: imghdr was removed in Python 3.13
    # We use PIL for image validation instead
    print_test("PIL-based validation", True, "Using PIL instead of deprecated imghdr")
    
    # Test werkzeug import
    try:
        from werkzeug.utils import secure_filename
        from werkzeug.datastructures import FileStorage
        print_test("Werkzeug installed", True, "Required for Flask")
    except ImportError:
        print_test("Werkzeug installed", False)


def test_upload_module():
    """Test 8: Upload Module"""
    print_header("TEST 8: Upload Module")
    
    try:
        from app.utils import upload
        print_test("Upload module imports", True)
        
        # Check all required functions exist
        required_funcs = [
            'allowed_file',
            'validate_image_content',
            'validate_image_with_pil',
            'generate_secure_filename',
            'save_image',
            'delete_image',
        ]
        
        for func_name in required_funcs:
            has_func = hasattr(upload, func_name)
            print_test(f"Function '{func_name}' exists", has_func)
        
    except ImportError as e:
        print_test("Upload module imports", False, str(e))


def run_all_tests():
    """Run all security tests"""
    print(f"\n{Colors.GREEN}╔═══════════════════════════════════════════════════════════╗{Colors.RESET}")
    print(f"{Colors.GREEN}║      SECURE IMAGE UPLOAD - SECURITY TEST SUITE           ║{Colors.RESET}")
    print(f"{Colors.GREEN}╚═══════════════════════════════════════════════════════════╝{Colors.RESET}")
    
    test_import_dependencies()
    test_upload_module()
    test_extension_validation()
    test_secure_filename_generation()
    test_file_size_limit()
    test_allowed_extensions()
    test_directory_structure()
    test_permissions()
    
    print(f"\n{Colors.GREEN}{'='*60}{Colors.RESET}")
    print(f"{Colors.GREEN}All security tests completed!{Colors.RESET}")
    print(f"{Colors.GREEN}{'='*60}{Colors.RESET}\n")
    
    print(f"{Colors.YELLOW}Next steps:{Colors.RESET}")
    print("  1. Review test results above")
    print("  2. Fix any failed tests")
    print("  3. Run: python scripts/setup_upload_permissions.sh")
    print("  4. Configure your web server (Nginx/Apache)")
    print("  5. Read: docs/SECURE_IMAGE_UPLOAD.md")
    print()


if __name__ == '__main__':
    run_all_tests()

