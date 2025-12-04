"""
Secure image upload utilities

This module provides secure image upload functionality with:
- File type validation (only images allowed)
- File size limits
- Secure filename generation
- Path traversal protection
- Content type verification
"""

import os
import secrets
from pathlib import Path
from typing import Optional, Tuple
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from PIL import Image


# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Maximum file size: 5MB
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB in bytes

# Image upload folder
UPLOAD_FOLDER = 'app/static/uploads/products'


def allowed_file(filename: str) -> bool:
    """
    Check if file has an allowed extension
    
    Args:
        filename: Name of the file to check
        
    Returns:
        True if extension is allowed, False otherwise
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_image_content(file_stream) -> bool:
    """
    Validate that the file is actually an image by checking its content
    
    Args:
        file_stream: File stream to validate
        
    Returns:
        True if file is a valid image, False otherwise
    """
    try:
        # Save current position
        pos = file_stream.tell()
        
        # Try to open image with PIL to identify format
        img = Image.open(file_stream)
        image_format = img.format.lower() if img.format else None
        
        # Reset file position
        file_stream.seek(pos)
        
        # Check if it's a valid image type
        # PIL formats: JPEG, PNG, GIF, etc.
        valid_pil_formats = {'jpeg', 'jpg', 'png', 'gif', 'webp'}
        return image_format in valid_pil_formats
    except Exception:
        return False


def validate_image_with_pil(file_stream) -> bool:
    """
    Validate image using PIL (Pillow) - more thorough validation
    
    Args:
        file_stream: File stream to validate
        
    Returns:
        True if file is a valid image that can be opened by PIL
    """
    try:
        # Save current position
        pos = file_stream.tell()
        
        # Try to open image with PIL
        img = Image.open(file_stream)
        img.verify()  # Verify it's a valid image
        
        # Reset file position
        file_stream.seek(pos)
        
        return True
    except Exception:
        return False


def generate_secure_filename(original_filename: str) -> str:
    """
    Generate a secure filename with random token
    
    Args:
        original_filename: Original filename from user
        
    Returns:
        Secure filename with random token
    """
    # Get file extension
    ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else 'jpg'
    
    # Generate random token (16 bytes = 32 hex characters)
    random_token = secrets.token_hex(16)
    
    # Return secure filename
    return f"{random_token}.{ext}"


def save_image(file: FileStorage, subfolder: str = 'products') -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Save uploaded image securely
    
    Args:
        file: FileStorage object from Flask request
        subfolder: Subfolder within uploads directory
        
    Returns:
        Tuple of (success: bool, filepath: str or None, error_message: str or None)
    """
    # Check if file exists
    if not file or file.filename == '':
        return False, None, "Nenhum arquivo selecionado"
    
    # Check file extension
    if not allowed_file(file.filename):
        return False, None, f"Tipo de arquivo não permitido. Use: {', '.join(ALLOWED_EXTENSIONS)}"
    
    # Check file size
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)  # Reset to beginning
    
    if file_size > MAX_FILE_SIZE:
        max_mb = MAX_FILE_SIZE / (1024 * 1024)
        return False, None, f"Arquivo muito grande. Tamanho máximo: {max_mb:.1f}MB"
    
    # Validate image content (first check with imghdr)
    if not validate_image_content(file.stream):
        return False, None, "O arquivo não é uma imagem válida"
    
    # Validate with PIL (more thorough)
    if not validate_image_with_pil(file.stream):
        return False, None, "O arquivo está corrompido ou não é uma imagem válida"
    
    # Generate secure filename
    filename = generate_secure_filename(file.filename)
    
    # Create upload directory if it doesn't exist
    upload_path = Path(UPLOAD_FOLDER) / subfolder
    upload_path.mkdir(parents=True, exist_ok=True)
    
    # Full file path
    filepath = upload_path / filename
    
    try:
        # Save file
        file.save(str(filepath))
        
        # Return relative path for database (web-accessible)
        relative_path = f"/static/uploads/{subfolder}/{filename}"
        return True, relative_path, None
        
    except Exception as e:
        return False, None, f"Erro ao salvar arquivo: {str(e)}"


def delete_image(image_path: str) -> bool:
    """
    Delete an uploaded image file
    
    Args:
        image_path: Path to image (relative web path like /static/uploads/products/xxx.jpg)
        
    Returns:
        True if deleted successfully, False otherwise
    """
    if not image_path:
        return False
    
    try:
        # Convert web path to filesystem path
        # Remove leading /static/ and convert to app/static/
        if image_path.startswith('/static/'):
            fs_path = 'app/static/' + image_path[8:]
        else:
            fs_path = image_path
        
        file_path = Path(fs_path)
        
        # Check if file exists and delete
        if file_path.exists() and file_path.is_file():
            file_path.unlink()
            return True
        
        return False
    except Exception:
        return False


def get_image_info(file: FileStorage) -> Optional[dict]:
    """
    Get information about an image file
    
    Args:
        file: FileStorage object
        
    Returns:
        Dictionary with image info or None if invalid
    """
    try:
        img = Image.open(file.stream)
        file.stream.seek(0)  # Reset stream
        
        return {
            'format': img.format,
            'mode': img.mode,
            'size': img.size,
            'width': img.width,
            'height': img.height,
        }
    except Exception:
        return None

