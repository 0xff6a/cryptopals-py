import gmpy2 as GMP

from utils import Buffer
from Crypto.Hash import SHA256

class KeyPair(object):
    """Diffie-Hellman public/private key pair"""
    RANDOM_BITS = 128

    def __init__(self, p, g):
        """ Generate the key pair based on the DH p and g parameters"""
        dh_a = self.__random_int(p)
        dh_A = GMP.powmod(g, dh_a, p)

        self.__dh_p = p
        self.__dh_g = g
        self.__secret_key = dh_a
        self.__public_key = dh_A

    def get_public(self):
        """Return the public key as a Buffer instance"""
        return Buffer(self.__public_key.digits(10))

    def get_secret(self):
        """Return the private key as a Buffer instance"""
        return Buffer(self.__secret_key.digits(10))

    def session_key(self, public_B):
        """Generate a session secret given the other party's public key"""
        raw_secret = GMP.powmod(public_B, self.__secret_key, self.__dh_p)

        # Hash the secret to create a key
        h_256 = SHA256.new()
        h_256.update(raw_secret.digits(10))
        raw_key = h_256.digest()

        return Buffer(raw_key)

    def __random_int(self, modulo):
        """Generate a random number modulo the supplied argument"""
        r_state = GMP.random_state()
        raw = GMP.mpz_urandomb(r_state, self.RANDOM_BITS)

        return GMP.t_mod(raw, modulo)
