# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 10:35:02 2018

@author: yuta_liu
"""

import ecdsa

sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1) # 用比特幣使用的加密演算法產生私鑰
vk = sk.get_verifying_key() # 用私鑰產生公鑰

print(sk.to_pem())
"""
把私鑰印出來會類似這樣，真正的使用場景中絕對不要這樣印出來放到網頁上
-----BEGIN EC PRIVATE KEY-----
MHQCAQEEIGqXRqNjZns1TJ1CfayizUPcpZop00KWWj0+fOy/WwqtoAcGBSuBBAAK
oUQDQgAEZUBDWMgG3dTAzKcvMbw1IkJiLbtFq/AyLIMsKpz2v2mc3e3QJUM/scUR
MzoXPDSPftfU2CT6f4K0saWZsstAWg==
-----END EC PRIVATE KEY-----
"""

print(vk.to_pem())
"""
公鑰拿給別人來驗證簽名是不是你的
-----BEGIN PUBLIC KEY-----
MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEZUBDWMgG3dTAzKcvMbw1IkJiLbtFq/Ay
LIMsKpz2v2mc3e3QJUM/scURMzoXPDSPftfU2CT6f4K0saWZsstAWg==
-----END PUBLIC KEY-----
"""

transaction1 = vk.to_pem() + b'dummyTest' # 這裡先隨便塞data當作上一個transaction
                                          # 注意onwer1的公鑰也要加入

sk2 = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1) # owner2的私鑰 
vk2 = sk2.get_verifying_key() # 用私鑰產生公鑰

sig = sk.sign(transaction1 + vk2.to_pem()) # 用上個transaction的內容與owner2的公鑰以owner1的私鑰進行簽名
                                         
print(sig)
"""
簽名也是產生一段很長的字串，隨資料一起傳送
'04a3674e4f2027aedf91c7d5fd9786f4c9889579d197a38c50e1b8e6e883aa49fbb3f0712d01af10b7d86ef5b5591c23476a497fe80141c957106fca040d9719'

"""

vk.verify(sig, transaction1 + vk2.to_pem()) # 最後用公鑰和簽名來驗證資料是不是有被竄改