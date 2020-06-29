import React, {Component} from 'react'
import {Button, Header, Icon, Label, Segment,List} from "semantic-ui-react";

export default class Tab_txlist extends Component {
    state = {
        from: "",
        to: "",
        value: "",
        hash: "",
        nonce: "",
        times: "",
        state: "",
    }

    constructor(props) {
        super(props)

        this.state.from= props.from
        this.state.to= props.to
        this.state.value= props.value
        this.state.hash= props.hash
        this.state.nonce= props.nonce
        this.state.times= props.times
        this.state.state= props.state
    }
    pending=(<List.Icon loading name='ethereum' size='large' verticalAlign='middle' />)

    success=(<List.Icon  name='ethereum' size='large' verticalAlign='middle' />)

    render() {
        let content = this.state.state===1 ?  this.pending : this.success
        return (
            <List.Item>
                {content}
                <List.Content>
                    <Label color='teal' >
                        <Icon name='barcode' /> {this.state.hash.slice(0,42)}
                        <br />{this.state.hash.slice(42,)}
                        <br />
                        <br />
                        <Icon name='sign-out' /> {this.state.from}
                        <br />
                        <br />
                        <Icon name='sign-in' /> {this.state.to}
                        <br />
                        <br />
                        <Icon name='pin' /> {this.state.nonce}
                        <br />
                        <br />
                        <Icon name='cny' /> {this.state.value}
                        <br />
                        <br />
                        <Icon name='wait' /> {this.state.times}
                    </Label>
                </List.Content>
            </List.Item>
        );
    }
}