import { TableSortLabel } from '@material-ui/core';
import React, { MouseEventHandler } from 'react';
import { SortDirection } from '../../typings/table';

export interface SortButtonProps {
    onClick: MouseEventHandler;
    selected: boolean;
    direction: SortDirection;
}

export const SortButton = (props: SortButtonProps): React.ReactElement => {
    return <TableSortLabel onClick={props.onClick} active={props.selected} direction={props.direction} />;
};
