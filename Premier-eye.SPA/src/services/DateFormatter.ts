import { timeParse } from 'd3-time-format';
import { dateFileFormat } from '../config/constants';

export const getDatetimeFromFilename = (filename: string) => {
    // js implementation of some functions in Premier-eye.Common
    const dateTime = filename.split('_')[1].split('.')[0];
    const parseTime = timeParse(dateFileFormat);
    return parseTime(dateTime);
};
