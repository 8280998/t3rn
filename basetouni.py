from web3 import Web3
import time
import random

# 这个是单边base到uni脚本，数量为5ETH一次，不要更改
# 读取address.txt的私匙，一行一个，数量不限
#

# 可自定义参数
AMOUNT_ETH = 5
TIMES = 10

# RPC 地址
UNI_RPC_URL = "https://unichain-sepolia.drpc.org"
ARB_RPC_URL = "https://base-sepolia.gateway.tenderly.co"

# 合约地址
UNI_TO_ARB_CONTRACT = "0x1cEAb5967E5f078Fa0FEC3DFfD0394Af1fEeBCC9"
ARB_TO_UNI_CONTRACT = "0xCEE0372632a37Ba4d0499D1E2116eCff3A17d3C3"

# 基础 Input Data
UNI_TO_ARB_BASE_DATA = "0x56591d5961726274000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000{address}0000000000000000000000000000000000000000000000003092467525c6a05c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000030927f74c9de0000"
ARB_TO_UNI_BASE_DATA = "0x56591d59756e6974000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000{address}0000000000000000000000000000000000000000000000004563757479b6bcb4000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004563918244f40000"

# 初始化 Web3 连接
w3_uni = Web3(Web3.HTTPProvider(UNI_RPC_URL))
w3_arb = Web3(Web3.HTTPProvider(ARB_RPC_URL))

# 检查连接
if not w3_uni.is_connected():
    raise Exception("无法连接到 UNI 测试网")
if not w3_arb.is_connected():
    raise Exception("无法连接到 ARB 测试网")

# 读取私钥文件
def load_private_keys():
    with open("address.txt", "r") as f:
        return [line.strip() for line in f if line.strip()]

# 从 UNI 跨到 ARB
def bridge_uni_to_arb(amount_eth, account):
    try:
        amount_wei = w3_uni.to_wei(amount_eth, 'ether')
        nonce = w3_uni.eth.get_transaction_count(account.address)
        data = UNI_TO_ARB_BASE_DATA.format(address=account.address[2:])
        
        tx = {
            'from': account.address,
            'to': UNI_TO_ARB_CONTRACT,
            'value': amount_wei,
            'nonce': nonce,
            'gas': 400000,
            'gasPrice': w3_uni.to_wei(1.6, 'gwei'),
            'chainId': 84532,
            'data': data
        }
        print(f"UNI -> ARB: Sending {amount_eth} ETH from {account.address}")
        signed_tx = w3_uni.eth.account.sign_transaction(tx, account.key)  # 修改为 account.key
        tx_hash = w3_uni.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"UNI -> ARB 交易已发送，交易哈希: {w3_uni.to_hex(tx_hash)}")
        tx_receipt = w3_uni.eth.wait_for_transaction_receipt(tx_hash)
        print(f"交易已确认，区块号: {tx_receipt.blockNumber}")
        return True
    except Exception as e:
        print(f"UNI -> ARB 跨链失败，错误: {e}")
        return False

# 从 ARB 跨到 UNI
def bridge_arb_to_uni(amount_eth, account):
    try:
        amount_wei = w3_arb.to_wei(amount_eth, 'ether')
        nonce = w3_arb.eth.get_transaction_count(account.address)
        data = ARB_TO_UNI_BASE_DATA.format(address=account.address[2:])
        
        tx = {
            'from': account.address,
            'to': ARB_TO_UNI_CONTRACT,
            'value': amount_wei,
            'nonce': nonce,
            'gas': 400000,
            'gasPrice': w3_arb.to_wei(0.5, 'gwei'),
            'chainId': 84532,
            'data': data
        }
        print(f"ARB -> UNI: Sending {amount_eth} ETH from {account.address}")
        signed_tx = w3_arb.eth.account.sign_transaction(tx, account.key)  # 修改为 account.key
        tx_hash = w3_arb.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"ARB -> UNI 交易已发送，交易哈希: {w3_arb.to_hex(tx_hash)}")
        tx_receipt = w3_arb.eth.wait_for_transaction_receipt(tx_hash)
        print(f"交易已确认，区块号: {tx_receipt.blockNumber}")
        return True
    except Exception as e:
        print(f"ARB -> UNI 跨链失败，错误: {e}")
        return False

# 主执行逻辑
def main():
    private_keys = load_private_keys()
    accounts = [w3_uni.eth.account.from_key(pk) for pk in private_keys]
    
    print(f"加载了 {len(accounts)} 个账户")
    
    # 无限循环，每轮结束后等待 10 分钟
    round_count = 0
    while True:
        round_count += 1
        print(f"\n第 {round_count} 轮跨链操作开始，当前时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"开始 UNI 和 ARB 互跨 {TIMES} 次，每次 {AMOUNT_ETH} ETH")
        
        for i in range(TIMES):
            print(f"\n第 {i+1} 次互跨：")
            for idx, account in enumerate(accounts):
                # UNI -> ARB
             #   bridge_uni_to_arb(AMOUNT_ETH, account)
                
                # 在 UNI -> ARB 和 ARB -> UNI 之间添加 1-2 秒随机间隔
                #delay = random.uniform(1, 2)
                #print(f"等待 {delay:.2f} 秒后进行 ARB -> UNI 跨链...")
                #time.sleep(delay)
                
                # ARB -> UNI
                bridge_arb_to_uni(AMOUNT_ETH, account)
                        
            print(f"第 {i+1} 次互跨完成")
        
        print(f"\n第 {round_count} 轮跨链操作完成，等待10分钟后开始下一轮...")
        time.sleep(10 * 60)  # 等待 10 分钟

if __name__ == "__main__":
    main()
