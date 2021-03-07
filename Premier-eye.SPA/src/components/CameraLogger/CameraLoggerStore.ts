import { isRight } from 'fp-ts/lib/These';
import { inject, injectable } from 'inversify';
import { action, makeObservable, observable } from 'mobx';
import { definitions } from 'typings/Dto';
import { ColumnDefinition, SortDirection } from 'typings/table';
import { BaseTableStore } from '../../components/Base/BaseTableStore';
import EventApiInteractionService from '../../services/ApiInteractionService/EventApiInteractionService';
import { TYPES } from '../../typings/types';

@injectable()
export class CameraLoggerStore extends BaseTableStore {
    private readonly eventFetcher: EventApiInteractionService;
    public events: definitions['DTOLog'][] | undefined = undefined;

    constructor(@inject(TYPES.EventApiInteractionService) eventFetcher: EventApiInteractionService) {
        super();
        this.eventFetcher = eventFetcher;
        makeObservable(this, { getLogs: action, events: observable });
    }

    public sortDirectionChanged<T>(sortBy: ColumnDefinition<T>, sortDir: SortDirection) {
        super.sortDirectionChanged(sortBy, sortDir);
        this.getLogs(sortBy as string, sortDir);
    }

    public getLogs = async (sortBy?: string, sortDir?: string) => {
        const either = await this.eventFetcher.getEventsList(sortBy, sortDir);
        if (isRight(either)) {
            this.events = either.right.data;
        }
    };
}
