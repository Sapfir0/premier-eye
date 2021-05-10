import { isRight } from 'fp-ts/lib/Either';
import { inject, injectable } from 'inversify';
import { action, makeObservable, observable } from 'mobx';
import { BaseInteractionError } from 'services/Errors/BaseInteractionError';
import { ResolvedEither } from 'typings/common';
import StepDataStructure from '../../services/DataStructure/StepDataStructure';
import { socket } from '../../services/Socket';
import { ICameraApiInteractionService, IGalleryApiInteractionService } from '../../services/typings/ApiTypes';
import { definitions } from '../../typings/Dto';
import { TYPES } from '../../typings/types';
import { Map } from 'immutable';
@injectable()
export class SliderStore {
    camera: definitions['Camera'] | null = null;
    imageInfo: definitions['ImageInfo'] | null = null;
    stepMap: Map<string, number> = new StepDataStructure().steps;
    error: BaseInteractionError | null = null;
    stepsStore: StepDataStructure = new StepDataStructure();
    camerasList: definitions['CameraList']['items'] = [];

    private readonly galleryFetcher: IGalleryApiInteractionService;
    private readonly cameraFetcher: ICameraApiInteractionService;

    constructor(
        @inject(TYPES.GalleryApiInteractionService) galleryFetcher: IGalleryApiInteractionService,
        @inject(TYPES.CameraApiInteractionService) cameraFetcher: ICameraApiInteractionService,
    ) {
        this.galleryFetcher = galleryFetcher;
        this.cameraFetcher = cameraFetcher;

        makeObservable(this, {
            changeCurrentStep: action,
            getCameraList: action,
            changeCurrentCamera: action,
            camerasList: observable,
            camera: observable,
            imageInfo: observable,
            error: observable,
        });

        socket.on('infoUpdated', () => {
            if (this.camera !== null) {
                this.changeCurrentCamera(this.camera.id);
            }
        });
    }

    public async getCameraList(): Promise<void> {
        const either: ResolvedEither<definitions['CameraList']> = await this.cameraFetcher.getCamerasList();

        if (isRight(either)) {
            this.camerasList = either.right.items;
        } else {
            this.error = either.left;
        }
    }

    public async changeCurrentStep(cameraId: string, currentStep: number): Promise<void> {
        const filename = this.camera?.images[currentStep].src;
        let either: ResolvedEither<definitions['ImageInfo']>;
        if (filename === undefined) {
            either = await this.galleryFetcher.getInfoImageByIndex(cameraId, currentStep);
        } else {
            either = await this.galleryFetcher.getInfoImage(filename);
        }

        this.stepMap = this.stepsStore.changeStepOnCurrentCamera(cameraId, currentStep);

        if (isRight(either)) {
            this.imageInfo = either.right;
        } else {
            this.error = either.left;
        }
    }

    public async changeCurrentCamera(cameraId: string): Promise<void> {
        const either: ResolvedEither<definitions['Camera']> = await this.cameraFetcher.getImageFromCamera(cameraId);

        if (isRight(either)) {
            this.camera = either.right;
        } else {
            this.error = either.left;
        }
    }
}
