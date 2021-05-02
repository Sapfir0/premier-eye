import { Either, isLeft } from 'fp-ts/lib/Either';
import { inject, injectable } from 'inversify';
import { action, makeObservable, observable, runInAction } from 'mobx';
import { BaseInteractionError } from 'services/Errors/BaseInteractionError';
import { ICameraApiInteractionService } from 'services/typings/ApiTypes';
import { BaseTableStore } from '../../components/Base/BaseTableStore';
import { definitions } from '../../typings/Dto';
import { ColumnDefinition, SortDirection } from '../../typings/table';
import { TYPES } from '../../typings/types';

@injectable()
export class SettingsStore extends BaseTableStore {
    errors: BaseInteractionError[] = [];
    camerasList: definitions['CameraList'] = { items: [] };

    nameOfCamera = '';
    isCreating = false;

    private readonly cameraFetcher: ICameraApiInteractionService;

    constructor(@inject(TYPES.CameraApiInteractionService) cameraFetcher: ICameraApiInteractionService) {
        super();
        this.cameraFetcher = cameraFetcher;
        makeObservable(this, {
            camerasList: observable,
            errors: observable,
            isCreating: observable,
            startCreatingNewCamera: action,
            stopCreatingNewCamera: action,
            addNewCamera: action,
            sortDirectionChanged: action,
            filterValueChanged: action,
        });
    }

    public startCreatingNewCamera = () => {
        this.isCreating = true;
    };

    public stopCreatingNewCamera = () => {
        this.isCreating = false;
    };

    public async addNewCamera(cameraDto: definitions['CameraDto']) {
        const either: Either<BaseInteractionError, definitions['CameraDto']> = await this.cameraFetcher.addNewCamera(
            cameraDto,
        );

        runInAction(() => {
            if (isLeft(either)) {
                this.errors.push(either.left);
            }
        });
    }

    public sortDirectionChanged<T>(sortBy: ColumnDefinition<T>, sortDir: SortDirection): void {
        super.sortDirectionChanged(sortBy, sortDir);
        this.cameraFetcher.getCamerasList(sortBy as string, sortDir);
    }

    public filterValueChanged(filterValue: string): void {
        super.filterValueChanged(filterValue);
        this.cameraFetcher.getCamerasList(this.sortBy, this.sortDir, this.filterName, this.filterValue);
    }
}
