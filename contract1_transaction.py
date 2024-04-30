import os
from iroha import Iroha, IrohaCrypto, IrohaGrpc

iroha = Iroha('admin@test')
net = IrohaGrpc('127.0.0.1:50051')


# Here is the information about the environment and admin account information:
IROHA_HOST_ADDR = os.getenv('IROHA_HOST_ADDR', '127.0.0.1')
IROHA_PORT = os.getenv('IROHA_PORT', '50051')
ADMIN_ACCOUNT_ID = os.getenv('ADMIN_ACCOUNT_ID', 'admin@test')
ADMIN_PRIVATE_KEY = os.getenv(
    'ADMIN_PRIVATE_KEY', 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70')


admin_key = os.getenv(ADMIN_PRIVATE_KEY, IrohaCrypto.private_key())
params = ("40c10f19"                                                          # selector
          "000000000000000000000000f205c4a929072dd6e7fc081c2a78dbc79c76070b"  # address
          "00000000000000000000000000000000000000000000000000000000000003E8"  # amount
         )

tx = iroha.transaction([
    iroha.command('CallEngine', callee='ServiceContract', input=params)
])
IrohaCrypto.sign_transaction(tx, admin_key)

net.send_tx(tx)


for status in net.tx_status_stream(tx):
    print(status)
