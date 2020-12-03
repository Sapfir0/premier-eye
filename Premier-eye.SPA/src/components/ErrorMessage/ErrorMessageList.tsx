import React, {Component} from 'react';
import { ErrorMessage } from './ErrorMessage';
import {BaseInteractionError} from "../../services/Errors/BaseInteractionError"

export interface IErrorMessageList {
    errors: BaseInteractionError[]
}

export class ErrorMessageList extends Component<IErrorMessageList> {
    render() {
        return (
            <div>
                {
                    this.props.errors.map((error) => (
                        <ErrorMessage key={error.name} text={error.message} />
                    ))
                }
                
            </div>
        );
    }
}