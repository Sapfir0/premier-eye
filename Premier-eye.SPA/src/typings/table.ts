import { MouseEventHandler } from 'react';

export type Key<T> = keyof T;
export type ColumnDefinition<T> = Key<T> | '';
export type HeadersBaseSettings<T> = Map<ColumnDefinition<T>, HeaderName<T>>;

export type SortDirection = 'asc' | 'desc';

export type Button = {};

export interface SortButton extends Button {
    sortDirection: SortDirection;
    element: (onClick: MouseEventHandler, selected: boolean, direction: SortDirection) => React.ReactElement;
}

export interface FilterButton extends Button {
    element?: (onClick: MouseEventHandler) => React.ReactElement;
    input?: (onChange: (event: React.ChangeEvent<HTMLInputElement>) => void, onClose: () => void) => React.ReactElement;
}

export type Buttons = {
    sortButton?: SortButton | false;
    filterButton?: FilterButton | false;
};

export interface HeaderName<DTO = any> {
    buttons?: Buttons;
    width?: number;
    text: string;
    cellProps?: (cellValue: DTO | DTO[keyof DTO]) => any; //TODO тип
    emptyDataColumn?: boolean; // если подано это значение, то в convert function будет передено не текущее значение столбца, а вся строка
    convertFunction?: (cellValue: DTO | DTO[keyof DTO], columnName: keyof DTO) => React.ReactElement | string;
}
