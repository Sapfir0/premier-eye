import { ApiInteractionService } from 'api_interaction_services';
import { inject } from 'inversify';
import { TYPES } from '../../typings/types';
import { ApiRoutes, API_URL } from '../../config/apiRoutes';
import { IGalleryApiInteractionService } from '../typings/ApiTypes';

export default class GalleryApiInteractionService implements IGalleryApiInteractionService {
    constructor(@inject(TYPES.ApiInteractionService) protected _apiService: ApiInteractionService) {}

    public getImage = (imageId: string) => {
        return this._apiService.get(ApiRoutes.GALLERY.GET_IMAGE(imageId));
    };
    public getInfoImage = (src: string) => {
        return this._apiService.get(ApiRoutes.IMAGE_INFO.GET_INFO_IMAGE(src));
    };

    public getInfoImageByIndex = (cameraId: string, currentImageIndex: number) => {
        return this._apiService.get(ApiRoutes.IMAGE_INFO.GET_IMAGE_INFO_BY_INDEX, {}, API_URL, {
            params: { cameraId: cameraId, indexOfImage: currentImageIndex },
        });
    };

    public getAllImages = () => {
        return this._apiService.get(ApiRoutes.GALLERY.GET_ALL_IMAGES);
    };
}
