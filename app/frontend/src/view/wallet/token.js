import React, {Component} from 'react'
import {Grid, Form, Header, Loader, Button, Loading, Segment, Image, List,Menu,Icon,Label} from 'semantic-ui-react'
import request from '../../utils/request'
import config from '../../utils/config'
import Tab_txlist from '../wallet/tab_txlist'

let {urls} = config
let ethers = require('ethers')
let service = require('../../service/service')
let fileSaver = require('file-saver');
//let sleep = require("sleep")

export default class Token extends Component {

    state = {
        wallets: [],// 支持多账户，默认第0个
        selectWallet: 0,
        //provider: "http://127.0.0.1:8545", //环境
        provider:"https://ropsten.infura.io/v3/19de6a4c0ccb416287b18bc81fa0b3b1",
		walletInfo: [], // 钱包信息，获取为异步，单独存储下
        activeWallet: {}, // 当前活跃钱包
        txto: "", // 交易接收地址
        txvalue: "", // 转账交易金额
        pwd: "", // 导出keystore需要密码
        activeItem: 'ETH',
        txlist:'',
        tokenaddr:'',
        tokenvalue:'',
        decimals:'',


        // UI状态表示
        txPositive: false, //
        loading: false,
        exportLoading: false,

    }

    constructor(props) {
        super(props)
        this.state.wallets = props.wallets
        this.state.selectWallet = props.wallets.length == 0 ? -1 : 0
    }

    // 更新钱包信息
    updateActiveWallet() {
        if (this.state.wallets.length == 0) {
            return null
        }
        let {tokenaddr} = this.state
        let activeWallet = this.getActiveWallet()
        this.setState({activeWallet})
        this.loadActiveWalletInfo(activeWallet)
        return activeWallet
    }

    // 获取当前的钱包
    getActiveWallet() {
        let wallet = this.state.wallets[this.state.selectWallet]
        console.log("wallet addr", wallet.address)
        // 激活钱包需要连接provider
        return service.connectWallet(wallet, this.state.provider)
    }

