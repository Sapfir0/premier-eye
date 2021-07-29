import { ApiInteractionService } from 'api_interaction_services';
import { inject } from 'inversify';
import { TYPES } from '../../typings/types';
import { ApiRoutes } from '../../config/apiRoutes';

export class AreaMapApiInteractionService  {
    constructor(@inject(TYPES.ApiInteractionService) protected _apiService: ApiInteractionService) {}

    public getObjects = () => {
        return this._apiService.get(ApiRoutes.AREA_MAP.OBJECTS);
    };
}
