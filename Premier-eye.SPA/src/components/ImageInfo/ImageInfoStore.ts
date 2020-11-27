import { Range } from "immutable"
import {makeObservable, observable} from "mobx"


export interface ICollapse {
    id: string,
    open: boolean
}


export class ImageInfoStore<TCollapsedData extends {id: string}> {
    @observable collapses: Array<ICollapse & TCollapsedData> = []

    constructor() {
        makeObservable(this)
    }

    emptyCollapses(countOfCollapses: number) {
        this.collapses = Range(0, countOfCollapses).map((el) => ({ id: el.toString(), open: false })).toArray() as Array<ICollapse & TCollapsedData>
        return this.collapses
    }

    setCollapses(existingData: TCollapsedData[]) {
        this.collapses = existingData.map((el) => ({...el, open: false}))
        return this.collapses
    }

    toggleCollapse(id: string) {
        this.collapses = this.collapses.map((item: ICollapse) =>
            item.id === id ? { ...item, open: !item.open } : item
        ) as Array<ICollapse & TCollapsedData>
    }

}
