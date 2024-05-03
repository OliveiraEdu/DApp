import commons
import logging
from iroha import Iroha, IrohaCrypto
from iroha.primitive_pb2 import can_create_role, can_create_domain, can_call_engine

# Configure logging
logging.basicConfig(level=logging.INFO)  # Set the logging level to INFO
logger = logging.getLogger(__name__)

admin = commons.new_user('admin@test')
alice = commons.new_user('alice@test')
iroha = Iroha(admin['id'])

@commons.hex
def create_role_tx():
    role_permissions = [can_call_engine]
    tx = iroha.transaction([
        iroha.command('CreateRole', role_name='burrow', permissions=role_permissions)
    ], creator_account=admin['id'])  # Corrected creator_account
    IrohaCrypto.sign_transaction(tx, admin['key'])  # Assuming alice is signing
    logger.info("Generated create role transaction successfully.")
    return tx
