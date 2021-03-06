import { isRight } from 'fp-ts/lib/These';
import { inject, injectable } from 'inversify';
import { action, makeObservable, observable } from 'mobx';
import { definitions } from 'typings/Dto';
import EventApiInteractionService from '../../services/ApiInteractionService/EventApiInteractionService';
import { TYPES } from '../../typings/types';

@injectable()
export class CameraLoggerStore {
    private readonly eventFetcher: EventApiInteractionService;
    public events: definitions['DTOLog'][] | undefined = undefined;

    constructor(@inject(TYPES.EventApiInteractionService) eventFetcher: EventApiInteractionService) {
        this.eventFetcher = eventFetcher;
        makeObservable(this, { getLogs: action, events: observable });
    }

    public getLogs = async () => {
        const either = await this.eventFetcher.getEventsList();
        if (isRight(either)) {
            this.events = either.right.data;
        }
        console.log(this.events);
    };
}
