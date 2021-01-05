import Alert from '@material-ui/lab/Alert';
import React, { Component } from 'react';

export class ErrorMessage extends Component<{ text: string }> {
    render() {
        console.log(this.props.text);
        return <Alert severity="error">{this.props.text} </Alert>;
    }
}
