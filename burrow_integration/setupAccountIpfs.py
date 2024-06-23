import os
import binascii
import ipfshttpclient
from iroha import IrohaCrypto, Iroha, IrohaGrpc
import integration_helpers
from name_generator import left, right
import random

# IPFS configuration
IPFS_HOST = '/dns/localhost/tcp/5001/http'  # Replace with your IP address and port
try:
    client = ipfshttpclient.connect(IPFS_HOST)
    print("Connected to IPFS successfully.")
except Exception as e:
    print(f"Failed to connect to IPFS: {e}")
    raise

# Iroha configuration
IROHA_HOST_ADDR = os.getenv("IROHA_HOST_ADDR", "127.0.0.1")
IROHA_PORT = os.getenv("IROHA_PORT", "50051")
net = IrohaGrpc(f"{IROHA_HOST_ADDR}:{IROHA_PORT}")

ADMIN_ACCOUNT_ID = os.getenv("ADMIN_ACCOUNT_ID", "admin@test")
ADMIN_PRIVATE_KEY = os.getenv(
    "ADMIN_PRIVATE_KEY",
    "f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70",
)
iroha_admin = Iroha(ADMIN_ACCOUNT_ID)

DOMAIN = "test"
user_private_key = "1234567890123456789012345678901234567890123456789012345678901234"

def generate_random_asset_name():
    left_part = random.choice(left)
    return f"{left_part}_coin"

def upload_file_to_ipfs(file_path):
    try:
        result = client.add(file_path)
        print(f"File uploaded to IPFS successfully: {result['Hash']}")
        return result['Hash']
    except Exception as e:
        print(f"Failed to upload file to IPFS: {e}")
        return None

@integration_helpers.trace
def create_and_setup_account(contract_address: str, user_account_short_id: str, filename: str, cid: str, public_key: str, asset_id: str):
    try:
        params = integration_helpers.get_first_four_bytes_of_keccak(
            b"createAndSetupAccount(string,string,string,string,string,string,string,string,string,string)"
        )
        no_of_param = 10
        for x in range(no_of_param):
            params = params + integration_helpers.left_padded_address_of_param(
                x, no_of_param
            )
        params = params + integration_helpers.argument_encoding(
            ADMIN_ACCOUNT_ID
        )  # admin account id
        params = params + integration_helpers.argument_encoding(
            user_account_short_id
        )  # user account name
        params = params + integration_helpers.argument_encoding(
            f"{user_account_short_id}@{DOMAIN}"
        )  # user account id
        params = params + integration_helpers.argument_encoding(asset_id)  # asset id
        params = params + integration_helpers.argument_encoding(DOMAIN)  # domain name
        params = params + integration_helpers.argument_encoding(
            "set up balance"
        )  # description
        params = params + integration_helpers.argument_encoding("100")  # amount
        params = params + integration_helpers.argument_encoding(
            filename
        )  # key for user detail (filename)
        params = params + integration_helpers.argument_encoding(
            cid
        )  # value for user detail (CID)
        params = params + integration_helpers.argument_encoding(
            public_key
        )  # public key of user
        tx = iroha_admin.transaction(
            [
                iroha_admin.command(
                    "CallEngine",
                    caller=ADMIN_ACCOUNT_ID,
                    callee=contract_address,
                    input=params,
                )
            ]
        )
        IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
        response = net.send_tx(tx)
        for status in net.tx_status_stream(tx):
            print(status)
        return response
    except Exception as e:
        print(f"Error creating and setting up account: {e}")
        return None

@integration_helpers.trace
def create_contract():
    try:
        bytecode = ""
        """Bytecode was generated using remix editor  https://remix.ethereum.org/ from file setupAccount.sol. """
        tx = iroha_admin.transaction(
            [iroha_admin.command("CallEngine", caller=ADMIN_ACCOUNT_ID, input=bytecode)]
        )
        IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
        net.send_tx(tx)
        hex_hash = binascii.hexlify(IrohaCrypto.hash(tx))
        for status in net.tx_status_stream(tx):
            print(status)
        return hex_hash
    except Exception as e:
        print(f"Error creating contract: {e}")
        return None

