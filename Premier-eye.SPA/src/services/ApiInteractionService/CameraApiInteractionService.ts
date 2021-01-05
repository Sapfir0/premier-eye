import { definitions } from 'typings/Dto';
import { ApiRoutes } from '../../config/apiRoutes';
import ApiInteractionService from '../ApiInteractionService';
import { ICameraApiInteractionService } from '../typings/ApiTypes';

export default class CameraApiInteractionService extends ApiInteractionService implements ICameraApiInteractionService {
    public getImageFromCamera = (cameraId: string) => {
        return this.get(ApiRoutes.CAMERA.GET_ALL_IMAGES_FROM_CAMERA(cameraId));
    };

    public getCamerasList = () => {
        return this.get(ApiRoutes.CAMERA.GET_CAMERAS_LIST);
    };

    public addNewCamera = (cameraDto: definitions['DTOCamera']) => {
        return this.put(ApiRoutes.CAMERA.CAMERA, cameraDto);
    };
}
