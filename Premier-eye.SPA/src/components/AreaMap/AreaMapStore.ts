import { injectable } from 'inversify';
import { observable } from 'mobx';

@injectable()
export class AreaMapStore {
    @observable mapUrl: string | null = null;
}
