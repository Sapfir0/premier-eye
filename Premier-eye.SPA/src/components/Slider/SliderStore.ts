import { action, observable } from "mobx";
import { definitions } from "../../typings/Dto";
import { Either } from "@sweet-monads/either";
import { BaseInteractionError } from "services/Errors/BaseInteractionError";
import {inject, injectable} from "inversify";
import { TYPES } from "../../typings/types";
import { ICameraApiInteractionService, IGalleryApiInteractionService } from "services/typings/ApiTypes";
import {act} from "react-dom/test-utils";


@injectable()
export class SliderStore {
    @observable imagesList: Array<string> = []
    @observable imageInfo: definitions['ImageInfo'] | null = null
    @observable currentCameraId: number = 1
    stepMap: Map<number, number> = new Map<number, number>()
    @observable errors: BaseInteractionError | null = null

    private readonly galleryFetcher: IGalleryApiInteractionService
    private readonly cameraFetcher: ICameraApiInteractionService

    constructor(
        @inject(TYPES.GalleryApiInteractionService) galleryFetcher: IGalleryApiInteractionService,
        @inject(TYPES.CameraApiInteractionService) cameraFetcher: ICameraApiInteractionService,
    ) {
        this.galleryFetcher = galleryFetcher
        this.cameraFetcher = cameraFetcher
    }

    @action
    public changeCurrentStep = async (cameraId: number, currentStep: number) => {
        const either: Either<BaseInteractionError, definitions['ImageInfo']> = await this.galleryFetcher.getInfoImageByIndex(cameraId, currentStep)

        if (either.isLeft()) {
            this.errors = either.value
        } else {
            this.imageInfo = either.value
        }

    }

    @action
    public changeCurrentCamera = async (cameraId: number) => {
        const either: Either<BaseInteractionError, string[]> = await this.cameraFetcher.getImageFromCamera(cameraId)
            
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
            this.imageInfo = either.value
        }
    }

    @action
    public getImagesFromCamera = async (cameraId: number) => {

    }



}