"""
Simple XOR encryption for quiz data obfuscation.

This module provides basic obfuscation using XOR cipher with 0xA5 key.
It is designed to prevent casual viewing of quiz answers and results,
NOT for securing sensitive data.

The implementation supports:
- Automatic detection of encrypted vs plain JSON files
- Backwards compatibility with existing plain JSON files
- UTF-8 character preservation (accents, special characters)
- Symmetric encryption (same operation for encrypt/decrypt)
"""

import json
from typing import Dict, Any


# XOR encryption key
XOR_KEY = 0xA5


def xor_bytes(data: bytes, key: int = XOR_KEY) -> bytes:
    """
    Apply XOR cipher to bytes.

    XOR is symmetric: applying it twice returns the original data.
    This means the same function works for both encryption and decryption.

    Args:
        data: Bytes to encrypt/decrypt
        key: XOR key (default 0xA5)

    Returns:
        Encrypted/decrypted bytes

    Example:
        >>> original = b"Hello"
        >>> encrypted = xor_bytes(original)
        >>> decrypted = xor_bytes(encrypted)
        >>> original == decrypted
        True
    """
    return bytes(b ^ key for b in data)


def is_encrypted(data: bytes) -> bool:
    """
    Detect if data is encrypted or plain JSON.

    Detection logic:
    - Plain JSON always starts with '{' (0x7B) or '[' (0x5B)
    - Or whitespace characters (0x20, 0x09, 0x0A, 0x0D)
    - After XOR with 0xA5: '{' becomes 0xDE, '[' becomes 0xFE
    - These encrypted values are unlikely to appear as first byte of valid UTF-8

    Args:
        data: Raw file bytes

    Returns:
        True if encrypted, False if plain JSON

    Example:
        >>> plain = b'{"key": "value"}'
        >>> is_encrypted(plain)
        False
        >>> encrypted = xor_bytes(plain)
        >>> is_encrypted(encrypted)
        True
    """
    if not data:
        return False

    first_byte = data[0]

    # Check for plain JSON markers
    # { (0x7B), [ (0x5B), space (0x20), tab (0x09), newline (0x0A), carriage return (0x0D)
    if first_byte in (0x7B, 0x5B, 0x20, 0x09, 0x0A, 0x0D):
        return False

    # Check for encrypted JSON markers
    # { XOR 0xA5 = 0xDE, [ XOR 0xA5 = 0xFE
    if first_byte in (0xDE, 0xFE):
        return True

    # Default to encrypted if ambiguous (safer assumption)
    return True


def encrypt_json(data: Dict[str, Any]) -> bytes:
    """
    Encrypt JSON data to bytes.

    Process:
    1. Convert dict to JSON string with formatting
    2. Encode to UTF-8 bytes
    3. Apply XOR encryption

    Args:
        data: Dictionary to encrypt

    Returns:
        Encrypted bytes ready to write to file

    Example:
        >>> data = {"name": "Quiz", "count": 5}
        >>> encrypted = encrypt_json(data)
        >>> isinstance(encrypted, bytes)
        True
        >>> is_encrypted(encrypted)
        True
    """
    # Convert to JSON string with pretty formatting (same as original)
    json_str = json.dumps(data, indent=2, ensure_ascii=False)

    # Encode to UTF-8 bytes
    json_bytes = json_str.encode('utf-8')

    # Apply XOR encryption
    return xor_bytes(json_bytes)


def decrypt_json(encrypted_data: bytes) -> Dict[str, Any]:
    """
    Decrypt bytes to JSON data.

    Process:
    1. Apply XOR decryption (same as encryption, symmetric)
    2. Decode UTF-8 bytes to string
    3. Parse JSON string to dict

    Args:
        encrypted_data: Encrypted bytes

    Returns:
        Decrypted dictionary

    Raises:
        UnicodeDecodeError: If decrypted data is not valid UTF-8
        json.JSONDecodeError: If decrypted data is not valid JSON

    Example:
        >>> data = {"test": True}
        >>> encrypted = encrypt_json(data)
        >>> decrypted = decrypt_json(encrypted)
        >>> data == decrypted
        True
    """
    # XOR is symmetric, so decryption is same operation as encryption
    json_bytes = xor_bytes(encrypted_data)

    # Decode UTF-8 to string
    json_str = json_bytes.decode('utf-8')

    # Parse JSON
    return json.loads(json_str)


def load_json(file_bytes: bytes) -> Dict[str, Any]:
    """
    Load JSON from bytes, auto-detecting encryption.

    This function provides backwards compatibility by detecting
    whether the file is encrypted or plain JSON and handling both.

    Process:
    1. Detect if data is encrypted using is_encrypted()
    2. If encrypted: decrypt and parse
    3. If plain: parse directly

    Args:
        file_bytes: Raw file bytes

    Returns:
        Parsed JSON dictionary

    Raises:
        UnicodeDecodeError: If data is not valid UTF-8
        json.JSONDecodeError: If data is not valid JSON

    Example:
        >>> # Works with encrypted data
        >>> encrypted = encrypt_json({"a": 1})
        >>> load_json(encrypted)
        {'a': 1}
        >>> # Works with plain JSON
        >>> plain = b'{"a": 1}'
        >>> load_json(plain)
        {'a': 1}
    """
    if is_encrypted(file_bytes):
        # File is encrypted, decrypt it
        return decrypt_json(file_bytes)
    else:
        # File is plain JSON, parse directly
        json_str = file_bytes.decode('utf-8')
        return json.loads(json_str)


def save_json(data: Dict[str, Any], encrypt: bool = True) -> bytes:
    """
    Save JSON to bytes with optional encryption.

    Args:
        data: Dictionary to save
        encrypt: Whether to encrypt (default True)

    Returns:
        Bytes to write to file

    Example:
        >>> data = {"quiz": "test"}
        >>> # Encrypted
        >>> encrypted = save_json(data, encrypt=True)
        >>> is_encrypted(encrypted)
        True
        >>> # Plain
        >>> plain = save_json(data, encrypt=False)
        >>> is_encrypted(plain)
        False
    """
    if encrypt:
        return encrypt_json(data)
    else:
        # Plain JSON with formatting
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        return json_str.encode('utf-8')
