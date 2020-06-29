import React, {Component} from 'react'
import {Button, Header, Segment} from "semantic-ui-react";
import {Form} from "semantic-ui-react/dist/commonjs/collections/Form/Form";
import {Grid} from "semantic-ui-react/dist/commonjs/collections/Grid/Grid";

export default class Tab_settings extends Component {

    render() {
        return (
            <Segment stacked textAlign='left'>
                <Header as='h1'>设置</Header>
                <Form.Input
                    style={{width: "100%"}}
                    action={{
                        color: 'teal',
                        labelPosition: 'left',
                        icon: 'lock',
                        content: '密码'
                    }}
                    actionPosition='left'
                    defaultValue='1.00'
                    type='pwd' name='pwd' required value={this.state.pwd}
                    placeholder='密码'
                    onChange={this.handleChange}/>
                <br/>
                <Button
                    color='twitter'
                    style={{width: "48%"}}
                    onClick={this.onExportPrivate}>
                    查看私钥
                </Button>
                <Button
                    color='twitter'
                    style={{width: "48%"}}
                    onClick={this.onExportClick}
                    loading={this.state.exportLoading}>
                    导出keystore
                </Button>
            </Segment>
        )
    }
}