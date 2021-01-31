import { Either, isLeft } from 'fp-ts/lib/Either';
import { inject, injectable } from 'inversify';
import { action, makeObservable, observable, runInAction } from 'mobx';
import { BaseInteractionError } from 'services/Errors/BaseInteractionError';
import { ICameraApiInteractionService } from 'services/typings/ApiTypes';
import { definitions } from '../../typings/Dto';
import { TYPES } from '../../typings/types';

@injectable()
export class SettingsStore {
    @observable errors: BaseInteractionError[] = [];
    @observable camerasList: definitions['CameraList'] = { items: [] };

    nameOfCamera = '';
    @observable isCreating = false;

    private readonly cameraFetcher: ICameraApiInteractionService;

    constructor(@inject(TYPES.CameraApiInteractionService) cameraFetcher: ICameraApiInteractionService) {
        this.cameraFetcher = cameraFetcher;
        makeObservable(this);
    }

    @action
    public startCreatingNewCamera = () => {
        this.isCreating = true;
    };

    @action
    public stopCreatingNewCamera = () => {
        this.isCreating = false;
    };

    @action
    public async addNewCamera(cameraDto: definitions['DTOCamera']) {
        const either: Either<BaseInteractionError, definitions['DTOCamera']> = await this.cameraFetcher.addNewCamera(
            cameraDto,
        );

        runInAction(() => {
            if (isLeft(either)) {
                this.errors.push(either.left);
            } else {
                // this.getCameraList();
            }
        });
    }
}
