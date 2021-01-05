import React, { Component } from 'react';
import { BaseInteractionError } from '../../../services/Errors/BaseInteractionError';
import { ErrorMessage } from './ErrorMessage';

export interface IErrorMessageList {
    errors: BaseInteractionError[];
}

export class ErrorMessageList extends Component<IErrorMessageList> {
    render() {
        return (
            <div>
                {this.props.errors.map((error) => (
                    <ErrorMessage key={error.name} text={error.message} />
                ))}
            </div>
        );
    }
}
