import axios, { AxiosRequestConfig, AxiosResponse } from 'axios';
import { bimap, Either } from 'fp-ts/Either';
import { inject, injectable } from 'inversify';
import * as qs from 'querystring';
import { TYPES } from '../typings/types';
import { BaseInteractionError } from './Errors/BaseInteractionError';
import { NetworkError } from './Errors/NetworkError';
import { IApiHelper, IBaseInteractionService } from './typings/ApiTypes';

@injectable()
class BaseInteractionService implements IBaseInteractionService {
    private readonly _api: IApiHelper;

    constructor(@inject(TYPES.ApiHelper) api: IApiHelper) {
        this._api = api;
    }

    public get = async <T = any>(
        url: string,
        data?: any,
        host?: string,
        config?: AxiosRequestConfig,
    ): Promise<Either<BaseInteractionError, T>> => {
        return this.query<T>({ method: 'get', url: url, data: data, baseURL: host, ...config });
    };

    public delete = async <T = any>(
        url: string,
        data?: any,
        host?: string,
        config?: AxiosRequestConfig,
    ): Promise<Either<BaseInteractionError, T>> => {
        return this.query<T>({ method: 'delete', url: url, data: data, baseURL: host, ...config });
    };

    public post = async <T = any>(
        url: string,
        data?: any,
        host?: string,
        settings?: any,
        config?: AxiosRequestConfig,
    ): Promise<Either<BaseInteractionError, T>> => {
        const parsedData = settings?.stringify ? qs.stringify(data) : data;
        const parsedConfig = settings?.multipartData ? this.setMultipartDataHeader(config) : config;

        return this.query<T>({ method: 'post', url: url, baseURL: host, data: parsedData, ...parsedConfig });
    };

    public put = async <T = any>(
        url: string,
        data?: any,
        host?: string,
        settings?: any,
        config?: AxiosRequestConfig,
    ): Promise<Either<BaseInteractionError, T>> => {
        return this.query<T>({ method: 'put', url: url, baseURL: host, data: data, ...config });
    };

    private query = async <T>(config: AxiosRequestConfig) => {
        const newConfig: AxiosRequestConfig = {
            ...config,
        };
        const req = axios.request<T>({ ...newConfig });
        const response = await this._api.request<T>(req);

        return bimap(
            (e: NetworkError) => new BaseInteractionError(e.message),
            (res: AxiosResponse<T>) => res.data,
        )(response);
    };

    private setMultipartDataHeader = (config?: AxiosRequestConfig) => {
        const newConfig: AxiosRequestConfig = {
            ...config,
            headers: {
                'Content-Type': 'multipart/form-data',
                ...config?.headers,
            },
        };
        return newConfig;
    };
}

export default BaseInteractionService;
