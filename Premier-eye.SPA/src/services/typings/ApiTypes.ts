import { definitions } from 'typings/Dto';
import { AsyncEither } from '../../typings/common';

export interface IGalleryApiInteractionService {
    getImage: (imageId: string) => AsyncEither<any>;
    getAllImages: () => AsyncEither<any>;
    getInfoImage: (src: string) => AsyncEither<any>;
    getInfoImageByIndex: (cameraId: string, indexOfImage: number) => AsyncEither<any>;
}

export interface ICameraApiInteractionService {
    getImageFromCamera: (cameraId: string) => AsyncEither<any>;
    getCamerasList: (sortBy?: string, sortDir?: string, filterBy?: string, filterValue?: string) => AsyncEither<any>;
    addNewCamera: (cameraDto: definitions['CameraDto']) => AsyncEither<any>;
}
