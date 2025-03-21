# t3rn
说明：T3RN自动SWAP脚本，据说单个地址SWAP上限奖励是2万个BRN。

当前支持op和uni互刷，op和arb互刷。刷之前检查各链上是否有对应的测试eth。

## 安装支持
    pip install web3 eth_account

    pip install --upgrade web3

参数配置：只能修改私匙和互跨次数，跨链金额不能更改。需要更改的请修改代码中对应的input data

   PRIVATE_KEY = "0x1234567890"  #填写私匙
   
   AMOUNT_ETH = 0.3  # 每次跨链金额（单位：ETH）
   
   TIMES = 1000  # 互跨来回次数
   
### 1 op_uni_03.py OP<->UNI 互SWAP刷奖励
    python3 op_uni_03.py
运行后如下截图
![image](https://github.com/user-attachments/assets/b84918fa-db30-41d1-b53c-e49541689c61)


### 2 op_arb_03.py OP<->ARB 互SWAP刷奖励
   python3 op_arb_03.py
