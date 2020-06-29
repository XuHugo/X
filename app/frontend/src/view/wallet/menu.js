import React,{Component} from 'react'

import {Grid,Header, Image, Tab} from 'semantic-ui-react'
import Wallet from "./wallet"
import Token from "./token"



export default class Menu extends Component {

    state = {
        wallets: [],// 支持多账户，默认第0个
    }

    constructor(props) {
        super(props)
        this.state.wallets = props.wallets
    }

    render() {
        let wallet = this.state.wallets
        const panes = [
            {menuItem: 'ETH', render: () => <Tab.Pane attached={false}><Wallet wallets={wallet}/></Tab.Pane>},
            {menuItem: 'Token', render: () =>  <Tab.Pane attached={false}><Token wallets={wallet}/></Tab.Pane> },
            {menuItem: 'smartcontract', render: () =>  <Tab.Pane>smartcontract Content</Tab.Pane> },
            {menuItem: 'others', render: () =>  <Tab.Pane>others Content</Tab.Pane> },
        ]

        return (
            <Grid textAlign='center'  verticalAlign='middle'>

                <Grid.Column >
                    <Header as='h2' color='teal' textAlign='center'>
                        <Image src='images/logo.png'/> X钱包
                    </Header>
                    <Tab
                        menu={{ fluid: true, vertical: true }}
                        menuPosition='left'
                        panes={panes}
                    />
                </Grid.Column>
            </Grid>
        )
    }
}