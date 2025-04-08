# 1. T3RN一键盘节点
说明：这个是T3rn的一键脚本，注意如下：

这个脚本适合于root用户，其他用户自己修改路径或设置成变量，懒得改了

查看日志命令是： tail -f executor.log

    curl -O https://raw.githubusercontent.com/8280998/t3rn/refs/heads/main/t3_node.sh && chmod +x t3_node.sh  && ./t3_node.sh

2024-04-08 增加monad网络

    curl -O https://raw.githubusercontent.com/8280998/t3rn/refs/heads/main/update.sh && chmod +x update.sh  && ./update.sh

update.sh 个人更新用，免输入key更新

## 1.1 一些常用节点查询

1.11 检查节点版本，返回类似信息：{"level":"info","time":1744116221892,"environment":"testnet","msg":"💿 Version: v0.62.0"}

    grep "Version:" executor.log

1.12 检查奖励信息，返回类似信息：Total reward: 0 #使用一键节点安装的话，每次更新后都会对日志进行复盖，之前的奖励信息也无法查询。这个命令作用不大

     grep '"wallet":"0x123456"' executor.log| awk -F'reward":' '{sub(/,.*/,"",$2); sum += $2} END {print "Total reward: " sum}'

# 2. t3rn跨链脚本 
## 因为op跨链经常卡链上，现更新到uni-arb互跨

2025-04-04 新增BASE到UNI的单边跨链。需要把私匙存放在address.txt,一行一个

    python3 basetouni.py
    
OP测试网经常卡链上，现在弃用OP的脚本，改为uni--arb互跨

其他脚本不再更新，现在只针对uni-arb做更新

如果需要arb到uni单边跨链，把uni_arb_35.py的代码加个#，这样：# bridge_uni_to_arb(AMOUNT_ETH, account)

## 安装支持
    pip install web3 eth_account

    pip install --upgrade web3

参数配置：只能修改私匙和互跨次数，跨链金额不能更改。

不懂代码请不要修改每次跨链的3.5.只修改私匙和次数。

默认循环一轮为10分钟，可以自定义为其他时间

支持批量多号刷SWAP，把私匙添加到address.txt,一行一个


   PRIVATE_KEY = "0x1234567890"  #填写私匙
   
   AMOUNT_ETH = 3.5  # 每次跨链金额（单位：ETH）
   
   TIMES = 50  # 互跨来回次数

   time.sleep(10 * 60)  # 等待 10 分钟，循环时间可修改
   
### 1 uni_arb_35.py ARB <-> UNI 互SWAP刷奖励 
    python3 uni_arb_35.py
运行后如下截图
![image](https://github.com/user-attachments/assets/b84918fa-db30-41d1-b53c-e49541689c61)



