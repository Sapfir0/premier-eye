export function getDiffSecond(date1: Date, date2: Date) {
    return Math.ceil(Math.abs(date2.getTime() - date1.getTime()) / 1000);
}

export function isImageShotedToday(date: Date) {
    const today = new Date();
    return (
        date.getDate() === today.getDate() &&
        date.getMonth() === today.getMonth() &&
        date.getFullYear() === today.getFullYear()
    );
}

export function getDiffDay(date1: Date, date2: Date): number {
    const utcDate =
        Date.UTC(date2.getFullYear(), date2.getMonth(), date2.getDate()) -
        Date.UTC(date1.getFullYear(), date1.getMonth(), date1.getDate());
    return Math.floor(utcDate / (1000 * 60 * 60 * 24));
}
