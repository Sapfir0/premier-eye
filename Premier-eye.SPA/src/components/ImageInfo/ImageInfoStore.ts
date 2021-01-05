import { Range } from 'immutable';
import { injectable } from 'inversify';
import { action, makeObservable, observable } from 'mobx';

export interface ICollapse {
    id: string;
    open: boolean;
}

@injectable()
export class ImageInfoStore<TCollapsedData extends { id: string }> {
    @observable collapses: Array<ICollapse & TCollapsedData> = [];

    constructor() {
        makeObservable(this);
    }

    @action
    emptyCollapses(countOfCollapses: number) {
        this.collapses = Range(0, countOfCollapses)
            .map((el) => ({ id: el.toString(), open: false }))
            .toArray() as Array<ICollapse & TCollapsedData>;
        return this.collapses;
    }

    @action
    setCollapses(existingData: TCollapsedData[]) {
        this.collapses = existingData.map((el) => ({ ...el, open: false }));
        return this.collapses;
    }

    @action
    toggleCollapse(id: string) {
        this.collapses = this.collapses.map((item: ICollapse) =>
            item.id === id ? { ...item, open: !item.open } : item,
        ) as Array<ICollapse & TCollapsedData>;
    }
}
