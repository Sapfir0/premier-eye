import {AxiosRequestConfig, AxiosResponse} from "axios";
import {NetworkError} from "../Errors/NetworkError";
import {Either} from "@sweet-monads/either";
import {AsyncEither} from "../../typings/common";
import {BaseInteractionError} from "../Errors/BaseInteractionError";
import { definitions } from "typings/Dto";


export interface IApiHelper {
    request: <T>(promise: Promise<AxiosResponse>) => Promise<Either<NetworkError, any>>
}

export interface IApiInteractionService {
    get: <T = any>(url: string, data?: any, host?: string, config?: AxiosRequestConfig) => AsyncEither<T>
    post: <T = any>(url: string, data: any, host: string, settings?: any, config?: AxiosRequestConfig) => AsyncEither<T>
}


export interface IBaseInteractionService {
    get: <T=any>(url: string, data?:any, host?: string, config?: AxiosRequestConfig) => Promise<Either<BaseInteractionError, T>>
    post: <T=any>(url: string, data?: any, host?: string, settings?: any, config?: AxiosRequestConfig,) => Promise<Either<BaseInteractionError, T>>
    delete: <T=any>(url: string, data?: any, host?: string, config?: AxiosRequestConfig) => Promise<Either<BaseInteractionError, T>>
    put: <T=any>(url: string, data?: any, host?: string, settings?: any, config?: AxiosRequestConfig,) => Promise<Either<BaseInteractionError, T>>
}

export interface IGalleryApiInteractionService {
    getImage: (imageId: string) => AsyncEither<any>
    getAllImages: () => AsyncEither<any>
    getInfoImage: (src: string) => AsyncEither<any>
    getInfoImageByIndex: (cameraId: string, indexOfImage: number) => AsyncEither<any>
}

export interface ICameraApiInteractionService {
    getImageFromCamera: (cameraId: string) => AsyncEither<any>
    getCamerasList: () => AsyncEither<any>
    addNewCamera: (cameraDto: definitions['DTOCamera']) => AsyncEither<any>
}
