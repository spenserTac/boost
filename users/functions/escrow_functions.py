import requests
import random
import string

from Crypto.Cipher import AES

# Creators "welcome" URL redirect >>> https://www.escrow-sandbox.com/agree?tid=<tid>&token=<token>


letters = string.ascii_lowercase

def encrypt_token(token):
    result_str = ''.join(random.choice(letters) for i in range(12))

    obj=AES.new('s72heb4762vaopl587ebzutb5091tzi3', AES.MODE_ECB)
    token2 = token + result_str
    encrypted_token = obj.encrypt(token2)

    return encrypted_token

def cipher_token(encrypted_token):
    obj=AES.new('s72heb4762vaopl587ebzutb5091tzi3', AES.MODE_ECB)
    i = obj.decrypt(encrypted_token).decode("utf-8")
    ciphered_token = i[0:36]

    return ciphered_token

def encrypt_id(id):
    result_str = ''.join(random.choice(letters) for i in range(41))

    obj=AES.new('vo1a4tujo17hjzg2folizy6denz98lcs', AES.MODE_ECB)
    id2 = str(id) + result_str
    encrypted_id = obj.encrypt(id2)

    return encrypted_id

def cipher_id(encrypted_id):
    obj=AES.new('vo1a4tujo17hjzg2folizy6denz98lcs', AES.MODE_ECB)
    i = obj.decrypt(encrypted_id).decode("utf-8")
    ciphered_id = i[0:7]

    return ciphered_id




#
#   Encypting and ciphering Token and ID TEST
#

'''

letters = string.ascii_lowercase
message = '2d2afb9f-364f-4f9f-82a5-803344d60432'#.join(random.choice(letters) for i in range(36))
print('\n\n\n\n\n')
print('MESSAGE: ', message, '\n')

#print(len(message))

m = encrypt_token(message)
print('ENCRYPTED TOKEN: ', m)
print('\nCIPHERED TOKEN: ', cipher_token(m))
print('\n-----------------------')
print(message)
print(cipher_token(m))
print('-----------------------\n')

print('===================================================')

message2 = '3300003'#.join(random.choice(letters) for i in range(36))
print('MESSAGE: ', message2, '\n')

#print(len(message2))

m2 = encrypt_id(message2)
print('ENCRYPTED ID: ', m2)
print('\nCIPHERED ID: ', cipher_id(m2))
print('\n-----------------------')
print(message2)
print(cipher_id(m2))
print('-----------------------\n')
print('\n\n\n\n\n')

'''

# returns json response. It will contain: sponsor LANDING PAGE, ID, TOKEN
def escrow_sponsor_pays(creator_email, sponsor_email, amount, creator_listing_name):
    print("\n\nsssssssssssssssssssssssssssupppppppppppppppppppppppppp\n\n")
    r = requests.post(

        'https://api.escrow-sandbox.com/integration/pay/2018-03-31',
        auth=('spenserdt@gmail.com', 'Greatdain445'),


        json={
            "parties": [
                {
                    "role": "broker",
                    "customer": "me",
                    "agreed": True
                },
                {
                    "role": "buyer",
                    "customer": sponsor_email,
                    "agreed": True
                },
                {
                    "role": "seller",
                    "customer": creator_email,
                    "agreed": True
                }
            ],
            "currency": "usd",
            "description": "This is desc. 1",
            "items": [
                {
                    "title": "The escrow order of listing ???",
                    "description": "You'll find the URL in the dashboard.",
                    "type": "milestone",
                    "inspection_period": 259200,
                    "quantity": 1,
                    "schedule": [
                        {
                            "amount": amount,
                            "payer_customer": sponsor_email,
                            "beneficiary_customer": creator_email
                        }
                    ]
                },
                {
                    "type": "broker_fee",
                    "schedule": [
                        {
                            "amount": "10",
                            "payer_customer": sponsor_email,
                            "beneficiary_customer": "me"
                        }
                    ]
                },
                {
                    "type": "broker_fee",
                    "schedule": [
                        {
                            "amount": 0,
                            "payer_customer": creator_email,
                            "beneficiary_customer": "me"
                        }
                    ]
                }
            ]
        },
    )

    return r.json()


def escrow_creator_pays(creator_email, sponsor_email, amount, creator_listing_name):
    r = requests.post(

        'https://api.escrow-sandbox.com/integration/pay/2018-03-31',
        auth=('spenserdt@gmail.com', 'Greatdain445'),


        json={
            "parties": [
                {
                    "role": "broker",
                    "customer": "me",
                    "agreed": True
                },
                {
                    "role": "buyer",
                    "customer": sponsor_email,
                    "agreed": True
                },
                {
                    "role": "seller",
                    "customer": creator_email,
                    "agreed": True
                }
            ],
            "currency": "usd",
            "description": "This is desc. 1",
            "items": [
                {
                    "title": "The escrow order of listing ???",
                    "description": "You'll find the URL in the dashboard.",
                    "type": "milestone",
                    "inspection_period": 259200,
                    "quantity": 1,
                    "schedule": [
                        {
                            "amount": amount,
                            "payer_customer": sponsor_email,
                            "beneficiary_customer": creator_email
                        }
                    ]
                },
                {
                    "type": "broker_fee",
                    "schedule": [
                        {
                            "amount": "10",
                            "payer_customer": creator_email,
                            "beneficiary_customer": "me"
                        }
                    ]
                },
                {
                    "type": "broker_fee",
                    "schedule": [
                        {
                            "amount": 0,
                            "payer_customer": sponsor_email,
                            "beneficiary_customer": "me"
                        }
                    ]
                }
            ]
        },
    )

    return r.json()


'''
r = requests.post(

    'https://api.escrow-sandbox.com/integration/pay/2018-03-31',
    auth=('spenserdt@gmail.com', 'Greatdain445'),


    json={
        "parties": [
            {
                "role": "broker",
                "customer": "me",
                "agreed": True
            },
            {
                "role": "buyer",
                "customer": "spenserdaintacin@gmail.com",
                "agreed": True
            },
            {
                "role": "seller",
                "customer": "getmodernkitchen@gmail.com",
                "agreed": True
            }
        ],
        "currency": "usd",
        "description": "This is desc. 1",
        "items": [
            {
                "title": "This is title 1",
                "description": "This is desc. 2",
                "type": "milestone",
                "inspection_period": 259200,
                "quantity": 1,
                "schedule": [
                    {
                        "amount": 1000.0,
                        "payer_customer": "spenserdaintacin@gmail.com",
                        "beneficiary_customer": "getmodernkitchen@gmail.com"
                    }
                ]
            },
            {
                "type": "broker_fee",
                "schedule": [
                    {
                        "amount": 100,
                        "payer_customer": "spenserdaintacin@gmail.com",
                        "beneficiary_customer": "me"
                    }
                ]
            },
            {
                "type": "broker_fee",
                "schedule": [
                    {
                        "amount": 0,
                        "payer_customer": "getmodernkitchen@gmail.com",
                        "beneficiary_customer": "me"
                    }
                ]
            }
        ]
    },
)
'''
