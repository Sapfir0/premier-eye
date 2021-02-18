import React from 'react';
import { getDiffSecond } from '../../../services/Time';
import TitledWarning from '../TitledWarning';

export const WarningIfBigDiffBetweenDates = (createdDate: Date, fixationDate: Date, maxDiff = 60 * 60 * 24) => {
    const bigDateDiff = getDiffSecond(createdDate, fixationDate) > maxDiff;

    if (bigDateDiff) {
        const longText = `Запись в базе данных появилась ${createdDate}.`;
        return <TitledWarning text={longText} />;
    }
    return null;
};
