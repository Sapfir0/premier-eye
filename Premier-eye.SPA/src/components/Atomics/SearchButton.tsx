import IconButton from '@material-ui/core/IconButton';
import SearchIcon from '@material-ui/icons/Search';
import React, { MouseEventHandler } from 'react';

export interface SearchButtonProps {
    onClick: MouseEventHandler;
}

export const SearchButton = (props: SearchButtonProps): React.ReactElement => {
    return (
        <IconButton onClick={props.onClick}>
            <SearchIcon />
        </IconButton>
    );
};
