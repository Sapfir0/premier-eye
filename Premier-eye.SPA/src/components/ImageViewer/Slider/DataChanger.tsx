import { Button } from '@material-ui/core';
import React from 'react';

export function ChangeDateButton() {
    return (
        <div style={{ width: '70px' }}>
            Выбрать дату съемки: <Button>{new Date().toLocaleDateString('ru-RU')} </Button>
        </div>
    );
}
