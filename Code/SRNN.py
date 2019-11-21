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
def generateRandomPrim():
    return number.getPrime(128,randfunc= None)



def encrypt(text,public_key):
  
    n,e,u_a = public_key
    ctext = [pow(ord(char)*u_a,e,n) for char in text]
    return ctext

def decrypt(ctext,private_key,ut):
  d,a,u = private_key
  pminusa,e,n = ut
  v = power(u,pminusa,n)
  text = [chr( (power(v,e*d,n)*power(char,d,n))%n)  for char in ctext]
  return "".join(text)

#Key Generation
def generate_keyPairs():
    p = generateRandomPrim()
    q = generateRandomPrim()
    
    n = p*q
    print("n ",n)
    '''phi(n) = phi(p)*phi(q)'''
    phi = (p-1) * (q-1) 
    print("phi ",phi)
    
    '''choose e coprime to n and 1 > e > phi'''    
    e = random.randint(1, phi)
    g = gcd(e,phi)
    while g != 1:
        e = random.randint(1, phi)
        g = gcd(e, phi)
        
    print("e=",e," ","phi=",phi)
    '''d[1] = modular inverse of e and phi'''
    d = egcd(e, phi)[1]
    
    '''make sure d is positive'''
    d = d % phi
    if(d < 0):
        d += phi
        
    '''pick u such that u<phi-1'''
    u = random.randint(1,5)
    
    '''pick a such that u<a<phi'''
    a = random.randint(u+1,u**2)
    
    '''compute u^a'''
    u_a = u**a
    
    '''
    public key = (n,e,u^a)
    private key = (d,a,u)
    '''
    return ((n,e,u_a),(d,a,u),((phi-a),e,n))


def power(x, y, p) : 
    res = 1     # Initialize result 
  
    # Update x if it is more 
    # than or equal to p 
    x = x % p  
  
    while (y > 0) : 
          
        # If y is odd, multiply 
        # x with result 
        if ((y & 1) == 1) : 
            res = (res * x) % p 
  
        # y must be even now 
        y = y >> 1      # y = y/2 
        x = (x * x) % p 
          
    return res



public_key,private_key,ut = generate_keyPairs() 
print("Public: ",public_key)
print("Private: ",private_key)

ctext = encrypt("Hello World",public_key)
print("encrypted  =",ctext)
plaintext = decrypt(ctext, private_key,ut)
print("decrypted =",plaintext)

