import Tooltip from '@material-ui/core/Tooltip';
import WarningIcon from '@material-ui/icons/Warning';
import React from 'react';
import './Warning.pcss';

export default function TitledWarning(props: { text: string }) {
    const longText = props.text;

    return (
        <Tooltip title={longText} aria-label="add">
            <WarningIcon className="warning-icon" />
        </Tooltip>
    );
}
