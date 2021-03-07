import { injectable } from 'inversify';
import { action, makeObservable, observable } from 'mobx';
import { switchDirection } from '../../services/utils';
import { SortDirection } from 'typings/table';

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

    public sortDirectionChanged(sortName: string, sortValue: SortDirection) {
        console.log('called base sort');
        this.sortBy = sortName;
        this.sortDir = switchDirection(sortValue);
    }
}
