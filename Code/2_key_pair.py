pip install pycrypto

from Crypto.Util import number
import math
import random

'''calculates the modular inverse from e and phi'''
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

'''
calculates the gcd of two ints
'''
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


''' generate prime number of 1024 bits'''
def generateRandomPrim(k):
    return number.getPrime(k,randfunc= None)

#Key Generation
def generate_keyPairs(k):
    p = generateRandomPrim(k)
    q = generateRandomPrim(k)
    
    #Key component
    n = p*q
    print("n ",n)
    
    
    phi = (p-1) * (q-1) 
    print("phi ",phi)
    
    '''choose e coprime to n and 1 > e > phi'''    
    e = random.randint(1, phi)
    g = gcd(e,phi)
    while g != 1:
        e = random.randint(1, phi)
        g = gcd(e, phi)
        
    print("e=",e," ","phi=",phi)
    
    
    '''modular inverse of e and phi'''
    d = egcd(e, phi)[1]
    
    '''make sure d is positive'''
    d = d % phi
    if(d < 0):
        d += phi
        
    return (e,d,n)

def encrypt(text,public_key,n):
    key = public_key
    ctext = [pow(ord(char),key,n) for char in text]
    return ctext

def decrypt(ctext,private_key,n):
  key = private_key
  text = [chr(pow(char,key,n)) for char in ctext]
  return "".join(text)

small_pair = generate_keyPairs(8)
large_pair = generate_keyPairs(128)

#SENDER SIDE 


text = "Meet me soon"

#generate Cipher text
S1 = encrypt(text,small_pair[0],small_pair[2])

#Encrypt the small key component
X = pow(small_pair[2],large_pair[0],large_pair[2])
small_pair = list(small_pair)
small_pair[2] = X
small_pair = tuple(small_pair)


#RECEIVER SIDE recieves the cipher text and encrypted small key component

#Decrypt the small key component
S3 = pow(small_pair[2],large_pair[1],large_pair[2])
small_pair = list(small_pair)
small_pair[2] = S3
small_pair = tuple(small_pair)

#Decrypt the cipher text with original small key pair
plain_text = decrypt(S1,small_pair[1],small_pair[2])

print("The message sent was:",plain_text)

