import { injectable } from "inversify";
import { action, observable } from "mobx";


@injectable()
export class AreaMapStore {
    @observable mapUrl: string | null = null

    @action
    public addNewCard = () => {

    }
}