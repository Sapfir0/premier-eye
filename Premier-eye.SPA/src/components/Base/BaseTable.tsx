import React, { ReactNode } from 'react';
import { BaseTableLayout, IBaseTableLayout } from './BaseTableLayout';

export interface IBaseTable<T> extends IBaseTableLayout<T> {
    page: number;
    pageSize: number;
    filterName: string;
    filterValue: string;
}

export class BaseTable<TDto, TProps extends IBaseTable<TDto>> extends React.Component<TProps> {
    constructor(props: TProps) {
        super(props);
    }

    public render(): JSX.Element {
        return <BaseTableLayout<TDto, TProps> {...this.props} />;
    }

}
