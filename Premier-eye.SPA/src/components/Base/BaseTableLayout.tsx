import { Table, TableBody, TableCell, TableHead, TableRow } from '@material-ui/core';
import React, { ReactNode } from 'react';
import { HeadersBaseSettings } from 'typings/table';
import { SortButton } from '../Atomics/SortButton';
import { BaseTableStore } from './BaseTableStore';
import { convert, getMappingForCell } from './BaseTableUtils';

export interface IBaseTableLayout<T> {
    list?: Array<T>;
    headers: HeadersBaseSettings<T>;
    children?: ReactNode;
    store: BaseTableStore;
}

export class BaseTableLayout<T, U extends IBaseTableLayout<T>> extends React.Component<U> {
    public render(): React.ReactElement {
        return (
            <Table>
                <TableHead>
                    <TableRow>{this.renderHeaders(this.props.headers)}</TableRow>
                </TableHead>
                <TableBody>{this.renderBody(this.props.list)}</TableBody>
            </Table>
        );
    }

    protected renderHeaders = (headerNames: HeadersBaseSettings<T>): ReactNode => {
        const headerElements: Array<JSX.Element> = [];

        headerNames.forEach((header, name) => {
            const filterButton = header.buttons?.filterButton;
            const sortButton = header.buttons?.sortButton;

            const handleSortClick = (event: React.MouseEvent<HTMLButtonElement>) => {
                this.props.store.sortDirectionChanged(name, this.props.store.sortDir);
            };

            const handleFilterClick = (event: React.MouseEvent<HTMLButtonElement>) => {
                filterButton?.callback(name);
            };

            let sortElement = null;
            if (sortButton !== false) {
                sortElement =
                    sortButton !== undefined ? (
                        sortButton.element(handleSortClick, name == this.props.store.sortBy, this.props.store.sortDir)
                    ) : (
                        <SortButton
                            onClick={handleSortClick}
                            selected={name == this.props.store.sortBy}
                            direction={name == this.props.store.sortBy ? this.props.store.sortDir : 'desc'}
                        />
                    );
            }

            const filterElement = header.buttons?.filterButton?.element(
                handleFilterClick,
                filterButton?.active as boolean,
            );

            const widthParam = header.width ? { width: header.width } : null;

            headerElements.push(
                <TableCell {...widthParam} key={name.toString()}>
                    {header.text}

                    {filterElement}
                    {sortElement}
                </TableCell>,
            );
        });
        return headerElements;
    };

    protected renderBody = (records?: Array<any>): ReactNode =>
        records?.map((item: any, index: number) => {
            const { id, ...itemData } = item;

            const mappedFields = getMappingForCell(this.props.headers); // TODO проверить, правильно ли инициализирован

            return (
                <TableRow key={id.toString()}>
                    {mappedFields.map((nameOfField: any) => this.renderCell(item, nameOfField, id))}
                </TableRow>
            );
        });

    protected renderCell = (item: any, column: keyof T, rowId: number): ReactNode => {
        const cellValue = item[column];

        const convertedValue = convert(this.props.headers, column, cellValue, item); // работает не так уж долго, как я думал

        return <TableCell key={`${rowId}.${column}`}>{convertedValue}</TableCell>;
    };
}
