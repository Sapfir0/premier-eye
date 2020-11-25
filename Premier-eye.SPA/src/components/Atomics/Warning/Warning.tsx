import TitledWarning from "../TitledWarning";
import { getDiffSecond } from "../../../services/Time";
import React from "react";

export const WarningIfBigDiffBetweenDates = (createdDate: Date, fixationDate: Date, maxDiff = 60 * 60) => {
    const bigDateDiff = getDiffSecond(createdDate, fixationDate) > maxDiff
    if (bigDateDiff) {
        const longText = `Запись в базе данных появилась ${createdDate}.`
        return <TitledWarning text={longText} />
    }
    return null
}
