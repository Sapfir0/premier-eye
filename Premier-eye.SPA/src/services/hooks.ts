import { useState } from 'react';
import { myContainer } from '../config/inversify.config';

export function useInject<T>(id: string | symbol): T {
    const [store, setStore] = useState(() => {
        return myContainer.get<T>(id);
    });
    return store;
}
