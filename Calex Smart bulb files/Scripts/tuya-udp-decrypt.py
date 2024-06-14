import binascii
from Cryptodome.Cipher import AES
from hashlib import md5

# Padding and unpadding functions
pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

# Encrypt and decrypt functions using AES
encrypt = lambda msg, key: AES.new(key, AES.MODE_ECB).encrypt(pad(msg).encode())
decrypt = lambda msg, key: unpad(AES.new(key, AES.MODE_ECB).decrypt(msg)).decode()

# UDP decrypt key, credits to https://github.com/ct-Open-Source/tuya-convert/blob/master/scripts/tuya-discovery.py for discovering the key
udpkey = md5(b"yGAdlopoPVldABfn").digest()

# Function to decrypt the UDP message
def decrypt_udp(msg):
    return decrypt(msg, udpkey)

# Function to parse the header of the UDP message
def parse_header(data):
    if data[:4] == b'\x00\x00U\xaa':
        return True
    return False


def main():
    # Provided UDP data packet (hexadecimal format)
    udp_data_hex = "000055aa00000000000000130000009c00000000a2d5ce15a71d24b3246c6683ee8406e2e6e7cd9d529bba5505c1972b37281bb8ea2f32b8c29872ba171125690e75bb185b59263941417902f831f2b006b18fe0e5009ca4c2b6940ff0c50c5e4948159f02da2d7bf10b10284b5270bc2b6fd23130cd4dacae9954c728976085659e957d029c794eb678b36cb86064dccd4ba96449d7c04d4bd0e855432b819cbf4452f6cc730c720000aa55"
    udp_data_bytes = binascii.unhexlify(udp_data_hex)

    # Check if the packet has a valid header
    if parse_header(udp_data_bytes):
        # Extract the payload from the UDP data
        payload = udp_data_bytes[20:-8]
        try:
            # Attempt to decrypt the payload
            decrypted_data = decrypt_udp(payload)
            print("Decrypted data:", decrypted_data)
        except Exception as e:
            print("Failed to decrypt the data:", str(e))
    else:
        print("Invalid UDP packet header")

if __name__ == "__main__":
    main()
