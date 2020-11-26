import { Range } from "immutable"
import { observable } from "mobx"


export interface ICollapse {
    id: number,
    open: boolean
}

export class ImageInfoStore<TCollapsedData extends {}> {
    @observable collapses: (TCollapsedData & ICollapse)[] = []

    constructor() {

    }

    setCollapses(countOfCollapses: number) {
        this.collapses = Range(0, countOfCollapses).map((el) => ({ id: el, open: false })).toArray()
    }

    toggleCollapse(id: number) {
        this.collapses.map((item: ICollapse) =>
            item.id === id ? { ...item, open: !item.open } : item
        )
    }

}
