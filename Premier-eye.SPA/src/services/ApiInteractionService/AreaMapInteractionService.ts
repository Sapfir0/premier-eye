import { ApiInteractionService } from 'api_interaction_services';
import { ApiRoutes, API_URL } from '../../config/apiRoutes';

export class AreaMapApiInteractionService extends ApiInteractionService {
    constructor() {
        super(API_URL);
    }

    public getObjects = () => {
        return this.get(ApiRoutes.AREA_MAP.OBJECTS);
    };
}
