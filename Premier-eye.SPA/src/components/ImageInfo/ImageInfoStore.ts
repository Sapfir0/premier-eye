import { Range } from 'immutable';
import { injectable } from 'inversify';
import { action, makeObservable, observable } from 'mobx';

export interface ICollapse {
    id: string;
    open: boolean;
}

@injectable()
export class ImageInfoStore<TCollapsedData extends { id: string }> {
    collapses: Array<ICollapse & TCollapsedData> = [];

    constructor() {
        makeObservable(this, {
            collapses: observable,
            setCollapses: action,
            toggleCollapse: action,
        });
    }

    public setCollapses(existingData: TCollapsedData[]): void {
        this.collapses = existingData.map((el) => ({ ...el, open: false }));
    }

    public toggleCollapse(id: string): void {
        this.collapses = this.collapses.map((item) => (item.id === id ? { ...item, open: !item.open } : item));
    }
}
