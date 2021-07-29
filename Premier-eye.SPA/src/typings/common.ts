import { BaseInteractionError } from 'api_interaction_services';
import { Either } from 'fp-ts/Either';

export type IdPayload = {
    id: number;
};

export type AsyncEither<T> = Promise<Either<BaseInteractionError, T>>;
export type ResolvedEither<T> = Either<BaseInteractionError, T>;

export interface BaseSettings {
    stringify?: boolean;
    multipartData?: boolean;
}

export interface ActionTypePayload<PayloadType, ActionType> {
    type: ActionType;
    payload: PayloadType;
}

export interface ActionTypePure<ActionType> {
    type: ActionType;
}

export type AnyActionName = string;

export type ErrorPayload = {
    error: BaseInteractionError;
};

export type Function = () => void;
