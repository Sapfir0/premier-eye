import { injectable } from 'inversify';
import { action, makeObservable, observable } from 'mobx';
import { ColumnDefinition, SortDirection } from 'typings/table';
import { switchDirection } from '../../services/utils';

@injectable()
export class BaseTableStore {
    sortDir: SortDirection = 'desc';
    sortBy = 'id';
    filterName: string | undefined = undefined;
    filterValue: string | undefined = undefined;

    constructor() {
        makeObservable(this, {
            filterValueChanged: action,
            sortDirectionChanged: action,
            sortDir: observable,
            sortBy: observable,
            filterName: observable,
            filterValue: observable,
            filterNameChanged: action,
        });
    }

    public filterValueChanged(filterValue: string | undefined) {
        this.filterValue = filterValue;
        if (filterValue === '') this.filterValue = undefined; // для обработки пустого поля
    }

    public filterNameChanged(filterName: string | undefined) {
        this.filterName = filterName;
    }

    public sortDirectionChanged<T>(sortName: ColumnDefinition<T>, sortValue: SortDirection) {
        this.sortBy = sortName as string;
        this.sortDir = switchDirection(sortValue);
    }
}
