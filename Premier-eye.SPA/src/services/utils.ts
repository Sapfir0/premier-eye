import { SortDirection } from 'typings/table';

export const range = (len: number) => Array.from(Array(len).keys());

export const switchDirection = (direction: SortDirection): SortDirection => {
    return direction == 'asc' ? 'desc' : 'asc';
};
