from multiversx_sdk import Address, Transaction, TransactionsConverter, ProxyNetworkProvider, UserSigner
import binascii

# Constants
ISSUER_ADDRESS = "your_issuer_address_here"  # The address of the account issuing the tokens
ISSUER_PRIVATE_KEY = "your_issuer_private_key_here"  # The private key of the issuer account for signing transactions
TOKEN_NAME = "WinterToken"  # Name of the token to be issued
TOKEN_TICKER = "WINTER"  # Ticker of the token, will be appended with a unique identifier
INITIAL_SUPPLY = 1000000000000000  # Total supply of tokens (100 million with 8 decimals)
DECIMALS = 8  # Number of decimal places the token will support
GAS_LIMIT = 60000000  # Maximum amount of gas that the transaction can consume
ISSUANCE_COST = 0.05 * 10**18  # Cost to issue the token, in EGLD (0.05 EGLD)

# Accounts generated on December 3rd that will receive the tokens
accounts = [
    "erd1...",  # Replace with actual account addresses
    "erd1...",
    "erd1..."
]

def hex_encode(value):
    """
    Helper function to convert a string to its hexadecimal representation.
    This is required for encoding data in the transaction payload.
    """
    return binascii.hexlify(value.encode()).decode()

def issue_token(account, proxy):
    """
    Issues a new token to the specified account.
    
    Parameters:
    - account: The account address that will receive the token.
    - proxy: The ProxyNetworkProvider instance to send transactions to the network.
    """
    # Prepare the data field of the transaction with the necessary details for token issuance
    data = f"issue@{hex_encode(TOKEN_NAME)}@{hex_encode(TOKEN_TICKER)}@{hex(INITIAL_SUPPLY)[2:]}@{hex(DECIMALS)[2:]}"

    # Create a new transaction for issuing tokens
    transaction = Transaction(
        sender=ISSUER_ADDRESS,
        receiver="erd1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqzllls8a5w6u",  # System smart contract address for issuing tokens
        value=ISSUANCE_COST,
        gas_limit=GAS_LIMIT,
        data=data,
        chain_id="T"  # Specify the chain ID (use "T" for testnet or the appropriate ID for mainnet)
    )

    # Sign the transaction using the issuer's private key
    signer = UserSigner.from_pem_file(ISSUER_PRIVATE_KEY)  # Load the signer with the issuer's private key
    transaction.signature = signer.sign(transaction)  # Sign the transaction

    # Send the transaction to the network
    tx_hash = proxy.send_transaction(transaction)
    print(f"Transaction sent for {account}, hash: {tx_hash}")  # Output the transaction hash for tracking

def main():
    """
    Main function to initialize the proxy provider and issue tokens to each account.
    """
    # Initialize the proxy provider to interact with the MultiversX network
    proxy = ProxyNetworkProvider("https://devnet-gateway.multiversx.com")  # Use the devnet gateway

    # Iterate over each account and issue tokens
    for account in accounts:
        issue_token(account, proxy)

if __name__ == "__main__":
    main()  # Run the main function when the script is executed