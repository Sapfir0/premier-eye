import React, {ReactNode} from "react";
import {convert, getMappingForCell} from "./BaseTableUtils";
import {TableCell, Table, TableRow, TableBody, TableContainer, TableHead} from "@material-ui/core"
import { HeadersBaseSettings } from "../../typings/common";


export interface IBaseTableLayout<T> {
    list?: Array<T>
    headers: HeadersBaseSettings<T>
}


export class BaseTableLayout<T, U extends IBaseTableLayout<T>> extends React.Component<U> {

    public render(): React.ReactElement {
        return (
            <Table  >
                <TableHead><TableRow>{this.renderHeaders(this.props.headers)}</TableRow></TableHead>
                <TableBody>{this.renderBody(this.props.list)}</TableBody>
            </Table>
        )
    }

    protected renderHeaders = (headerNames: HeadersBaseSettings<T>): ReactNode => {
        const headerElements: Array<JSX.Element> = []

        headerNames.forEach((header, name) => {

            headerElements.push(<TableCell key={name.toString()}>
                {header.text}
            </TableCell>)
        })
        return headerElements
    }


    protected renderBody = (records?: Array<any>): ReactNode =>
        records?.map((item: any, index: number) => {
            const {id, ...itemData} = item;

            const mappedFields = getMappingForCell(this.props.headers) // TODO проверить, правильно ли инициализирован

            return (
                <TableRow key={id.toString()}>

                    {mappedFields.map((nameOfField: any) => this.renderCell(item, nameOfField, id))}

                </TableRow>
            );
        });

    protected renderCell = (item: any, column: keyof T, rowId: number): ReactNode => {
        const cellValue = item[column];
        
        const convertedValue = convert(this.props.headers, column, cellValue, item) // работает не так уж долго, как я думал
        
        return (
            <TableCell key={`${rowId}.${column}`}>
                {convertedValue}
            </TableCell>
        )
    }

}

