import {ISliderStore} from "../../typings/sliderTypes";
import StepDataStructure from "../../services/DataStructure/StepDataStructure";
import { action, observable } from "mobx";
import { definitions } from "typings/Dto";


export class SliderStore {
    @observable imagesList: Array<string> = []
    @observable imageInfo: definitions['ImageInfo'] | null = null
    @observable currentCameraId: number = 1
    stepMap: Map<number, number> = new Map<number, number>()


    constructor() {
        
    }

    @action
    public changeCurrentStep = (cameraId: number, currentStep: number) => {
        const either: Either<BaseInteractionError, definitions['ImageInfo']> = yield this.galleryFetcher.getInfoImageByIndex(action.payload.cameraId, action.payload.currentStep)

        const parsed = either
            .mapRight((info) => this.actions.setInfoImage(info))
            .mapLeft((error) => this.actions.setError(error))

        yield put(parsed.value)
    }

    @action
    public changeCurrentCamera = (cameraId: number) => {
        
    }

    @action
    public getInfoImage = (src: string) => {
        
    }

    // public *getImagesFromCamera(action: ActionTypePayload<IdPayload, SLIDER_ACTIONS>) {
    //     const either: Either<BaseInteractionError, string[]> = yield this.cameraFetcher.getImageFromCamera(action.payload.id)

    //     const parsed = either
    //         .mapRight((imagesUrl) => this.actions.setImagesUrlFromCamera(imagesUrl))
    //         .mapLeft((error) => this.actions.setError(error))

    //     yield put(parsed.value)
    // }

    // public *getInfoAboutImageFromCameraByFilename(action: ActionTypePayload<SrcPayload, SLIDER_ACTIONS>) {
    //     const either: Either<BaseInteractionError, definitions['ImageInfo']> = yield this.galleryFetcher.getInfoImage(action.payload.src)

    //     const parsed = either
    //         .mapRight((info) => this.actions.setInfoImage(info))
    //         .mapLeft((error) => this.actions.setError(error))

    //     yield put(parsed.value)
    // }



}