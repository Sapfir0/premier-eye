import { Snackbar } from '@material-ui/core';
import Alert from '@material-ui/lab/Alert';
import React from 'react';
import { useModalState } from '../../services/hooks';

export type ErrorSnackbarProps = {
    message: string;
};

export const ErrorSnackbar = (props: ErrorSnackbarProps) => {
    const { onClose, isOpen } = useModalState();

    return (
        <Snackbar
            anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
            open={isOpen}
            onClose={onClose}
            key={props.message}
        >
            <Alert onClose={onClose} severity="error">
                {props.message}
            </Alert>
        </Snackbar>
    );
};
