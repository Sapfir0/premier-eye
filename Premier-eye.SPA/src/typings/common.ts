import {Either} from "@sweet-monads/either";
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

