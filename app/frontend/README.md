# install

```
➜  eth-webwallet git:(master) ✗ node -v                                          
v8.12.0
➜  eth-webwallet git:(master) ✗ npm install
```



# 开启ganache-cli

```bash
ganache-cli -m 助记词
```

默认端口 8545



# 修改provider

默认链接8545，请确认eth测试端口正常,否则登录后无法进入钱包页面



修改文件:wallet.js

```
state = {
    wallets: [],// 支持多账户，默认第0个
    selectWallet: 0,
    provider: "http://127.0.0.1:8545", //环境,
    }
```

# npm start

```
npm run start
```



# 打开浏览器

```
http://127.0.0.1:3000
```

端口根据npm 分配



# 问题 

ganache provider是可以获取钱包信息，但转账会提示余额不足

大家使用 ganache-cli 开启eth测试环境即可



页面转账成功，余额减少后，可登陆转账的账号，查看真实余额，也都可以使用工具查看

【可选1】进入truffle develop 使用命令查看余额

【可选2】为了便于查看转账及余额信息，大家可以开启**geth**命令行，开启时添加端口

- **geth attach provider-url** 开启geth命令行

- eth.accounts 获取当前账号信息
- eth.getBalance(eth.accounts[8]) 获取某一个账号余额



```bash
➜  00-wallet git:(master) ✗ geth attach http://localhost:8545
Welcome to the Geth JavaScript console!
> eth.accounts
["0xfef3d415f66464c3b38e10fd5f31edbead7be44b", "0xfc26f518d2f7091667dbdd81ee04d1f17d122359", "0x5e7363aa3c0669083a554dde5ed548a8ec90ff12", "0x57060a8a16bff2615769282eb83d1b50891f04a9", "0xc1f109c747e70bbc85371bcb6fbdc8fe23219da9", "0x3d25841411dd7917c123d980f4dd33cad101cc31", "0x9b477be361d60597e24dd7838d29f706396a3fa1", "0x8adffcabe036474de3a6d6f513bfd6df19fbcc1f", "0x2394c966264c3794247136637e0dc9924dfad3d7", "0xbf513ae069d7a58eb4d0f8c6e17402dbe2cc1bee"]
> eth.getBalance(eth.accounts[0])
100000000000000000000
> eth.getBalance(eth.accounts[8])
120000000000000000000
```



