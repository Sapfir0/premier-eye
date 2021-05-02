import { useState } from 'react';
import { myContainer } from '../config/inversify.config';

export function useInject<T>(id: string | symbol): T {
    const [store, setStore] = useState(() => {
        return myContainer.get<T>(id);
    });
    return store;
}

export const useModalState = ({ initialOpen = false } = {}) => {
    const [isOpen, setIsOpen] = useState(initialOpen);

    const onOpen = () => {
        setIsOpen(true);
    };

    const onClose = () => {
        setIsOpen(false);
    };

    const onToggle = () => {
        setIsOpen(!isOpen);
    };

    return { onOpen, onClose, isOpen, onToggle };
};
