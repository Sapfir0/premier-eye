import { ApiInteractionService } from 'api_interaction_services';
import { ApiRoutes, API_URL } from '../../config/apiRoutes';
import { IGalleryApiInteractionService } from '../typings/ApiTypes';

export default class GalleryApiInteractionService
    extends ApiInteractionService
    implements IGalleryApiInteractionService {
    constructor() {
        super(API_URL);
    }

    public getImage = (imageId: string) => {
        return this.get(ApiRoutes.GALLERY.GET_IMAGE(imageId));
    };
    public getInfoImage = (src: string) => {
        return this.get(ApiRoutes.IMAGE_INFO.GET_INFO_IMAGE(src));
    };

    public getInfoImageByIndex = (cameraId: string, currentImageIndex: number) => {
        return this.get(ApiRoutes.IMAGE_INFO.GET_IMAGE_INFO_BY_INDEX, {}, API_URL, {
            params: { cameraId: cameraId, indexOfImage: currentImageIndex },
        });
    };

    public getAllImages = () => {
        return this.get(ApiRoutes.GALLERY.GET_ALL_IMAGES);
    };
}
