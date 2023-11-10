import hashlib
from web3 import Web3

from Cryptodome.PublicKey import ECC
from Cryptodome.Hash import SHA256
from base58 import b58encode_check

def generate_wallet_address():
    # Генерувати приватний ключ
    private_key = ECC.generate(curve='P-256')

    # Отримати публічний ключ з приватного ключа
    public_key = private_key.public_key()

    # Отримати байтове представлення публічного ключа
    public_key_bytes = public_key.export_key(format='DER')

    # Обчислити хеш публічного ключа
    hash_object = SHA256.new(public_key_bytes)
    hash_bytes = hash_object.digest()

    # Отримати адресу кошелька з хешу
    wallet_address = b58encode_check(hash_bytes)

    return wallet_address

# Викликати функцію для генерації адреси кошелька
address = generate_wallet_address()
print(f"Згенерована адреса кошелька: {address}")


def find_lost_wallets():
    # Створіть список з можливими адресами кошельків
    wallet_addresses = [
        'FGp8AJZMo7Y3LqZ928Lg8rtR1X65cMXpSLZavHcPuZTJsETNH',
        '0x987654321fedcba',
        '0xabcdef123456789',
        '0xfedcba987654321'
    ]

    # Переберіть кожну адресу кошелька
    for address in wallet_addresses:
        # Згенеруйте хеш адреси
        hash_address = hashlib.sha256(address.encode()).hexdigest()

        # Перевірте, чи існує кошелек з таким хешем
        if check_wallet_existence(hash_address):
            print(f"Знайдено загублений або заброшений кошелек: {address}")

def check_wallet_existence(hash_address):
    # Перевірте базу даних або зверніться до блокчейну для перевірки існування кошелька з хешем адреси
    # Ось приклад, як ви можете перевірити існування кошелька на блокчейні Ethereum за допомогою бібліотеки Web3.py:

    # Підключення до блокчейну Ethereum
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/your_infura_project_id'))

    # Перевірка існування кошелька за адресою
    if w3.is_address(hash_address):
        return True
    else:
        return False

# Викликати функцію для пошуку загублених або заброшених кошельків
find_lost_wallets()
