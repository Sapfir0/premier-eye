import React, {Component} from 'react';
import Alert from '@material-ui/lab/Alert';


export class ErrorMessage extends Component<{text: string}> {
    render() {
        console.log(this.props.text)
        return (
            <Alert severity="error">{this.props.text} </Alert>
        );
    }
}