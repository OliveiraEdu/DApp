import ipfshttpclient

# Connect to the IPFS node at a specific IP address
client = ipfshttpclient.connect('/dns/localhost/tcp/5001/http')  # Replace with your IP address and port

def upload_file_to_ipfs(file_path):
    # Add the file to IPFS
    result = client.add(file_path)
    return result['Hash']

def download_file_from_ipfs(cid, output_path):
    # Retrieve the file from IPFS
    file_data = client.cat(cid)
    # Save the file locally
    with open(output_path, 'wb') as f:
        f.write(file_data)

# Specify the path to the file you want to upload
local_file_path = '/home/eduardo/Git/DApp/commons.py'

# Upload the file to IPFS and get the CID
file_cid = upload_file_to_ipfs(local_file_path)
print(f'Uploaded file CID: {file_cid}')

# Specify the path where you want to save the downloaded file
downloaded_file_path = '/home/eduardo/download/file1.txt'

# Download the file from IPFS using the CID and save it locally
download_file_from_ipfs(file_cid, downloaded_file_path)
print(f'File downloaded and saved to: {downloaded_file_path}')
