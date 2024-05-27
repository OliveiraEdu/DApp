import os
import sys
import binascii
from grpc import RpcError, StatusCode
import inspect
from iroha import Iroha, IrohaGrpc, IrohaCrypto
from functools import wraps

IROHA_HOST_ADDR = os.getenv('IROHA_HOST_ADDR', '127.0.0.1')
IROHA_PORT = os.getenv('IROHA_PORT', '50051')
ADMIN_ACCOUNT_ID = os.getenv('ADMIN_ACCOUNT_ID', 'admin@test')
ADMIN_PRIVATE_KEY = os.getenv('ADMIN_PRIVATE_KEY', 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70')

iroha = Iroha(ADMIN_ACCOUNT_ID)
net = IrohaGrpc(f'{IROHA_HOST_ADDR}:{IROHA_PORT}')

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

bytecode = ("6080604052348015600e575f80fd5b50335f806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055506105f28061005b5f395ff3fe608060405234801561000f575f80fd5b506004361061004a575f3560e01c8063075461721461004e57806327e235e31461006c57806340c10f191461009c578063d0679d34146100b8575b5f80fd5b6100566100d4565b60405161006391906103c2565b60405180910390f35b61008660048036038101906100819190610409565b6100f7565b604051610093919061044c565b60405180910390f35b6100b660048036038101906100b1919061048f565b61010c565b005b6100d260048036038101906100cd919061048f565b6101dd565b005b5f8054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b6001602052805f5260405f205f915090505481565b5f8054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614610162575f80fd5b789f4f2726179a224501d762422c946590d910000000000000008110610186575f80fd5b8060015f8473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f205f8282546101d291906104fa565b925050819055505050565b60015f3373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f205481111561029e578060015f3373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f20546040517fcf47918100000000000000000000000000000000000000000000000000000000815260040161029592919061052d565b60405180910390fd5b8060015f3373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f205f8282546102ea9190610554565b925050819055508060015f8473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f205f82825461033d91906104fa565b925050819055507f3990db2d31862302a685e8086b5755072a6e2b5b780af1ee81ece35ee3cd334533838360405161037793929190610587565b60405180910390a15050565b5f73ffffffffffffffffffffffffffffffffffffffff82169050919050565b5f6103ac82610383565b9050919050565b6103bc816103a2565b82525050565b5f6020820190506103d55f8301846103b3565b92915050565b5f80fd5b6103e8816103a2565b81146103f2575f80fd5b50565b5f81359050610403816103df565b92915050565b5f6020828403121561041e5761041d6103db565b5b5f61042b848285016103f5565b91505092915050565b5f819050919050565b61044681610434565b82525050565b5f60208201905061045f5f83018461043d565b92915050565b61046e81610434565b8114610478575f80fd5b50565b5f8135905061048981610465565b92915050565b5f80604083850312156104a5576104a46103db565b5b5f6104b2858286016103f5565b92505060206104c38582860161047b565b9150509250929050565b7f4e487b71000000000000000000000000000000000000000000000000000000005f52601160045260245ffd5b5f61050482610434565b915061050f83610434565b9250828201905080821115610527576105266104cd565b5b92915050565b5f6040820190506105405f83018561043d565b61054d602083018461043d565b9392505050565b5f61055e82610434565b915061056983610434565b9250828203905081811115610581576105806104cd565b5b92915050565b5f60608201905061059a5f8301866103b3565b6105a760208301856103b3565b6105b4604083018461043d565b94935050505056fea2646970667358221220b6a6795e72e12f1e89a1a967830feb92a3f9d3d3e571a0f7b8e09a257c6d4fba64736f6c634300081a0033")

commands = [
    iroha.command('CallEngine', caller='admin@test', input=bytecode)
]

tx = IrohaCrypto.sign_transaction(iroha.transaction(commands), ADMIN_PRIVATE_KEY)

# Error handling
try:
    send_transaction_and_print_status(tx)
except RuntimeError as e:
    print(f"Error occurred: {e}")
