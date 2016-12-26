#!/usr/bin/env python
# Create a bitcoin multisignature paper wallet with variable m-of-n settings..
from bitcoin import *

priv = []
wif = []
pub = []

#print '>>>Generating', rankeys, 'random keys..'
priv.append(random_key())
wif.append(encode_privkey(priv[0],'wif'))
pub.append(privtopub(priv[0]))

print scriptaddr(mk_multisig_script(pub, 1, 1))
print wif[0]
