import { MouseEventHandler } from "react";

export type Key<T> = keyof T;
export type HeadersBaseSettings<T> = Map<Key<T> | '', HeaderName<T>>;

export type SortDirection = 'asc' | 'desc';

export type OnClick = (event: React.MouseEvent<HTMLButtonElement>, data: any ) => void; //TODO тип указать

export type Button = {
    callback: (...args: any) => any;
    active: boolean;
};

export interface SortButton extends Button {
    sortDirection: SortDirection;
    element: (onClick: MouseEventHandler, selected: boolean, direction: SortDirection) => React.ReactElement;
}

export interface FilterButton extends Button {
    element: (onClick: MouseEventHandler, selected: boolean) => React.ReactElement;
}

export type Buttons = {
    sortButton?: SortButton;
    filterButton?: FilterButton;
};

export interface HeaderName<DTO = any> {
    buttons?: Buttons;
    width?: number;
    text: string;
    cellProps?: (cellValue: any /*DTO | DTO[keyof DTO]*/) => any; //TODO тип
    emptyDataColumn?: boolean; // если подано это значение, то в convert function будет передено не текущее значение столбца, а вся строка
    convertFunction?: (cellValue: any /*DTO | DTO[keyof DTO]*/, columnName: keyof DTO) => React.ReactElement | string;
}
