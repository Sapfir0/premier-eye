import createSagaMiddleware from "redux-saga";
import {applyMiddleware, compose, createStore} from "redux";
import createRootReducer from "./reducers";
import logger from "redux-logger";
import rootSaga from "./sagas";
import { routerMiddleware, connectRouter } from "connected-react-router";
import {TYPES} from "../typings/types";
import {myContainer} from "../config/inversify.config";
import UrlService from "../services/UrlService";


const urlService = myContainer.get<UrlService>(TYPES.UrlService)

const sagaMiddleware = createSagaMiddleware()
const middlewares = [logger, routerMiddleware(urlService.history), sagaMiddleware ];

const rootReducerWithRouter = createRootReducer(urlService.history)
export type RootStore = ReturnType<typeof rootReducerWithRouter>

export const store = compose(applyMiddleware(...middlewares))(createStore)(rootReducerWithRouter);

sagaMiddleware.run(rootSaga)

