import { definitions } from 'typings/Dto';
import { ApiRoutes, API_URL } from '../../config/apiRoutes';
import ApiInteractionService from '../ApiInteractionService';

export default class EventApiInteractionService extends ApiInteractionService {
    public getEventsList = (sortBy: string, sortDir: string) => {
        return this.get<{ data: definitions['DTOLog'][] }>(ApiRoutes.EVENT.LOG, {}, API_URL, {
            params: {
                sortDir,
                sortBy,
            },
        });
    };
}
