import json
import os

from solana.rpc.api import Client
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.transaction import AccountMeta, Transaction, TransactionInstruction

PROGRAM_KEYPAIR_PATH = os.getcwd() + '/dist/program/hello_solana-keypair.json'
MY_KEYPAIR_PATH = os.path.expanduser('~') + '/.config/solana/id.json'



def main():
    print("Launching client...")

    ## Connection to cluster
    connection = Client("https://api.devnet.solana.com")  # http client
    if connection is not None:
        print("Connection established.")

    ## Get program key
    with open(PROGRAM_KEYPAIR_PATH, 'r') as f:
        program_secret_key = json.load(f)
    print(f"secret key is {program_secret_key}")
    program_keypair: Keypair = Keypair.from_secret_key(
        bytes(program_secret_key))
    programid: PublicKey = program_keypair.public_key
    print(programid)

    ## Generate a account (keypair) to transact with our program
    # with open(MY_KEYPAIR_PATH, 'r') as f:
    #     my_secret_key = json.load(f)
    # trigger_keypair = Keypair.from_secret_key(bytes(my_secret_key))

    trigger_keypair = Keypair()
    resp = connection.request_airdrop(trigger_keypair.public_key, 1000000000)  # Airdrop 1 SOL 
    connection.confirm_transaction(resp.value)

    
    print(f"keypair is {trigger_keypair.public_key}")

    ## Conduct a transaction with our program
    print(f"--Printing Program {programid.to_base58()}")

    instruction = TransactionInstruction(
            [AccountMeta(trigger_keypair.public_key, False, True)] # List of Accounts
            , programid, # Program PublicKey
            bytes(0) # Instruction data, For example: bytearray.fromhex('000000000000000000')
            )

    print(instruction)
    connection.send_transaction(
        Transaction().add(instruction), trigger_keypair)


if __name__ == "__main__":
    main()
