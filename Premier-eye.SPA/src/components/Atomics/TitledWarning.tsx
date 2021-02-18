import Tooltip from '@material-ui/core/Tooltip';
import WarningIcon from '@material-ui/icons/Warning';
import React from 'react';

const styles = { color: 'orange' };

const WarningRef = React.forwardRef(function WarningRef(props, ref) {
    return <WarningIcon style={styles} />;
});

export default function TitledWarning(props: { text: string }) {
    const longText = props.text;

    return (
        <Tooltip title={longText} aria-label="add">
            <WarningRef />
        </Tooltip>
    );
}