@integration_helpers.trace
def sets_asset(contract_address: str, asset_id: str, amount: str):
    try:
        asset, domain = asset_id.split("#")
        params = integration_helpers.get_first_four_bytes_of_keccak(
            b"setsAsset(string,string,string,string,string)"
        )
        no_of_param = 5
        for x in range(no_of_param):
            params = params + integration_helpers.left_padded_address_of_param(
                x, no_of_param
            )
        params = params + integration_helpers.argument_encoding(asset)  # asset name
        params = params + integration_helpers.argument_encoding(domain)  # domain name
        params = params + integration_helpers.argument_encoding("4")  # precision
        params = params + integration_helpers.argument_encoding(asset_id)  # asset id
        params = params + integration_helpers.argument_encoding(amount)  # amount
        tx = iroha_admin.transaction(
            [
                iroha_admin.command(
                    "CallEngine",
                    caller=ADMIN_ACCOUNT_ID,
                    callee=contract_address,
                    input=params,
                )
            ]
        )
        IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
        print(f"Transaction to set asset:\n{tx}")
        response = net.send_tx(tx)
        for status in net.tx_status_stream(tx):
            print(status)
        if response:
            print("Asset set successfully.")
        else:
            print("Failed to set asset.")
        return response
    except Exception as e:
        print(f"Error setting asset: {e}")
        return None

def print_paragraph(text: str):
    print(10 * "-", text, ":", 10 * "-")

@integration_helpers.trace
def get_account_details(contract_address: str, user_account: str):
    try:
        iroha_user = Iroha(user_account)
        params = integration_helpers.get_first_four_bytes_of_keccak(b"getAccountDetail()")
        no_of_param = 0
        tx = iroha_user.transaction(
            [
                iroha_user.command(
                    "CallEngine", caller=user_account, callee=contract_address, input=params
                )
            ]
        )
        IrohaCrypto.sign_transaction(tx, user_private_key)
        response = net.send_tx(tx)
        for status in net.tx_status_stream(tx):
            print(status)
        return response
    except Exception as e:
        print(f"Error getting account details: {e}")
        return None

@integration_helpers.trace
def balance(address: str, user_id: str, ASSET_ID: str):
    try:
        params = integration_helpers.get_first_four_bytes_of_keccak(
            b"queryBalance(string,string)"
        )
        no_of_param = 2
        for x in range(no_of_param):
            params = params + integration_helpers.left_padded_address_of_param(
                x, no_of_param
            )
        params = params + integration_helpers.argument_encoding(user_id)  # account id
        params = params + integration_helpers.argument_encoding(ASSET_ID)  # asset id
        tx = iroha_admin.transaction(
            [
                iroha_admin.command(
                    "CallEngine", caller=ADMIN_ACCOUNT_ID, callee=address, input=params
                )
            ]
        )
        IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
        response = net.send_tx(tx)
        for status in net.tx_status_stream(tx):
            print(status)
        return response
    except Exception as e:
        print(f"Error querying balance: {e}")
        return None

def main():
    try:
        print_paragraph("Preparation")
        hash = create_contract()
        if not hash:
            print("Failed to create contract.")
            return
        address = integration_helpers.get_engine_receipts_address(hash)
        print(f"Contract created with address: {address}")
        
        asset_name = generate_random_asset_name()
        asset_id = f"{asset_name}#{DOMAIN}"
        amount = random.randint(1, 1000)
        print(f"Setting asset with ID: {asset_id}, Amount: {amount}")
        response = sets_asset(address, asset_id, str(amount))
        # if not response:
        #     print("Failed to set asset.")
        #     return
        print(f"Contract address: {address}")
        print(f"Asset ID: {asset_id}, Amount: {amount}")

        # Specify the path to the file you want to upload
        local_file_path = '/home/eduardo/Git/DApp/queries.py'
        if not os.path.exists(local_file_path):
            print(f"File does not exist: {local_file_path}")
            return

        # Upload the file to IPFS and get the CID
        file_cid = upload_file_to_ipfs(local_file_path)
        if file_cid:
            print(f'Uploaded file CID: {file_cid}')

            user_account_left = random.choice(left)
            user_account_right = random.choice(right)
            user_account_short_id = f"{user_account_left}_{user_account_right}"
            print(f"Creating account with name: {user_account_short_id}")

            print_paragraph("Creating account")
            success = create_and_setup_account(address, user_account_short_id, os.path.basename(local_file_path), file_cid, user_private_key, asset_id)
            # if success:
            #     print("Account created and set up successfully.")
            # else:
            #     print("Failed to create and set up account.")

            # Uncomment the following lines if you want to check account details and balance
            # print_paragraph("Checking account")
            # response = get_account_details(address, f"{user_account_short_id}@{DOMAIN}")
            # integration_helpers.get_engine_receipts_result(response)
            # response = balance(address, f"{user_account_short_id}@{DOMAIN}", asset_id)
            # integration_helpers.get_engine_receipts_result(response)
        else:
            print("File upload to IPFS failed.")
    except Exception as e:
        print(f"An error occurred in the main function: {e}")

if __name__ == "__main__":
    main()
