import {HeadersBaseSettings} from "../../typings/common";

export function getMappingForCell<T>(headers: HeadersBaseSettings<T>): Array<keyof T | ""> {
    return [...headers.keys()]
}


// ищем в хедерах присутсвие convertFunction, если оно есть, прогоняет текущее значение через него, если нет, то возвращает текущее значение
export function convert<T>(headers: HeadersBaseSettings<T>, column: keyof T, value: any, row: any) {
    const obj = headers.get(column)
    if (obj && obj.convertFunction) {
        if (obj.emptyDataColumn) {
            return obj.convertFunction(row, column)
        } else {
            return obj.convertFunction(value, column)
        }
    }
    return value
}


