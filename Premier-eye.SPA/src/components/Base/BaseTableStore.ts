import { injectable } from 'inversify';
import { action, makeObservable, observable } from 'mobx';
import { switchDirection } from '../../services/utils';
import { ColumnDefinition, SortDirection } from 'typings/table';

@injectable()
export class BaseTableStore {
    sortDir: SortDirection = 'desc';
    sortBy = 'id';

    constructor() {
        makeObservable(this, {
            filterValueChanged: action,
            sortDirectionChanged: action,
            sortDir: observable,
            sortBy: observable,
        });
    }

    public filterValueChanged(filterName: string, filterValue: string) {}

    public sortDirectionChanged<T>(sortName: ColumnDefinition<T>, sortValue: SortDirection) {
        this.sortBy = sortName as string;
        this.sortDir = switchDirection(sortValue);
    }
}
