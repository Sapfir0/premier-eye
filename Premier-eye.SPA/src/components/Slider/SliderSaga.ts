import {push} from "connected-react-router";
import {inject, injectable} from "inversify";
import {TYPES} from "../../typings/types";
import {ActionTypePayload, IdPayload} from "../../typings/common";
import {ICameraApiInteractionService, IGalleryApiInteractionService} from "../../services/typings/ApiTypes";
import {ISliderPrivateAction} from "../../typings/IAction";
import {Either} from "@sweet-monads/either";
import {BaseInteractionError} from "../../services/Errors/BaseInteractionError";
import {ISliderSaga} from "../../typings/ISaga";
import {GET_IMAGES_FROM_CAMERA, GET_INFO_IMAGE, SLIDER_ACTIONS} from "../../store/actionNames/sliderActionNames";
import {SliderBasePayload, SrcPayload} from "../../typings/sliderTypes";
import {put, takeEvery } from "redux-saga/effects";
import {IImageInfo} from "../ImageInfo/IImageInfo";


@injectable()
export default class SliderSaga implements ISliderSaga {
    private readonly galleryFetcher: IGalleryApiInteractionService
    private readonly actions: ISliderPrivateAction
    private readonly cameraFetcher: ICameraApiInteractionService

    constructor(
        @inject(TYPES.GalleryApiInteractionService) galleryFetcher: IGalleryApiInteractionService,
        @inject(TYPES.CameraApiInteractionService) cameraFetcher: ICameraApiInteractionService,
        @inject(TYPES.SliderAction) actions: ISliderPrivateAction,
    ) {
        this.actions = actions
        this.galleryFetcher = galleryFetcher
        this.cameraFetcher = cameraFetcher

        this.getImagesFromCamera = this.getImagesFromCamera.bind(this)
        this.getInfoAboutImageFromCamera = this.getInfoAboutImageFromCamera.bind(this)

    }

    public *getImagesFromCamera(action: ActionTypePayload<IdPayload, SLIDER_ACTIONS>) {
        const either: Either<BaseInteractionError, string[]> = yield this.cameraFetcher.getImageFromCamera(action.payload.id)

        const parsed = either
            .mapRight((imagesUrl) => this.actions.setImagesUrlFromCamera(imagesUrl))
            .mapLeft((error) => this.actions.setError(error))

        yield put(parsed.value)
    }

    public *getInfoAboutImageFromCamera(action: ActionTypePayload<SrcPayload, SLIDER_ACTIONS>) {
        const either: Either<BaseInteractionError, IImageInfo> = yield this.galleryFetcher.getInfoImage(action.payload.src)

        const parsed = either
            .mapRight((info) => this.actions.setInfoImage(info))
            .mapLeft((error) => this.actions.setError(error))

        yield put(parsed.value)
    }

    public *watch(): Generator {
        yield takeEvery(GET_IMAGES_FROM_CAMERA, this.getImagesFromCamera)
        yield takeEvery(GET_INFO_IMAGE, this.getInfoAboutImageFromCamera)
    }

}
