import requests
import random
import string

#from Crypto.Cipher import AES

# Creators URL redirect >>> https://my.escrow.com/myEscrow/Transaction.asp?tid=<transaction_id> (Only after the sponsor has completed the stuff)
# Sponsor URL redirect >>> "https://www.escrow.com/pay?token=<token>"

# https://my.escrow-sandbox.com/myescrow/Transaction.asp?TID=3564176
# Buyer transaction page >>>  https://my.escrow-sandbox.com/myescrow/Transaction.asp?tran=3565394

# https://my.escrow-sandbox.com/myescrow/Transaction.asp?TID=<transaction_id>

# get transaction details (assign it to a variable then print var.json()) >>> requests.get('https://api.escrow-sandbox.com/2017-09-01/transaction/3564176',auth=('spenserdt@gmail.com', 'Greatdain445'))


'''


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


'''

#
#   Encypting and ciphering Token and ID TEST
#


# returns json response. It will contain: sponsor LANDING PAGE, ID, TOKEN
# escrow: 14490_8NV4AibVVPvovHAT3ZbUaZMEv5iCfVNTEBmVs0urmI2mxwzOmYq25GFnA2bl1UQn
# escrow-sandbox: 1903_654mQOuPbybvpQ7ZMtoPlWFqXrb76mBKKVUQWyqpUUgAphioq9ZbtRlpyipDqsCO
def escrow_sponsor_pays(creator_email, sponsor_email, amount, creator_listing_name, sponsor_listing_name):

    fee = str(0.10 * float(amount))

    r = requests.post(

    'https://api.escrow.com/integration/pay/2018-03-31',
    auth=('admin@getboostplatform.com', '14490_8NV4AibVVPvovHAT3ZbUaZMEv5iCfVNTEBmVs0urmI2mxwzOmYq25GFnA2bl1UQn'),


    json={
        "parties": [
            {
                "role": "broker",
                "customer": "me",
                "agreed": True
            },
            {
                "role": "buyer",
                "customer": "sponsor@gmail.com",
                "agreed": True,

            },
            {
                "role": "seller",
                "customer": creator_email,
                "agreed": True,
                "visibility": {
                    "hidden_from": ["sponsor@gmail.com"]
                }
            }
        ],
        "currency": "usd",
        # This is actially the title (only seen on the description page at the bottom, not that important)
        #  Make it somthing like SPONSOR LISTING: <sponsor_listing> | CREATOR LISTING <creator_listing>
        "description": "SPONSOR LISTING: {sponsor_listing} | CREATOR LISTING {creator_listing}".format(sponsor_listing=sponsor_listing_name, creator_listing=creator_listing_name),
        "items": [
            {
                # The title and description are shown in the card payemnt and with the total (at the top of detail page)
                # Title should be solid yet short description of transaction.
                # desciption should give instructions for URL stuff.
                "title": "Boost Sponsored Escrow Order",
                "description": "Thank You For Using Boost.",
                "type": "milestone",
                "inspection_period": 86400,
                "quantity": 1,
                "schedule": [
                    {
                        "amount": amount,
                        "payer_customer": "sponsor@gmail.com",
                        "beneficiary_customer": creator_email
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
                ],
                "visibility": {
                    "hidden_from": ["sponsor@gmail.com"]
                }
            },
            {
                "type": "broker_fee",
                "schedule": [
                    {
                        "amount": fee,
                        "payer_customer": "sponsor@gmail.com",
                        "beneficiary_customer": "me"

                    }
                ],
                "visibility": {
                    "hidden_from": ["sponsor@gmail.com"]
                }
            }
        ]
    },
    )

    return r.json()


def escrow_creator_pays(creator_email, sponsor_email, amount, creator_listing_name, sponsor_listing_name):

    fee = str(0.10 * float(amount))

    r = requests.post(

    'https://api.escrow.com/integration/pay/2018-03-31',
    auth=('admin@getboostplatform.com', '14490_8NV4AibVVPvovHAT3ZbUaZMEv5iCfVNTEBmVs0urmI2mxwzOmYq25GFnA2bl1UQn'),


    json={
        "parties": [
            {
                "role": "broker",
                "customer": "me",
                "agreed": True
            },
            {
                "role": "buyer",
                "customer": "sponsor@gmail.com",
                "agreed": True,

            },
            {
                "role": "seller",
                "customer": creator_email,
                "agreed": True,
                "visibility": {
                    "hidden_from": ["sponsor@gmail.com"]
                }
            }
        ],
        "currency": "usd",
        # This is actially the title (only seen on the description page at the bottom, not that important)
        #  Make it somthing like SPONSOR LISTING: <sponsor_listing> | CREATOR LISTING <creator_listing>
        "description": "SPONSOR LISTING: {sponsor_listing} | CREATOR LISTING {creator_listing}".format(sponsor_listing=sponsor_listing_name, creator_listing=creator_listing_name),
        "items": [
            {
                # The title and description are shown in the card payemnt and with the total (at the top of detail page)
                # Title should be solid yet short description of transaction.
                # desciption should give instructions for URL stuff.
                "title": "Boost Sponsored Escrow Order",
                "description": "Thank You For Using Boost.",
                "type": "milestone",
                "inspection_period": 86400,
                "quantity": 1,
                "schedule": [
                    {
                        "amount": amount,
                        "payer_customer": "sponsor@gmail.com",
                        "beneficiary_customer": creator_email
                    }
                ]
            },
            {
                "type": "broker_fee",
                "schedule": [
                    {
                        "amount": fee,
                        "payer_customer": creator_email,
                        "beneficiary_customer": "me"

                    }
                ],
                "visibility": {
                    "hidden_from": ["sponsor@gmail.com"]
                }
            },
            {
                "type": "broker_fee",
                "schedule": [
                    {
                        "amount": 0,
                        "payer_customer": "sponsor@gmail.com",
                        "beneficiary_customer": "me"

                    }
                ],
                "visibility": {
                    "hidden_from": ["sponsor@gmail.com"]
                }
            }
        ]
    },
    )

    return r.json()