    // 加载钱包信息
    async loadActiveWalletInfo(wallet) {
        let address,balance,tx
        if (false){
            address = wallet.address
            let infos = await request(urls.user.add, { address:address,}, "POST")
            balance = infos.balance
            tx = infos.nonce
        }
        else{
            address = await wallet.getAddress()
            balance = await wallet.getBalance()
            tx = await wallet.getTransactionCount()
        }
        this.setState({
            walletInfo: [address, balance, tx]
        })
    }

    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms))
    }
    async updateActiveWalletInfo() {
        let {tokenaddr} = this.state
        if(tokenaddr === ""){
            this.sleep(3000)
        }else{
            let wallet = this.state.wallets[this.state.selectWallet]
            let address,balance,tx
            address = wallet.address
            let infos = await request(urls.token.list, { address:address,contract:tokenaddr}, "POST")
            console.log(infos.result)
            let lili=[]
            for  (let info in infos.result){
                let ll
                ll =(<Tab_txlist
                    from={infos.result[info].from}
                    to={infos.result[info].to}
                    hash={infos.result[info].hash}
                    nonce={infos.result[info].nonce}
                    value={infos.result[info].value}
                    times={infos.result[info].time}
                    state={infos.result[info].state}
                />)
                lili.push(ll)
            }
            console.log(lili)
            this.setState({
                txlist: null
            })
            this.setState({
                txlist: lili
            })
            //this.forceUpdate()
            console.log(this.state.txlist)
        }

    }

    // 发送交易
    onSendClick = () => {
        let {txto, txvalue, tokenaddr, decimals, activeWallet} = this.state

        console.log("~~~~~~~~~~~send token ", tokenaddr)
        // 地址校验
        let address = service.checkAddress(tokenaddr)
        if (address == "") {
            alert("地址不正确")
            return
        }
        console.log(txvalue, isNaN(txvalue))
        if (isNaN(txvalue)) {
            alert("转账金额不合法")
            return
        }

        // 设置加载loading，成功或者识别后取消loading
        this.setState({loading: true})
		console.log("walletInfo;",this.state.walletInfo[2])
        var amount = txvalue*Math.pow(10,decimals);
        amount = amount.toString(16);
        var len =64-amount.length;
        var o="0";
		o=o.repeat(len);
        let transaction = {
				nonce: this.state.walletInfo[2],
				gasLimit: 60000,
				gasPrice: ethers.utils.bigNumberify("20000000000"),
				to: tokenaddr,
				// ... or supports ENS names
				// to: "ricmoo.firefly.eth",
				data: "0xa9059cbb"+"000000000000000000000000"+txto.slice(2)+o+amount,
 			    // 这可确保无法在不同网络上重复广
	    	    chainId: ethers.utils.getNetwork('ropsten').chainId
		}
        console.log("~~~~~~~~~~~~transaction;",transaction)
		service.sendRawTokenTransaction(activeWallet, transaction,txto,txvalue,decimals)
				.then(tx=>{
					//console.log(tx);
					alert("sendTokenRawTraction ok!",tx);
					this.updateActiveWallet()
					this.setState({loading: false, txto: "", txvalue: ""})
				})
				.catch(e=>{
					this.setState({loading: false})
					console.log(e);
					alert(e);
				})
    }

    // 页面加载完毕，更新钱包信息
    componentDidMount() {
        this.updateActiveWallet()
        this.timer = setInterval(() => this.updateActiveWalletInfo(),  15000);
    }

      componentWillUnmount() {
        this.timer && clearTimeout(this.timer);
    }

    getTokenValue = (e, {value}) => {
        console.log('get token value:',value);
        let { activeWallet} = this.state
        this.setState({tokenaddr:value})
        service.getTokenValue(activeWallet, value)
            .then(txv=>{
					alert("get tokenvalue ok!");
					this.setState({tokenvalue: txv["balance"],decimals:txv["decimals"]})
                    console.log("get tokenvalue ok!",txv);
				})
				.catch(e=>{
					this.setState({loading: false})
					console.log(e);
					alert(e);
				})
    }

    handleChange = (e, {name, value}) => {
        this.setState({[name]: value})
    }

    handleItemClick = (e, { name }) => this.setState({ activeItem: name })

    render() {
        // 金额显示需要手工转换
        let wallet = this.state.walletInfo
        if (wallet.length == 0) {
            return <Loader active inline/>
        }
        let balance = wallet[1]
        let balanceShow = ethers.utils.formatEther(balance) + "(" + balance.toString() + ")"
        let txlist = this.state.txlist
        const { activeItem } = this.state.activeItem
        return (
            <div>
                <Grid columns='equal' textAlign='center'>
                    <Grid.Row stretched >
                        <Grid.Column style={{maxWidth: 650, marginTop: 10}}>
                            <Segment stacked textAlign='left'>
                                <Header as='h1'>Token</Header>
                                <Form.Input
                                    style={{width: "100%"}}
                                    action={{
                                        color: 'teal',
                                        labelPosition: 'left',
                                        icon: 'address card',
                                        content: '账户'
                                    }}
                                    actionPosition='left'
                                    value={wallet[0]}
                                />
                                <br/>
                                <Form.Input
                                    style={{width: "100%"}}
                                    action={{
                                        color: 'teal',
                                        labelPosition: 'left',
                                        icon: 'credit card',
                                        content: 'token'
                                    }}
                                    actionPosition='left'
                                    defaultValue='0x00'
                                    type='text' addr='tokenaddr' required value={this.state.tokenaddr}
                                    placeholder='token地址' onChange={this.getTokenValue}/>
                                <br/>
                                <Form.Input
                                    style={{width: "100%"}}
                                    action={{
                                        color: 'teal',
                                        labelPosition: 'left',
                                        icon: 'ethereum',
                                        content: '余额'
                                    }}
                                    actionPosition='left'
                                    placeholder='token余额'
                                    value={this.state.tokenvalue}
                                />
                                <br/>
                            </Segment>
                            <Segment stacked textAlign='left'>
                                <Header as='h1'>Token 转账</Header>
                                <Form.Input
                                    style={{width: "100%"}}
                                    action={{
                                        color: 'teal',
                                        labelPosition: 'left',
                                        icon: 'address card',
                                        content: '地址'
                                    }}
                                    actionPosition='left'
                                    defaultValue='52.03'
                                    type='text' name='txto' required value={this.state.txto}
                                    placeholder='对方地址' onChange={this.handleChange}/>
                                <br/>
                                <Form.Input
                                    style={{width: "100%"}}
                                    action={{
                                        color: 'teal',
                                        labelPosition: 'left',
                                        icon: 'ethereum',
                                        content: '金额'
                                    }}
                                    actionPosition='left'
                                    defaultValue='1.00'
                                    type='text' name='txvalue' required value={this.state.txvalue}
                                    placeholder='token' onChange={this.handleChange}/>
                                <br/>
                                <Button
                                    color='twitter'
                                    style={{width: "100%"}}
                                    size='large'
                                    loading={this.state.loading}
                                    onClick={this.onSendClick}>
                                    确认
                                </Button>
                            </Segment>
                        </Grid.Column>
                        <Grid.Column style={{maxWidth: 650, marginTop: 10}}>
                            <Segment stacked raised textAlign='left'>
                                <Header as='h1'>TxList</Header>
                                <List divided relaxed>
                                    {txlist}
                                </List>
                            </Segment>
                        </Grid.Column>
                    </Grid.Row>
                </Grid>

            </div>
        )
    }
}
