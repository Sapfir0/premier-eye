import Button from '@material-ui/core/Button';
import React from 'react';
import './UploadButton.pcss';

export const UploadButton = (props: any) => {
    // buttonProps
    return (
        <>
            <input accept="image/*" id="contained-button-file" className="uploadButton" type="file" />
            <label htmlFor="contained-button-file">
                <Button {...props} variant="contained" color="primary" component="span">
                    {props.children}
                </Button>
            </label>
        </>
    );
};
