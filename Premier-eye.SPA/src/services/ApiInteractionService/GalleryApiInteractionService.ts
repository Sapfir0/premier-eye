import {IGalleryApiInteractionService} from "../typings/ApiTypes";
import ApiInteractionService from "../ApiInteractionService";
import {API_URL, ApiRoutes} from "../../config/apiRoutes";


export default class GalleryApiInteractionService extends ApiInteractionService implements IGalleryApiInteractionService {
    public getImage = (imageId: string) => {
        return this.get(ApiRoutes.GALLERY.GET_IMAGE(imageId))
    }
    public getInfoImage = (src: string) => {
        return this.get(ApiRoutes.IMAGE_INFO.GET_INFO_IMAGE(src))
    }

    public getInfoImageByIndex = (cameraId: string, currentImageIndex: number) => {
        return this.get(ApiRoutes.IMAGE_INFO.GET_IMAGE_INFO_BY_INDEX, {}, API_URL, {params: {cameraId: cameraId, indexOfImage: currentImageIndex}})
    }

    public getAllImages = () => {
        return this.get(ApiRoutes.GALLERY.GET_ALL_IMAGES)
    }
}