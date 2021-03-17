import { isRight } from 'fp-ts/lib/Either';
import { inject, injectable } from 'inversify';
import { action, makeObservable, observable } from 'mobx';
import { ICameraApiInteractionService } from 'services/typings/ApiTypes';
import { AreaMapApiInteractionService } from '../../services/ApiInteractionService/AreaMapInteractionService';
import { ResolvedEither } from '../../typings/common';
import { definitions } from '../../typings/Dto';
import { TYPES } from '../../typings/types';

@injectable()
export class AreaMapStore {
    objects = [];
    private readonly areaMapFetcher: AreaMapApiInteractionService;
    private readonly cameraFetcher: ICameraApiInteractionService;
    camerasList: definitions['CameraList'] = { items: [] };

    constructor(
        @inject(TYPES.AreaMapApiInteractionService) areaFetcher: AreaMapApiInteractionService,
        @inject(TYPES.CameraApiInteractionService) cameraFetcher: ICameraApiInteractionService,
    ) {
        this.areaMapFetcher = areaFetcher;
        this.cameraFetcher = cameraFetcher;
        makeObservable(this, {
            getObjectList: action,
            getCameraList: action,
            camerasList: observable,
            objects: observable,
        });
    }

    public async getObjectList(): Promise<void> {
        const either: ResolvedEither<any> = await this.areaMapFetcher.getObjects();

        if (isRight(either)) {
            this.objects = either.right;
        }
    }

    public async getCameraList(): Promise<void> {
        const either: ResolvedEither<definitions['CameraList']> = await this.cameraFetcher.getCamerasList();

        if (isRight(either)) {
            this.camerasList = either.right;
        }
    }
}
