import {ICameraApiInteractionService} from "../typings/ApiTypes";
import ApiInteractionService from "../ApiInteractionService";
import {ApiRoutes} from "../../config/apiRoutes";
import { definitions } from "typings/Dto";


export default class CameraApiInteractionService extends ApiInteractionService implements ICameraApiInteractionService {
    public getImageFromCamera = (cameraId: string) => {
        return this.get(ApiRoutes.CAMERA.GET_ALL_IMAGES_FROM_CAMERA(cameraId))
    }

    public getCamerasList = () => {
        return this.get(ApiRoutes.CAMERA.GET_CAMERAS_LIST)
    }

    public addNewCamera = (cameraDto: definitions['CameraDTO']) => {
        return this.put(ApiRoutes.CAMERA.CAMERA, cameraDto)
    }
}