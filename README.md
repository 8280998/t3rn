# 1. T3RN一键盘节点
说明：这个是T3rn的一键脚本，注意如下：

这个脚本适合于root用户，其他用户自己修改路径或设置成变量，懒得改了

查看日志命令是： tail -f executor.log

    curl -O https://raw.githubusercontent.com/8280998/t3rn/refs/heads/main/t3_node.sh && chmod +x t3_node.sh  && ./t3_node.sh

2024-04-08 增加monad网络


## 1.1 一些常用节点查询

1.11 检查节点版本，返回类似信息：{"level":"info","time":1744116221892,"environment":"testnet","msg":"💿 Version: v0.62.0"}

    grep "Version:" executor.log

1.12 检查奖励信息，返回类似信息：Total reward: 0 #使用一键节点安装的话，每次更新后都会对日志进行复盖，之前的奖励信息也无法查询。这个命令作用不大

     grep '"wallet":"0x123456"' executor.log| awk -F'reward":' '{sub(/,.*/,"",$2); sum += $2} END {print "Total reward: " sum}'

# 2. t3rn跨链脚本 autoswap.py，以后只针对此脚本做更新，其他不再更新。
## 因为各条链经常卡住，于2025-05-09，新写的一个脚本，可以自动调节各链ETH从最多往最少跨

新写的脚本解决ETH堆积到一条链的问题，自动平衡各链资产，适合做节点同时又SWAP的地址

## 安装支持
    pip install web3 eth_account

    pip install --upgrade web3

运行配置：需要把私匙存放在address.txt，一行一个。

# 注意安全，自行阅读代码或运行前先把代码交给chatgpt/grok等ai检查。

建议使用脚本以下默认参数，因为自动无限循环跨链

AMOUNT_ETH = 2.5        # 固定跨链数量跟模板数据强关联，不可修改

TIMES = 10                 # 跨链次数

CROSS_PER_ADDRESS = 3     # 每次跨链尝试次数，因为经常失败建议设置为2-5次
   
### 1 ETH自动调节SWAP脚本 

显示运行时：

    python3 autoswap.py

后台运行：

    nohup python3 autoswap.py > autoswap.log 2>&1 &
    
更新后的自动调节脚本运行后如下截图
![image](https://github.com/user-attachments/assets/ee635c53-75c5-48f0-8c1d-dba9b96de815)




