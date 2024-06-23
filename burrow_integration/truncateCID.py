import hashlib
import base58

# In-memory storage for mapping (could be replaced with a database or other storage)
cid_storage = {}

def get_hash(input_string):
    return hashlib.sha256(input_string.encode()).hexdigest()[:8]  # Take first 8 characters of the SHA-256 hash

def encode_cid(cid):
    truncated_cid = cid[:32]
    remaining_cid = cid[32:]
    hash_of_remaining = get_hash(remaining_cid)
    combined = truncated_cid + hash_of_remaining
    encoded = base58.b58encode(combined.encode()).decode()
    
    # Store the original CID using the truncated part and the hash as the key
    cid_storage[encoded] = cid
    
    return encoded

def decode_cid(encoded_cid):
    decoded_combined = base58.b58decode(encoded_cid).decode()
    truncated_cid = decoded_combined[:32]
    hash_of_remaining = decoded_combined[32:]
    return truncated_cid, hash_of_remaining

def get_original_cid(encoded_cid):
    # Retrieve the original CID from the storage
    return cid_storage.get(encoded_cid, None)

# Verify the process
original_cid = "QmW2HkQ1A4Hmq1H2NdC3g9kuTjVpbxTAcNev4VbyRcKbuW"

# Encode the CID
encoded_cid = encode_cid(original_cid)
print(f"Encoded CID: {encoded_cid}")

# Decode the encoded CID
truncated_cid, hash_of_remaining = decode_cid(encoded_cid)
print(f"Truncated CID: {truncated_cid}")
print(f"Hash of Remaining: {hash_of_remaining}")

# Get the original CID back
retrieved_cid = get_original_cid(encoded_cid)
print(f"Original CID: {retrieved_cid}")

# Check if the original CID matches the retrieved CID
assert original_cid == retrieved_cid, "Original CID and retrieved CID do not match!"
print("Original CID successfully retrieved!")
