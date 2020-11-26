
export interface Settings {
    id: number,
    open: boolean
}

export function getSettings(countOfObjects: number) {
    let state = [];
    for (let i = 1; i < countOfObjects + 1; i++) {
        state.push({id: i, open: false})
    }
    return state;
}

