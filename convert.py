from Crypto.Hash import keccak
k = keccak.new(digest_bits=256)
k.update(1000)

print (k.hexdigest())

print ((k.hexdigest()[24:64]).zfill(64))


