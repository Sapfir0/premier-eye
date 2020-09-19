import {ICameraApiInteractionService} from "../typings/ApiTypes";
import ApiInteractionService from "../ApiInteractionService";
import {ApiRoutes} from "../../config/apiRoutes";


export default class CameraApiInteractionService extends ApiInteractionService implements ICameraApiInteractionService {
    public getImageFromCamera = (cameraId: number) => {
        return this.get(ApiRoutes.GALLERY.GET_IMAGES_FROM_CAMERA(cameraId))
    }
    public getCameraInfo = (cameraId: number) => {
        return this.get(ApiRoutes.GALLERY.GET_CAMERA_INFO(cameraId))
    }
}