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

bytecode = ("6080604052348015600e575f80fd5b50335f806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055506105de8061005b5f395ff3fe608060405234801561000f575f80fd5b506004361061004a575f3560e01c8063075461721461004e57806327e235e31461006c57806340c10f191461009c578063d0679d34146100b8575b5f80fd5b6100566100d4565b604051610063919061035d565b60405180910390f35b610086600480360381019061008191906103a4565b6100f7565b60405161009391906103e7565b60405180910390f35b6100b660048036038101906100b1919061042a565b61010c565b005b6100d260048036038101906100cd919061042a565b6101b9565b005b5f8054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b6001602052805f5260405f205f915090505481565b5f8054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614610162575f80fd5b8060015f8473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f205f8282546101ae9190610495565b925050819055505050565b60015f3373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f2054811115610239576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161023090610522565b60405180910390fd5b8060015f3373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f205f8282546102859190610540565b925050819055508060015f8473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020015f205f8282546102d89190610495565b925050819055507f3990db2d31862302a685e8086b5755072a6e2b5b780af1ee81ece35ee3cd334533838360405161031293929190610573565b60405180910390a15050565b5f73ffffffffffffffffffffffffffffffffffffffff82169050919050565b5f6103478261031e565b9050919050565b6103578161033d565b82525050565b5f6020820190506103705f83018461034e565b92915050565b5f80fd5b6103838161033d565b811461038d575f80fd5b50565b5f8135905061039e8161037a565b92915050565b5f602082840312156103b9576103b8610376565b5b5f6103c684828501610390565b91505092915050565b5f819050919050565b6103e1816103cf565b82525050565b5f6020820190506103fa5f8301846103d8565b92915050565b610409816103cf565b8114610413575f80fd5b50565b5f8135905061042481610400565b92915050565b5f80604083850312156104405761043f610376565b5b5f61044d85828601610390565b925050602061045e85828601610416565b9150509250929050565b7f4e487b71000000000000000000000000000000000000000000000000000000005f52601160045260245ffd5b5f61049f826103cf565b91506104aa836103cf565b92508282019050808211156104c2576104c1610468565b5b92915050565b5f82825260208201905092915050565b7f496e73756666696369656e742062616c616e63650000000000000000000000005f82015250565b5f61050c6014836104c8565b9150610517826104d8565b602082019050919050565b5f6020820190508181035f83015261053981610500565b9050919050565b5f61054a826103cf565b9150610555836103cf565b925082820390508181111561056d5761056c610468565b5b92915050565b5f6060820190506105865f83018661034e565b610593602083018561034e565b6105a060408301846103d8565b94935050505056fea264697066735822122063bffd3e6838ef80a6415de2e9c69b4d4df4721af90cdcb571c6ac471f7e246564736f6c63430008190033")

commands = [
    iroha.command('CallEngine', caller='admin@test', input=bytecode)
]

tx = IrohaCrypto.sign_transaction(iroha.transaction(commands), ADMIN_PRIVATE_KEY)

# Error handling
try:
    send_transaction_and_print_status(tx)
except RuntimeError as e:
    print(f"Error occurred: {e}")
