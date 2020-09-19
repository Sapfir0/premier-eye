import {IApiInteractionService} from "../services/typings/ApiTypes";


const TYPES = {
    ApiHelper: Symbol.for('ApiHelper'),
    BaseInteractionService: Symbol.for('BaseInteractionService'),
    ApiInteractionService: Symbol.for('ApiInteractionService'),
    UrlService: Symbol.for('UrlService'),
    GalleryApiInteractionService: Symbol.for('GalleryApiInteractionService'),
    CameraApiInteractionService: Symbol.for('CameraApiInteractionService'),

    SliderAction: Symbol.for('SliderAction'),
    SliderReducer: Symbol.for('SliderReducer'),
    SliderSaga: Symbol.for('SliderSaga'),

}

export { TYPES }
