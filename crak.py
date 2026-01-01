import hashlib
import os


def load_wordlist(filepath):
    """Load common passwords from a wordlist file."""
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Error reading wordlist: {e}")
        return []


def hash_password(password, hash_type):
    """Hash a password using the specified algorithm."""
    if hash_type == 'md5':
        return hashlib.md5(password.encode()).hexdigest()
    elif hash_type == 'sha1':
        return hashlib.sha1(password.encode()).hexdigest()
    elif hash_type == 'sha256':
        return hashlib.sha256(password.encode()).hexdigest()
    return None


def detect_hash_type(hash_str):
    """Detect hash type based on length."""
    length = len(hash_str)
    if length == 32:
        return 'md5'
    elif length == 40:
        return 'sha1'
    elif length == 64:
        return 'sha256'
    return None


def crack_hash(target_hash, wordlist):
    """Attempt to crack hash using wordlist."""
    hash_type = detect_hash_type(target_hash)
    
    if not hash_type:
        print(f"Unknown hash type (length: {len(target_hash)})")
        return None
    
    print(f"Detected hash type: {hash_type.upper()}")
    print(f"Attempting to crack {len(wordlist)} passwords...")
    
    for idx, password in enumerate(wordlist):
        if (idx + 1) % 10000 == 0:
            print(f"  Tried {idx + 1} passwords...")
        
        hashed = hash_password(password, hash_type)
        if hashed == target_hash:
            return password
    
    return None


def main():
    user_hash = input("Enter hash to crack: ").strip()
    cleaned_hash = user_hash.replace(" ", "").lower()
    
    # Try common wordlist locations
    wordlist_paths = [
        'rockyou.txt',
        'wordlist.txt',
        os.path.expanduser('~/wordlists/rockyou.txt'),
        '/usr/share/wordlists/rockyou.txt',
    ]
    
    wordlist = []
    for path in wordlist_paths:
        wordlist = load_wordlist(path)
        if wordlist:
            print(f"Loaded {len(wordlist)} passwords from {path}")
            break
    
    if not wordlist:
        print("No wordlist found. Using default passwords...")
        wordlist = [
            'password', '123456', 'password123', 'admin', 'letmein',
            'welcome', 'monkey', '1234567', 'dragon', '12345678',
            'sunshine', 'qwerty', 'abc123', '123123', 'password1'
        ]
    
    result = crack_hash(cleaned_hash, wordlist)
    
    if result:
        print(f"\n✓ Hash cracked! Password: {result}")
    else:
        print(f"\n✗ Password not found in wordlist.")
    
    try:
        input("\nPress Enter to exit...")
    except EOFError:
        pass


if __name__ == '__main__':
    main()