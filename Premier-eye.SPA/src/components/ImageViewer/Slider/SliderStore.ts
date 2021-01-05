import { Either, isLeft } from 'fp-ts/lib/Either';
import { inject, injectable } from 'inversify';
import { action, makeObservable, observable, runInAction } from 'mobx';
import { BaseInteractionError } from 'services/Errors/BaseInteractionError';
import { ICameraApiInteractionService, IGalleryApiInteractionService } from 'services/typings/ApiTypes';
import StepDataStructure from '../../../services/DataStructure/StepDataStructure';
import { definitions } from '../../../typings/Dto';
import { TYPES } from '../../../typings/types';

@injectable()
export class SliderStore {
    @observable camera: definitions['Camera'] | null = null;
    @observable imageInfo: definitions['ImageInfo'] | null = null;
    stepMap: Map<string, number> = new StepDataStructure().steps;
    @observable errors: BaseInteractionError[] = [];
    stepsStore: StepDataStructure = new StepDataStructure();
    @observable camerasList: definitions['CameraList'] = { items: [] };

    private readonly galleryFetcher: IGalleryApiInteractionService;
    private readonly cameraFetcher: ICameraApiInteractionService;

    constructor(
        @inject(TYPES.GalleryApiInteractionService) galleryFetcher: IGalleryApiInteractionService,
        @inject(TYPES.CameraApiInteractionService) cameraFetcher: ICameraApiInteractionService,
    ) {
        this.galleryFetcher = galleryFetcher;
        this.cameraFetcher = cameraFetcher;
        makeObservable(this);
    }

    // зациклить вызов камера лист каждые 2.9 сек

    @action
    public async getCameraList() {
        const either: Either<
            BaseInteractionError,
            definitions['CameraList']
        > = await this.cameraFetcher.getCamerasList();

        runInAction(() => {
            if (isLeft(either)) {
                this.errors.push(either.left);
            } else {
                this.camerasList = either.right;
                console.log(this.camerasList);
            }
        });
    }

    @action
    public async changeCurrentStep(cameraId: string, currentStep: number) {
        const either: Either<
            BaseInteractionError,
            definitions['ImageInfo']
        > = await this.galleryFetcher.getInfoImageByIndex(cameraId, currentStep);

        runInAction(() => {
            this.stepMap = this.stepsStore.changeStepOnCurrentCamera(cameraId, currentStep);

            if (isLeft(either)) {
                this.errors.push(either.left);
            } else {
                this.imageInfo = either.right;
            }
        });
    }

    @action
    public async changeCurrentCamera(cameraId: string) {
        const either: Either<BaseInteractionError, definitions['Camera']> = await this.cameraFetcher.getImageFromCamera(
            cameraId,
        );

        runInAction(() => {
            if (isLeft(either)) {
                this.errors.push(either.left);
            } else {
                this.camera = either.right;
                // console.log(this.camera.images)
            }
        });
    }

    @action // deprecated
    public async getInfoImage(src: string) {
        // пока не используем
        const either: Either<BaseInteractionError, definitions['ImageInfo']> = await this.galleryFetcher.getInfoImage(
            src,
        );

        runInAction(() => {
            if (isLeft(either)) {
                this.errors.push(either.left);
            } else {
                this.imageInfo = either.right;
            }
        });
    }
}
