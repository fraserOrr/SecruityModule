#python cipher.py e key.txt plaintext.txt 
#python cipher.py d key.txt ciphertext.txt 

def KSA(key):
    keylength = len(key)

    S = list(range(256))

    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % keylength]) % 256
        S[i], S[j] = S[j], S[i]  # swap

    return S

    
def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]  # swap

        K = S[(S[i] + S[j]) % 256]
        yield K


def streamcipher(key):
    S = KSA(key)
    #print(S)
    return PRGA(S)


if __name__ == '__main__':
    import sys

    def convert_to_bytes(s):
        return bytes([ord(c) for c in s])

    with open(sys.argv[2], 'r') as keyfile:
        key = convert_to_bytes(keyfile.read())

    #print(key)
    keystream = streamcipher(key)

    with open(sys.argv[3], 'r') as inputfile:
        if sys.argv[1] == 'e':  #encryption
            plaintext = inputfile.read() #Read the plaintext as a string from the inputfile
            output_ciphertext = []
            for c in plaintext:
                output_ciphertext.append(ord(c) ^ next(keystream)) #Turn each character from the plaintext string to an integer. XOR it with the next integer from the keystream to encrypt it.
            print(bytes(output_ciphertext).hex(), file=sys.stdout, end='') #Replace sys.stdout if you want to write output to a file
        elif sys.argv[1] == 'd': #decryption           
            ciphertext = inputfile.read() #Read the ciphertext as a string from the inputfile
            output_plaintext = []
            for c in bytes.fromhex(ciphertext): #Convert the ciphertext hex string into a sequence of integers (https://docs.python.org/3/library/stdtypes.html#bytes.fromhex)
                output_plaintext.append(chr(c ^ next(keystream))) #XOR each ciphertext integer c with the next integer from the keystream to decrypt it. Turn the resulting integer to a character.
            print(''.join(output_plaintext), file=sys.stdout, end='') #Replace sys.stdout if you want to write output to a file
        else:
            print("Unknown opcode. Opcode should be 'e' for encryption or 'd' for decryption.", file=sys.stderr)