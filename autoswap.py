from web3 import Web3
import time
import random
import sys

sys.stdout = open(sys.stdout.fileno(), 'w', buffering=1)

# 注意安全，自行阅读代码或运行前先把代码交给chatgpt/grok等ai检查。
# 运行前请自行评估风险，否则造成任何损失与本脚本无关

# 自定义参数
AMOUNT_ETH = 2.5        # 固定跨链数量跟模板数据强关联，不可修改
TIMES = 10                 # 跨链次数
CROSS_PER_ADDRESS = 3     # 每次跨链尝试次数，因为经常失败建议设置为2-5次

# RPC参数
CHAINS = {
    'uni': {
        'rpc': 'https://unichain-sepolia-rpc.publicnode.com',
        'chain_id': 1301,
        'contract': '0x1cEAb5967E5f078Fa0FEC3DFfD0394Af1fEeBCC9'
    },
    'arb': {
        'rpc': 'https://sepolia-rollup.arbitrum.io/rpc',
        'chain_id': 421614,
        'contract': '0x22B65d0B9b59af4D3Ed59F18b9Ad53f5F4908B54'
    },
    'base': {
        'rpc': 'https://base-sepolia-rpc.publicnode.com',
        'chain_id': 84532,
        'contract': '0xCEE0372632a37Ba4d0499D1E2116eCff3A17d3C3'
    },
    'op': {
        'rpc': 'https://sepolia.optimism.io',
        'chain_id': 11155420,
        'contract': '0xb6Def636914Ae60173d9007E732684a9eEDEF26E'
    }
}

# 链标识映射
CHAIN_IDENTIFIERS = {
    'uni': 'unit',
    'arb': 'arbt',
    'base': 'bast',
    'op': 'opst'
}

# input data 模板数据
BASE_DATA_TEMPLATE = (
    "0x56591d59{target_chain:4s}000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000{address}00000000000000000000000000000000000000000000000022b1677e13a4a73c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000022b1c8c1227a0000"
)

# 初始化
w3_instances = {chain: Web3(Web3.HTTPProvider(config['rpc'])) for chain, config in CHAINS.items()}

# 检测RPC连接
for chain, w3 in w3_instances.items():
    if not w3.is_connected():
        raise Exception(f"连接到 {chain} 失败")

def load_private_keys():
    with open("address.txt", "r") as f:
        return [line.strip() for line in f if line.strip()]

def get_balance(account, chain):
    return w3_instances[chain].eth.get_balance(account.address) / 1e18

def generate_input_data(from_chain, to_chain, address, amount_wei):
    target_chain = CHAIN_IDENTIFIERS[to_chain].encode().hex()
    return BASE_DATA_TEMPLATE.format(
        target_chain=target_chain,
        address=address[2:].lower()
    )

def bridge(from_chain, to_chain, amount_eth, account):
    try:
        w3 = w3_instances[from_chain]
        amount_wei = w3.to_wei(amount_eth, 'ether')
        nonce = w3.eth.get_transaction_count(account.address, 'pending')
        data = generate_input_data(from_chain, to_chain, account.address, amount_wei)
        
        tx = {
            'from': account.address,
            'to': CHAINS[from_chain]['contract'],
            'value': amount_wei,
            'nonce': nonce,
            'gas': 400000,
            'gasPrice': w3.to_wei(0.5, 'gwei'),
            'chainId': CHAINS[from_chain]['chain_id'],
            'data': data
        }
        print(f"{from_chain.upper()} -> {to_chain.upper()}: 从 {account.address} 发出 {amount_eth} 个ETH")
        signed_tx = w3.eth.account.sign_transaction(tx, account.key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"{from_chain.upper()} -> {to_chain.upper()} 跨链发送成功, hash: {w3.to_hex(tx_hash)}")
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=10)
        print(f"链上已确认, 区块号: {tx_receipt.blockNumber}")
        return True
    except Exception as e:
        print(f"{from_chain.upper()} -> {to_chain.upper()} 跨链失败: {e}")
        print(f"跳过失败的跨链，继续处理下一个操作...")
        return False

def check_and_balance_chains(account):
    balances = {chain: get_balance(account, chain) for chain in CHAINS}
    print(f"ETH资产列表: {balances}")
    
    # 找到余额最高和最低的链
    max_chain = max(balances.items(), key=lambda x: x[1])[0]
    min_chain = min(balances.items(), key=lambda x: x[1])[0]
    
    # 使用固定金额
    amount_eth = AMOUNT_ETH
    print(f"固定跨链金额: {amount_eth} ETH")
    
    # 如果最高余额链有足够 ETH，则跨链到最低余额链
    if balances[max_chain] >= amount_eth and max_chain != min_chain:
        print(f"跨链操作: 从 {max_chain} 向 {min_chain} 转移 {amount_eth} ETH")
        bridge(max_chain, min_chain, amount_eth, account)
    else:
        print(f"跳过跨链: {max_chain} 余额不足（{balances[max_chain]:.2f} ETH）或与 {min_chain} 相同")
    
    return balances

def main():
    private_keys = load_private_keys()
    accounts = [w3_instances['arb'].eth.account.from_key(pk) for pk in private_keys]
    
    print(f"加载 {len(accounts)} 个地址")
    
    round_count = 0
    while True:
        round_count += 1
        print(f"\n第 {round_count} 轮开始于 {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 每个地址轮流进行 TIMES 次跨链
        for i in range(TIMES):
            print(f"\n跨链第 {i+1} 轮")
            for account in accounts:
                try:
                    print(f"\n处理地址 {account.address}")
                    # 每个地址执行 CROSS_PER_ADDRESS 次跨链
                    for j in range(CROSS_PER_ADDRESS):
                        print(f"第 {i+1} 轮，第 {j+1} 次跨链")
                        check_and_balance_chains(account)
                except Exception as e:
                    print(f"处理地址 {account.address} 时出错: {e}")
                    print(f"跳过地址 {account.address}，继续处理下一个地址...")
                    continue
        
        print(f"\n第 {round_count} 轮结束, 等待1分钟后开始下一轮...")
        time.sleep(1 * 60)

if __name__ == "__main__":
    main()
