import {Either} from "fp-ts/Either";
import {BaseInteractionError} from "../services/Errors/BaseInteractionError";

export type IdPayload = {
    id: number
}

export type AsyncEither<T> = Promise<Either<BaseInteractionError, T>>

export interface BaseSettings {
    stringify?: boolean
    multipartData?: boolean
}


export interface ActionTypePayload<PayloadType, ActionType> {
    type: ActionType;
    payload: PayloadType;
}

export interface ActionTypePure<ActionType> {
    type: ActionType;
}

export type AnyActionName = string

export type ErrorPayload = {
    error: BaseInteractionError
}

export type Function = () => void



export interface HeaderName<DTO=any> {
    text: string,
    emptyDataColumn?: boolean // если подано это значение, то в convert function будет передено не текущее значение столбца, а вся строка
    convertFunction?: (cellValue: any, columnName: keyof DTO) => React.ReactElement | string
}

export type Key<T> = keyof T
export type HeadersBaseSettings<T> = Map<Key<T> | "", HeaderName<T>>
