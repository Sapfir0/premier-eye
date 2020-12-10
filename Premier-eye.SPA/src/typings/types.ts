import {IApiInteractionService} from "../services/typings/ApiTypes";


const TYPES = {
    ApiHelper: Symbol.for('ApiHelper'),
    BaseInteractionService: Symbol.for('BaseInteractionService'),
    ApiInteractionService: Symbol.for('ApiInteractionService'),
    GalleryApiInteractionService: Symbol.for('GalleryApiInteractionService'),
    CameraApiInteractionService: Symbol.for('CameraApiInteractionService'),

    SliderStore: Symbol.for('SliderStore'),
    ImageInfoStore: Symbol.for('ImageInfoStore'),
    AreaMapStore: Symbol.for('AreaMapStore'),

}

export { TYPES }
