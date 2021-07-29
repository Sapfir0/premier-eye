import { ApiInteractionService } from 'api_interaction_services';
import { inject } from 'inversify';
import { definitions } from '../../typings/Dto';
import { TYPES } from '../../typings/types';
import { ApiRoutes, API_URL } from '../../config/apiRoutes';
import { ICameraApiInteractionService } from '../typings/ApiTypes';

export default class CameraApiInteractionService implements ICameraApiInteractionService {
    constructor(@inject(TYPES.ApiInteractionService) protected _apiService: ApiInteractionService) {}

    public getImageFromCamera = (cameraId: string) => {
        return this._apiService.get(ApiRoutes.CAMERA.CURRENT(cameraId));
    };

    public getCamerasList = (sortBy?: string, sortDir?: string, filterBy?: string, filterValue?: string) => {
        return this._apiService.get(ApiRoutes.CAMERA.GET_CAMERAS_LIST, {}, API_URL, {
            params: {
                sortDir,
                sortBy,
                filterBy,
                filterValue,
            },
        });
    };

    public addNewCamera = (cameraDto: definitions['CameraDto']) => {
        return this._apiService.post(ApiRoutes.CAMERA.CURRENT(cameraDto.name), cameraDto);
    };
}
