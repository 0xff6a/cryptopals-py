import gmpy2 as gmp
import os

from utils import Buffer
from Crypto.Hash import SHA256
from gmpy2 import mpz

class KeyPair(object):
    """Diffie-Hellman public/private key pair"""
    RANDOM_BITS = 128
    G_NIST = mpz('2', 16)
    P_NIST = mpz(
        'ffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024'
        'e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd'
        '3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec'
        '6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f'
        '24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361'
        'c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552'
        'bb9ed529077096966d670c354e4abc9804f1746c08ca237327fff'
        'fffffffffffff', 16
    )

    def __init__(self, p=P_NIST, g=G_NIST):
        """ Generate the key pair based on the DH p and g parameters"""
        dh_a = self.__random_int(p)
        dh_A = gmp.powmod(g, dh_a, p)

        self.__dh_p = p
        self.__dh_g = g
        self.__secret_key = dh_a
        self.__public_key = dh_A

    def get_public(self):
        """Return the public key as a Buffer instance"""
        return Buffer.from_mpz(self.__public_key)

    def get_secret(self):
        """Return the private key as a Buffer instance"""
        return Buffer.from_mpz(self.__secret_key)

    def session_key(self, public_B):
        """Generate a session secret given the other party's public key"""
        raw_secret = gmp.powmod(
            public_B.to_mpz(),
            self.__secret_key,
            self.__dh_p
        )

        # Hash the secret to create a key
        h_256 = SHA256.new()
        h_256.update(raw_secret.digits(10))
        raw_key = h_256.digest()

        return Buffer(raw_key)

    def __random_int(self, modulo):
        """Generate a random number modulo the supplied argument"""
        r_seed = int(os.urandom(32).encode('hex'), 16)
        r_state = gmp.random_state(r_seed)
        raw = gmp.mpz_urandomb(r_state, self.RANDOM_BITS)

        return gmp.t_mod(raw, modulo)
