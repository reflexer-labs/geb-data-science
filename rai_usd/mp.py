from web3 import Web3, HTTPProvider
from retry import retry
from multiprocessing import Queue, Process

@retry(exceptions=Exception, tries=-1, delay=1, max_delay=None, backoff=1, jitter=0)
def fetch_link_mp(contract, abi, eth_rpc_url, block_numbers, q):
    """

    Parameters
    ----------
    eth_rpc_url : str
        ethereum rpc url
    block_numbers : iterable[int]
        Block numbers to fetch base_fee for
    q : multiprocessing.Queue
        Queue to put results on
    """
    w3 = Web3(Web3.HTTPProvider(eth_rpc_url, request_kwargs={"timeout": 10}))
    link = w3.eth.contract(address=contract, abi=abi)
    results = []

    for n in block_numbers:
        try:
            round_id, price, started_at, timestamp, answer_in_round = link.caller(block_identifier=n).latestRoundData()
        except Exception as e:
            print(e)
            continue

        results.append((n, price, timestamp, started_at))

    q.put(results)
    
#@retry(exceptions=Exception, tries=-1, delay=1, max_delay=None, backoff=1, jitter=0)
def fetch_rp(contract, abi, eth_rpc_url, block_numbers, q):
    """

    Parameters
    ----------
    eth_rpc_url : str
        ethereum rpc url
    block_numbers : iterable[int]
        Block numbers to fetch base_fee for
    q : multiprocessing.Queue
        Queue to put results on
    """
    w3 = Web3(Web3.HTTPProvider(eth_rpc_url, request_kwargs={"timeout": 10}))
    oracle_relayer = w3.eth.contract(address=contract, abi=abi)
    results = []

    for n in block_numbers:
        try:
            rp = oracle_relayer.caller(block_identifier=n).redemptionPrice()
        except Exception as e:
            print(e)
            continue

        results.append((n, rp))

    q.put(results)
  
def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def build_procs(f, q, blocks, n_jobs, contract, abi, eth_rpc_url):
    procs = []

    chunks = split(blocks, n_jobs)
    for chunk in chunks:
        p = Process(target=f, args=(contract, abi, eth_rpc_url, chunk, q))
        procs.append(p)

    return procs

def fetch(f, n_jobs, contract, abi, eth_rpc_url, start_block=None, stop_block=None, blocks=None):
    if (blocks and start_block) or (blocks and stop_block) or (not blocks and not start_block):
        raise ValueError("Pass `blocks` or `start_block` and `stop_block`. Not both")

    if start_block:
        blocks = list(range(start_block, stop_block +1))

    results = []
    q = Queue()

    n_blocks = len(blocks)
    assert n_blocks > 0
    chunks = split(blocks, n_jobs)

    procs = build_procs(f, q, blocks, n_jobs, contract, abi, eth_rpc_url)
    for p in procs:
        p.start()

    for p in procs:
        proc_results = q.get()
        for r in proc_results:
            results.append(r)

    for p in procs:
        p.join()

    return sorted(results, key=lambda x: x[0])
