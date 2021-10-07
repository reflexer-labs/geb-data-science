import requests
import json
import pandas as pd

SAVIOUR_ADDRESS = '0xA9402De5ce3F1E03Be28871b914F77A4dd5e4364'
SAVIOUR_ABI = '[{"inputs":[{"internalType":"bool","name":"isSystemCoinToken0_","type":"bool"},{"internalType":"address","name":"coinJoin_","type":"address"},{"internalType":"address","name":"collateralJoin_","type":"address"},{"internalType":"address","name":"cRatioSetter_","type":"address"},{"internalType":"address","name":"systemCoinOrcl_","type":"address"},{"internalType":"address","name":"liquidationEngine_","type":"address"},{"internalType":"address","name":"taxCollector_","type":"address"},{"internalType":"address","name":"oracleRelayer_","type":"address"},{"internalType":"address","name":"safeManager_","type":"address"},{"internalType":"address","name":"saviourRegistry_","type":"address"},{"internalType":"address","name":"liquidityManager_","type":"address"},{"internalType":"address","name":"lpToken_","type":"address"},{"internalType":"uint256","name":"minKeeperPayoutValue_","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"AddAuthorization","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"usr","type":"address"}],"name":"AllowUser","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"caller","type":"address"},{"indexed":true,"internalType":"address","name":"safeHandler","type":"address"},{"indexed":false,"internalType":"uint256","name":"lpTokenAmount","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"usr","type":"address"}],"name":"DisallowUser","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"caller","type":"address"},{"indexed":true,"internalType":"address","name":"safeHandler","type":"address"},{"indexed":false,"internalType":"uint256","name":"systemCoinAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"collateralAmount","type":"uint256"},{"indexed":false,"internalType":"address","name":"dst","type":"address"}],"name":"GetReserves","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"parameter","type":"bytes32"},{"indexed":false,"internalType":"uint256","name":"val","type":"uint256"}],"name":"ModifyParameters","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"parameter","type":"bytes32"},{"indexed":false,"internalType":"address","name":"data","type":"address"}],"name":"ModifyParameters","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"RemoveAuthorization","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"keeper","type":"address"},{"indexed":true,"internalType":"bytes32","name":"collateralType","type":"bytes32"},{"indexed":true,"internalType":"address","name":"safeHandler","type":"address"},{"indexed":false,"internalType":"uint256","name":"collateralAddedOrDebtRepaid","type":"uint256"}],"name":"SaveSAFE","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"caller","type":"address"},{"indexed":true,"internalType":"address","name":"safeHandler","type":"address"},{"indexed":false,"internalType":"address","name":"dst","type":"address"},{"indexed":false,"internalType":"uint256","name":"lpTokenAmount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"HUNDRED","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MAX_UINT","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"ONE","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"RAY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"THOUSAND","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"WAD","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"WAD_COMPLEMENT","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"addAuthorization","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"usr","type":"address"}],"name":"allowUser","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"allowedUsers","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"authorizedAccounts","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"cRatioSetter","outputs":[{"internalType":"contract SaviourCRatioSetterLike","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"},{"internalType":"address","name":"safeHandler","type":"address"}],"name":"canSave","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"coinJoin","outputs":[{"internalType":"contract CoinJoinLike","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"collateralJoin","outputs":[{"internalType":"contract CollateralJoinLike","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"collateralToken","outputs":[{"internalType":"contract ERC20Like","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"collateralType","type":"bytes32"},{"internalType":"uint256","name":"targetDebtAmount","type":"uint256"}],"name":"debtBelowFloor","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"safeID","type":"uint256"},{"internalType":"uint256","name":"lpTokenAmount","type":"uint256"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"usr","type":"address"}],"name":"disallowUser","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"collateralType","type":"bytes32"}],"name":"getAccumulatedRate","outputs":[{"internalType":"uint256","name":"accumulatedRate","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getCollateralPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"safeHandler","type":"address"},{"internalType":"uint256","name":"redemptionPrice","type":"uint256"},{"internalType":"uint256","name":"safeDebtRepaid","type":"uint256"},{"internalType":"uint256","name":"safeCollateralAdded","type":"uint256"}],"name":"getKeeperPayoutTokens","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getKeeperPayoutValue","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"safeHandler","type":"address"}],"name":"getLPUnderlying","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"safeID","type":"uint256"},{"internalType":"address","name":"dst","type":"address"}],"name":"getReserves","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getSystemCoinMarketPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"safeHandler","type":"address"}],"name":"getTargetCRatio","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"safeHandler","type":"address"},{"internalType":"uint256","name":"redemptionPrice","type":"uint256"}],"name":"getTokensForSaving","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"isSystemCoinToken0","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"keeperPayout","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"keeperPayoutExceedsMinValue","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"liquidationEngine","outputs":[{"internalType":"contract LiquidationEngineLike_3","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"liquidityManager","outputs":[{"internalType":"contract UniswapLiquidityManagerLike","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"lpToken","outputs":[{"internalType":"contract ERC20Like","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"lpTokenCover","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"minKeeperPayoutValue","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"parameter","type":"bytes32"},{"internalType":"address","name":"data","type":"address"}],"name":"modifyParameters","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"parameter","type":"bytes32"},{"internalType":"uint256","name":"val","type":"uint256"}],"name":"modifyParameters","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"oracleRelayer","outputs":[{"internalType":"contract OracleRelayerLike_2","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"payoutToSAFESize","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"removeAuthorization","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"restrictUsage","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"safeEngine","outputs":[{"internalType":"contract SAFEEngineLike_8","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"safeManager","outputs":[{"internalType":"contract GebSafeManagerLike","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"keeper","type":"address"},{"internalType":"bytes32","name":"collateralType","type":"bytes32"},{"internalType":"address","name":"safeHandler","type":"address"}],"name":"saveSAFE","outputs":[{"internalType":"bool","name":"","type":"bool"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"saviourRegistry","outputs":[{"internalType":"contract SAFESaviourRegistryLike","name":"","type":"address"}],"stateMfutability":"view","type":"function"},{"inputs":[],"name":"systemCoin","outputs":[{"internalType":"contract ERC20Like","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"systemCoinOrcl","outputs":[{"internalType":"contract PriceFeedLike","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"taxCollector","outputs":[{"internalType":"contract TaxCollectorLike","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"},{"internalType":"address","name":"safeHandler","type":"address"}],"name":"tokenAmountUsedToSave","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"underlyingReserves","outputs":[{"internalType":"uint256","name":"systemCoins","type":"uint256"},{"internalType":"uint256","name":"collateralCoins","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"safeID","type":"uint256"},{"internalType":"uint256","name":"lpTokenAmount","type":"uint256"},{"internalType":"address","name":"dst","type":"address"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]'

def fetch_saviour_targets(web3, saviour_safes):
    saviour_contract = web3.eth.contract(address=SAVIOUR_ADDRESS, abi=SAVIOUR_ABI)
    
    cratios = []
    syscoins = []
    collaterals = []
    for handler in saviour_safes['safeHandler']:
        handler = web3.toChecksumAddress(handler)
        cratio = saviour_contract.functions.getTargetCRatio(handler).call()
        syscoin, collateral = saviour_contract.functions.getLPUnderlying(handler).call()
        syscoin /= 1E18
        collateral /= 1E18
        
        cratios.append(cratio)
        syscoins.append(syscoin)
        collaterals.append(collateral)
    
    saviour_safes['target_cratio'] = cratios
    saviour_safes['lp_syscoin'] = syscoins
    saviour_safes['lp_collateral'] = collaterals
    
    return saviour_safes
       
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
        print(json.loads(r.content)['data'])
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