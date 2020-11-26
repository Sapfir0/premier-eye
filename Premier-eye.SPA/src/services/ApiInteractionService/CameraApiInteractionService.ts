import {ICameraApiInteractionService} from "../typings/ApiTypes";
import ApiInteractionService from "../ApiInteractionService";
import {ApiRoutes} from "../../config/apiRoutes";


export default class CameraApiInteractionService extends ApiInteractionService implements ICameraApiInteractionService {
    public getImageFromCamera = (cameraId: number) => {
        return this.get(ApiRoutes.CAMERA.GET_ALL_IMAGES_FROM_CAMERA(cameraId))
    }

    public getCamerasList = () => {
        return this.get(ApiRoutes.CAMERA.GET_CAMERAS_LIST)
    }
}