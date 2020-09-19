import {IGalleryApiInteractionService} from "../typings/ApiTypes";
import ApiInteractionService from "../ApiInteractionService";
import {ApiRoutes} from "../../config/apiRoutes";


export default class GalleryApiInteractionService extends ApiInteractionService implements IGalleryApiInteractionService {
    public getImage = (imageId: string) => {
        return this.get(ApiRoutes.GALLERY.GET_IMAGE(imageId))
    }
    public getInfoImage = (src: string) => {
        return this.get(ApiRoutes.GALLERY.GET_INFO_IMAGE(src))
    }

    public getAllImages = () => {
        return this.get(ApiRoutes.GALLERY.GET_ALL_IMAGES)
    }
}