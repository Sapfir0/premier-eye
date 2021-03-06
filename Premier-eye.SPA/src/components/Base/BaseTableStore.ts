import { injectable } from 'inversify';
import { makeObservable } from 'mobx';

@injectable()
export class BaseTableStore {
    constructor() {
        makeObservable(this, {});
    }

    protected filterValueChanged(filterName: string, filterValue: string) {}

    protected sortDirectionChanged(sortName: string, sortValue: string) {}
}
