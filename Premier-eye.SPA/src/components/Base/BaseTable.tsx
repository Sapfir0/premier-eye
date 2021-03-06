import React from 'react';
import { SortDirection } from '../../typings/table';
import { BaseTableLayout, IBaseTableLayout } from './BaseTableLayout';

export interface IBaseTable<T> extends IBaseTableLayout<T> {
    page: number;
    pageSize: number;
    filterName: string;
    filterValue: string;
}

export class BaseTable<TDto, TProps extends IBaseTable<TDto>> extends React.Component {
    constructor(props: TProps) {
        super(props);
    }

    public render(): React.ReactElement {
        return <BaseTableLayout<TDto, TProps> {...this.props} />;
    }

    private switchDirection = (direction: SortDirection): SortDirection => {
        return direction == 'asc' ? 'desc' : 'asc';
    };
}
