import { Table, TableBody, TableCell, TableHead, TableRow } from '@material-ui/core';
import { observer } from 'mobx-react';
import React, { ReactNode } from 'react';
import { ColumnDefinition, FilterButton, HeadersBaseSettings, SortButton as SortButtonType } from 'typings/table';
import { InputField } from '../Atomics/InputField';
import { SearchButton } from '../Atomics/SearchButton';
import { SortButton } from '../Atomics/SortButton';
import { BaseTableStore } from './BaseTableStore';
import { convert, getMappingForCell } from './BaseTableUtils';

export interface IBaseTableLayout<T> {
    list?: Array<T>;
    headers: HeadersBaseSettings<T>;
    children?: ReactNode;
    store: BaseTableStore;
}

export const BaseTableLayout = observer(
    class BaseTableLayout<T, U extends IBaseTableLayout<T>> extends React.Component<U> {
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

        private getSortButton<T>(
            sortButton: SortButtonType | false | undefined,
            name: ColumnDefinition<T>,
            handleSortClick: () => void,
        ) {
            let sortElement = null;
            if (sortButton !== false) {
                if (sortButton !== undefined) {
                    sortElement = sortButton.element(
                        handleSortClick,
                        name == this.props.store.sortBy,
                        this.props.store.sortDir,
                    );
                } else {
                    sortElement = (
                        <SortButton
                            onClick={handleSortClick}
                            selected={name == this.props.store.sortBy}
                            direction={name == this.props.store.sortBy ? this.props.store.sortDir : 'desc'}
                        />
                    );
                }
            }
            return sortElement;
        }

        private getFilterButton<T>(
            filterButton: FilterButton | false | undefined,
            name: ColumnDefinition<T>,
            onChange: (event: React.ChangeEvent<HTMLInputElement>) => void,
            onClose: () => void,
        ) {
            let filterElement = null;
            if (filterButton !== false) {
                if (filterButton !== undefined) {
                    filterElement =
                        name == this.props.store.filterName
                            ? filterButton.input(onChange, onClose)
                            : filterButton.element(() => this.props.store.filterNameChanged(name as string));
                } else {
                    filterElement =
                        name == this.props.store.filterName ? (
                            <InputField onClose={onClose} onChange={onChange} />
                        ) : (
                            <SearchButton onClick={() => this.props.store.filterNameChanged(name as string)} />
                        );
                }
            }
            return filterElement;
        }

        protected renderHeaders = (headerNames: HeadersBaseSettings<T>): ReactNode => {
            const headerElements: Array<JSX.Element> = [];

            headerNames.forEach((header, name) => {
                const filterButton = header.buttons?.filterButton;
                const sortButton = header.buttons?.sortButton;

                const handleSortClick = () => {
                    this.props.store.sortDirectionChanged(name, this.props.store.sortDir);
                };

                const handleFilterValueChanged = (event: React.ChangeEvent<HTMLInputElement>) => {
                    this.props.store.filterValueChanged(event.target.value);
                };

                const onClose = () => {
                    this.props.store.filterNameChanged(undefined);
                    this.props.store.filterValueChanged(undefined);
                };

                const sortElement = this.getSortButton(sortButton, name, handleSortClick);
                const filterElement = this.getFilterButton(filterButton, name, handleFilterValueChanged, onClose);

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
    },
);
