import { ApiInteractionService } from 'api_interaction_services';
import { inject } from 'inversify';
import { definitions } from '../../typings/Dto';
import { TYPES } from '../../typings/types';
import { ApiRoutes, API_URL } from '../../config/apiRoutes';

export default class EventApiInteractionService  {
    constructor(@inject(TYPES.ApiInteractionService) protected _apiService: ApiInteractionService) {}


    public getEventsList = (sortBy?: string, sortDir?: string, filterBy?: string, filterValue?: string) => {
        return this._apiService.get<{ data: definitions['DTOLog'][] }>(ApiRoutes.EVENT.LOG, {}, API_URL, {
            params: {
                sortDir,
                sortBy,
                filterBy,
                filterValue,
            },
        });
    };
}
