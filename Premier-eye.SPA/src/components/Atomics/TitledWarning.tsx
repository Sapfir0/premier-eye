import Tooltip from '@material-ui/core/Tooltip';
import WarningIcon from '@material-ui/icons/Warning';
import React from 'react';

export default function TitledWarning(props: { text: string }) {
    const longText = props.text;
    return (
        <Tooltip title={longText} aria-label="add">
            <WarningIcon style={{ color: 'orange' }} />
        </Tooltip>
    );
}
