import {action, makeObservable, observable, runInAction, toJS} from "mobx";
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
    @observable camerasList: definitions['CameraList'] = {items: []}

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
    public async getCameraList() {
        const either: Either<BaseInteractionError, definitions['CameraList']> = await this.cameraFetcher.getCamerasList()
        
        runInAction(() => {
            if (either.isLeft()) {
                this.errors = either.value
            } else {
                this.camerasList = either.value
                console.log(this.camerasList);
                
            }    
        })
    }

    @action
    public async changeCurrentStep(cameraId: number, currentStep: number) {
        const either: Either<BaseInteractionError, definitions['ImageInfo']> = await this.galleryFetcher.getInfoImageByIndex(cameraId, currentStep)
        
        runInAction(() => {
            this.stepMap = this.stepsStore.changeStepOnCurrentCamera(cameraId, currentStep)

            if (either.isLeft()) {
                this.errors = either.value
            } else {
                this.imageInfo = either.value
            }    
        })
        
      
    }

    @action
    public async changeCurrentCamera(cameraId: number) {
        const either: Either<BaseInteractionError, {items: string[]}> = await this.cameraFetcher.getImageFromCamera(cameraId)

        runInAction(() => {
            this.currentCameraId = cameraId
            if (either.isLeft()) {
                this.errors = either.value
            } else {
                console.log(either.value)
                this.imagesList = either.value.items
            }
        })

    }

    @action // deprecated
    public async getInfoImage(src: string) { // пока не используем
        const either: Either<BaseInteractionError, definitions['ImageInfo']> = await this.galleryFetcher.getInfoImage(src)

        runInAction(() => {
            if (either.isLeft()) {
                this.errors = either.value
            } else {
                this.imageInfo = either.value
            }
        })

    }




}