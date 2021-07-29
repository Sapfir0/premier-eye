import { ApiInteractionService } from 'api_interaction_services';
import { definitions } from 'typings/Dto';
import { ApiRoutes, API_URL } from '../../config/apiRoutes';

export default class EventApiInteractionService extends ApiInteractionService {
    constructor() {
        super(API_URL);
    }

    public getEventsList = (sortBy?: string, sortDir?: string, filterBy?: string, filterValue?: string) => {
        return this.get<{ data: definitions['DTOLog'][] }>(ApiRoutes.EVENT.LOG, {}, API_URL, {
            params: {
                sortDir,
                sortBy,
                filterBy,
                filterValue,
            },
        });
    };
}
