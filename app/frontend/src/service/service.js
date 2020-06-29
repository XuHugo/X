import {BlockTag, Provider, TransactionRequest, TransactionResponse} from "ethers/providers";
import {Arrayish, BigNumber, ProgressCallback} from "ethers/utils";
import request from "../utils/request";
import config from '../utils/config'

let {urls} = config
let ethers = require('ethers')

// 默认路径
const PATH_PREFIX = "m/44'/60'/0'/0/"

// 私钥校验
function checkPrivate(key) {
    if (key === '') {
        return "不能为空"
    }
    if (key.length != 66 && key.length != 64) {
        return false, "秘钥长度必须为66或者64"
    }
    if (!key.match(/^(0x)?([0-9A-fa-f]{64})+$/)) {
        return "秘钥为16进制表示[0-9A-fa-f]"
    }
    return ""
}

// 地址校验
function checkAddress(address) {
    try {
        let realAddress =ethers.utils.getAddress(address)
        console.log("realaddress",realAddress)
        return realAddress
    }catch (e) {
        return ""
    }

}

// 随机私钥
function newRandomKey() {
    let randomByte = ethers.utils.randomBytes(32)
    let randomNumber = ethers.utils.bigNumberify(randomByte);
    return randomNumber.toHexString()
}

// 通过私钥创建钱包
function newWalletFromPrivateKey(privateKey) {
    let wallets = []
    let wallet = new ethers.Wallet(privateKey)
    wallets.push(wallet)
    return wallets
}

// 通过助记词创建钱包
function newWalletFromMmic(mmic, path) {
    let wallets = []
    for (let i = 0; i < 10; i++) {
        path = PATH_PREFIX + i
        let wallet = ethers.Wallet.fromMnemonic(mmic, path)
        wallets.push(wallet)
        console.log(i, wallets)
    }
    return wallets
}

// 随机创建钱包
function newRandomWallet() {
    let wallets = []
    let wallet = ethers.Wallet.createRandom()
    wallets.push(wallet)
    return wallets
}

// 校验地址
function checkJsonWallet(data) {
    return ethers.utils.getJsonWalletAddress(data)
}

// 从keystore导入钱包，需要密码
function newWalletFromJson(json, pwd) {

    return new Promise(async (resolve, reject) => {
        try {
            let wallets = []
            let wallet = await ethers.Wallet.fromEncryptedJson(json, pwd, false)
            wallets.push(wallet)
            resolve(wallets)
        } catch (e) {
            reject(e)
        }
    })
}

// 生成助记词
function genMmic() {
    let words = ethers.utils.HDNode.entropyToMnemonic(ethers.utils.randomBytes(16));
    return words
}

// 连接provider
function connectWallet(wallet, providerurl) {
    let provider = new ethers.providers.JsonRpcProvider(providerurl);
    return wallet.connect(provider);
}

// 发送交易
function sendTransaction(wallet,to,value) {
    return wallet.sendTransaction({
        to: to,
        value: value,
    })
}

//签名交易
async function  sendRawTransaction(wallet,transaction){
	let signtx = await wallet.sign(transaction)
	console.log(signtx)
	transaction["from"]=wallet.address
    transaction["rawtx"]=signtx
    transaction["token"]=false
    let txhash = await request(urls.eth.sendtx, transaction, "POST")
	console.log(txhash)
	return txhash
}

//获取余额
async function  getTokenValue(wallet,tokenaddr){
    let body ={}
	body["address"]=wallet.address
    body["token"]=tokenaddr
    console.log("serive.gettoken:",body)
    let tokenvalue = await request(urls.token.gettoken, body,"POST")
	console.log(tokenvalue)
	return tokenvalue
}

//签名交易
async function  sendRawTokenTransaction(wallet,transaction,to,value,decimals){
	let signtx = await wallet.sign(transaction)
	let tx = {
	from:wallet.address,
    to:to,
    value:value,
    contract:transaction["to"],
    rawtx:signtx,
    token:true,
    nonce:transaction["nonce"],
    decimals:decimals}
    console.log("@@@@@@sendRawTokenTransaction:",tx)
    let txhash = await request(urls.token.sendtoken, tx, "POST")
	console.log(txhash)
	return txhash
}

export {
    checkPrivate,
    checkAddress,
    newRandomKey,
    newWalletFromPrivateKey,
    newWalletFromMmic,
    newRandomWallet,
    genMmic,
    newWalletFromJson,
    checkJsonWallet,
    connectWallet,
    sendTransaction,
	sendRawTransaction,
    getTokenValue,
    sendRawTokenTransaction,
}
