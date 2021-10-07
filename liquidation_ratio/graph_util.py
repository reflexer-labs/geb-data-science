import requests
import json
import pandas as pd

def fetch_safes(url):

    query = '''
    query {{
        safes(first: 1000, skip:{}) {{
            safeId
            collateral
            debt
        }}
    }}'''

    n = 0
    safes = []
    while True:
        r = requests.post(url, json = {'query':query.format(n*1000)})
        s = json.loads(r.content)['data']['safes']
        safes.extend(s)
        n += 1
        if len(s) < 1000:
            break
    safes = pd.DataFrame(safes)
    safes['collateral'] = safes['collateral'].astype(float)
    safes['debt'] = safes['debt'].astype(float)
    #safes['safeId'] = safes['safeId'].astype(int)

    return safes

def fetch_rp(url):

    query =  '''
    query {
        systemState(id:"current") {
        currentRedemptionPrice {
            value }
        }
    }'''
    r = requests.post(url, json = {'query':query})
    s = json.loads(r.content)['data']['systemState']['currentRedemptionPrice']['value']

    return float(s)

def fetch_debt_ceiling(url):

    query =  '''
    query {
        collateralType(id:"ETH-A") {
        debtCeiling
        }
    }'''
    r = requests.post(url, json = {'query':query})
    s = json.loads(r.content)['data']['collateralType']['debtCeiling']

    return float(s)


def fetch_saviour_safes(url):

    query = '''
    query {{
        safeSaviours(first: 1000, skip:{}) {{
            safes {{
            safeId
            safeHandler
            collateral
            debt            
            }}
        }}
    }}'''

    n = 0
    safes = []
    while True:
        r = requests.post(url, json = {'query':query.format(n*1000)})
        #print(json.loads(r.content)['data'])
        saviours = json.loads(r.content)['data']['safeSaviours']
        for s in saviours:
            safes.extend(s['safes'])
        n += 1
        if len(s) < 1000:
            break
    safes = pd.DataFrame(safes)
    safes['collateral'] = safes['collateral'].astype(float)
    safes['debt'] = safes['debt'].astype(float)
    #safes['safeId'] = safes['safeId'].astype(int)

    return safes