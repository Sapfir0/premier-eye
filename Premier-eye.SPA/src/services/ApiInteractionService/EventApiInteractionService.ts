import { definitions } from 'typings/Dto';
import { ApiRoutes } from '../../config/apiRoutes';
import ApiInteractionService from '../ApiInteractionService';

export default class EventApiInteractionService extends ApiInteractionService {
    public getEventsList = () => {
        return this.get<{ data: definitions['DTOLog'][] }>(ApiRoutes.EVENT.LOG);
    };
}
