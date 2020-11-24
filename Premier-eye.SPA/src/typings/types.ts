import {IApiInteractionService} from "../services/typings/ApiTypes";


const TYPES = {
    ApiHelper: Symbol.for('ApiHelper'),
    BaseInteractionService: Symbol.for('BaseInteractionService'),
    ApiInteractionService: Symbol.for('ApiInteractionService'),
    UrlService: Symbol.for('UrlService'),
    GalleryApiInteractionService: Symbol.for('GalleryApiInteractionService'),
    CameraApiInteractionService: Symbol.for('CameraApiInteractionService'),

    SliderStore: Symbol.for('SliderStore'),


}

export { TYPES }
