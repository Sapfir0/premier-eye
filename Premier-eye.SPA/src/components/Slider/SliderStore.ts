import {action, makeObservable, observable, toJS} from "mobx";
import { definitions } from "../../typings/Dto";
import { Either } from "@sweet-monads/either";
import { BaseInteractionError } from "services/Errors/BaseInteractionError";
import {inject, injectable} from "inversify";
import { TYPES } from "../../typings/types";
import { ICameraApiInteractionService, IGalleryApiInteractionService } from "services/typings/ApiTypes";
import {act} from "react-dom/test-utils";
import StepDataStructure from "../../services/DataStructure/StepDataStructure";


@injectable()
export class SliderStore {
    @observable imagesList: Array<string> = []
    @observable imageInfo: definitions['ImageInfo'] | null = null
    @observable currentCameraId: number = 1
    stepMap: Map<number, number> = new StepDataStructure().steps
    @observable errors: BaseInteractionError | null = null
    stepsStore: StepDataStructure = new StepDataStructure()

    private readonly galleryFetcher: IGalleryApiInteractionService
    private readonly cameraFetcher: ICameraApiInteractionService

    constructor(
        @inject(TYPES.GalleryApiInteractionService) galleryFetcher: IGalleryApiInteractionService,
        @inject(TYPES.CameraApiInteractionService) cameraFetcher: ICameraApiInteractionService,
    ) {
        this.galleryFetcher = galleryFetcher
        this.cameraFetcher = cameraFetcher
        makeObservable(this)
    }

    @action
    public changeCurrentStep = async (cameraId: number, currentStep: number) => {
        const either: Either<BaseInteractionError, definitions['ImageInfo']> = await this.galleryFetcher.getInfoImageByIndex(cameraId, currentStep)
        this.stepMap = this.stepsStore.changeStepOnCurrentCamera(cameraId, currentStep)

        if (either.isLeft()) {
            this.errors = either.value
        } else {
            this.imageInfo = toJS(either.value)
        }

    }

    @action
    public changeCurrentCamera = async (cameraId: number) => {
        const either: Either<BaseInteractionError, string[]> = await this.cameraFetcher.getImageFromCamera(cameraId)
        this.currentCameraId = cameraId
        if (either.isLeft()) {
            this.errors = either.value
        } else {
            this.imagesList = either.value
        }
    }

    @action
    public getInfoImage = async (src: string) => {
        const either: Either<BaseInteractionError, definitions['ImageInfo']> = await this.galleryFetcher.getInfoImage(src)

        if (either.isLeft()) {
            this.errors = either.value
        } else {
            this.imageInfo = toJS(either.value)
        }
    }




}