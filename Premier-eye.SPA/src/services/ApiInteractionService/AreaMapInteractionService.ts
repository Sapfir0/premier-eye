import { ApiRoutes } from '../../config/apiRoutes';
import ApiInteractionService from '../ApiInteractionService';

export class AreaMapApiInteractionService extends ApiInteractionService {
    public getObjects = () => {
        return this.get(ApiRoutes.AREA_MAP.OBJECTS);
    };
}
