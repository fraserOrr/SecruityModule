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

def KeyGeneration():
    
    
    AlphabetString = string.ascii_lowercase[:26]
    KeyContent = []
    for ch in AlphabetString:
        KeyContent.append(ch)
    #output= np.array(np.meshgrid(KeyContent,KeyContent,KeyContent,KeyContent)).T.reshape(-1,4)
    output= np.array(np.meshgrid(KeyContent,KeyContent)).T.reshape(-1,2)
    return(output)
    #print(KeyContent)
def convert_to_bytes(s):
        return bytes([ord(c) for c in s])

def BruteForce():
    import re
    ciphertext = inputfile.read() #Read the ciphertext as a string from the inputfile
    output_plaintext = []
   
    
    output_ciphertext = []
    for Key in KeyGeneration():
        s = ""
        result = ""
        output = ""
        for i in Key:
            s+=str(i)
            

        key = convert_to_bytes(s)
        keystream = streamcipher(key)
        output_plaintext[:] = []    
        for c in bytes.fromhex(ciphertext): #Convert the ciphertext hex string into a sequence of integers (https://docs.python.org/3/library/stdtypes.html#bytes.fromhex)
            output_plaintext.append(chr(c ^ next(keystream))) #XOR each ciphertext integer c with the next integer from the keystream to decrypt it. Turn the resulting integer to a character.
        #output = ''.join(output_plaintext)
        for j in output_plaintext:
            output+=str(j)
        output2 = re.sub(r' ', '', output)
        #
        #print("\n"+ s + "\n" + result)
        #print(output)
        if isEnglish(output2) == True:
            print("\n"+ s + "\n" + output)


def isEnglish(s):
    try:
        s.decode('ascii')
    except UnicodeDecodeError:
        return(False)
    else:
        return(True)


if __name__ == '__main__':
    import sys
    import numpy as np
    import string
    if sys.argv[1] == 'd':
        with open(sys.argv[2], 'r') as inputfile:

            BruteForce()
    else:
        print("Incorrect Argument")

    
