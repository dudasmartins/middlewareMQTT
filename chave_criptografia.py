from cryptography.fernet import Fernet
nova_chave = Fernet.generate_key()
print(f"Chave gerada: {nova_chave.decode()}")

# Chave gerada: 9i7e0z0FtQNjj85riGhBy7ZAdxTs8gPSg7BFIUrvka8=