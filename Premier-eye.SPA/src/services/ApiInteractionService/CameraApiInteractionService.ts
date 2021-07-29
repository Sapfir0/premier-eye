import { ApiInteractionService } from 'api_interaction_services';
import { definitions } from 'typings/Dto';
import { ApiRoutes, API_URL } from '../../config/apiRoutes';
import { ICameraApiInteractionService } from '../typings/ApiTypes';

export default class CameraApiInteractionService extends ApiInteractionService implements ICameraApiInteractionService {
    constructor() {
        super(API_URL);
    }

    public getImageFromCamera = (cameraId: string) => {
        return this.get(ApiRoutes.CAMERA.CURRENT(cameraId));
    };

    public getCamerasList = (sortBy?: string, sortDir?: string, filterBy?: string, filterValue?: string) => {
        return this.get(ApiRoutes.CAMERA.GET_CAMERAS_LIST, {}, API_URL, {
            params: {
                sortDir,
                sortBy,
                filterBy,
                filterValue,
            },
        });
    };

    public addNewCamera = (cameraDto: definitions['CameraDto']) => {
        return this.post(ApiRoutes.CAMERA.CURRENT(cameraDto.name), cameraDto);
    };
}
