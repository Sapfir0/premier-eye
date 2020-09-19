
function getDiffSecond(date1: Date , date2: Date) {
    return Math.ceil(Math.abs(date2.getTime() - date1.getTime()) / 1000);
}

export { getDiffSecond}
