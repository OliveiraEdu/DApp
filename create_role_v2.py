import os
import sys
import binascii
from grpc import RpcError, StatusCode
import inspect
from iroha import Iroha, IrohaGrpc, IrohaCrypto
from iroha.primitive_pb2 import can_call_engine
from functools import wraps

IROHA_HOST_ADDR = os.getenv('IROHA_HOST_ADDR', '127.0.0.1')
IROHA_PORT = os.getenv('IROHA_PORT', '50051')
ADMIN_ACCOUNT_ID = os.getenv('ADMIN_ACCOUNT_ID', 'admin@test')
ADMIN_PRIVATE_KEY = os.getenv('ADMIN_PRIVATE_KEY', 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70')

iroha = Iroha(ADMIN_ACCOUNT_ID)
net = IrohaGrpc(f'{IROHA_HOST_ADDR}:{IROHA_PORT}')


# Here we will create user keys
user_private_key = IrohaCrypto.private_key()
user_public_key = IrohaCrypto.derive_public_key(user_private_key)




def trace(func):
    @wraps(func)
    def tracer(*args, **kwargs):
        name = func.__name__
        stack_size = int(len(inspect.stack(0)) / 2)
        indent = stack_size * '\t'
        print(f'{indent} > Entering "{name}": args: {args}')
        result = func(*args, **kwargs)
        print(f'{indent} < Leaving "{name}"')
        return result
    return tracer

@trace
def send_transaction_and_print_status(transaction):
    hex_hash = binascii.hexlify(IrohaCrypto.hash(transaction))
    creator_id = transaction.payload.reduced_payload.creator_account_id
    commands = get_commands_from_tx(transaction)
    print(f'Transaction "{commands}", hash = {hex_hash}, creator = {creator_id}')
    net.send_tx(transaction)
    handle_transaction_errors(transaction)

def handle_transaction_errors(transaction):
    for i, status in enumerate(net.tx_status_stream(transaction)):
        status_name, status_code, error_code = status
        print(f"{i}: status_name={status_name}, status_code={status_code}, error_code={error_code}")
        if status_name in ('STATEFUL_VALIDATION_FAILED', 'STATELESS_VALIDATION_FAILED', 'REJECTED'):
            handle_error(status_name, error_code, transaction)

def handle_error(status_name, error_code, transaction):
    error_messages = {
        'STATEFUL_VALIDATION_FAILED': 'Stateful validation failed',
        'STATELESS_VALIDATION_FAILED': 'Stateless validation failed',
        'REJECTED': 'Transaction rejected'
    }
    error_message = error_messages.get(status_name, 'Unknown error') + f': {error_code}'
    raise RuntimeError(f"{status_name} failed on tx: {transaction} due to reason {error_code}: {error_message}")

def get_commands_from_tx(transaction):
    commands_from_tx = []
    for command in transaction.payload.reduced_payload.__getattribute__("commands"):
        listed_fields = command.ListFields()
        commands_from_tx.append(listed_fields[0][0].name)
    return commands_from_tx



#Create Account

# Create Role
role_name = 'first_role'
role_permissions = [can_call_engine]

commands = [
    iroha.command('CreateRole', role_name=role_name, permissions=role_permissions)
]

tx = IrohaCrypto.sign_transaction(iroha.transaction(commands), ADMIN_PRIVATE_KEY)


# #Create Domain
# domain = 'first_domain'
# default_role = 'first_role'
# asset_id = 'first_asset'
# asset_short_id = 'first_coin'
# precision=2

# commands = [iroha.command('CreateDomain', domain_id=domain, default_role=default_role), iroha.command('CreateAsset', asset_name=asset_short_id, domain_id=domain, precision=precision)]

# tx = IrohaCrypto.sign_transaction(iroha.transaction(commands), ADMIN_PRIVATE_KEY)



# Error handling
try:
    send_transaction_and_print_status(tx)
except RuntimeError as e:
    print(f"Error occurred: {e}")
