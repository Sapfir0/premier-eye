

def writeRowInCSV(df, filename, time, cars, peoples, trucks, time2, cars2, peoples2, trucks2):
    data = pd.Series([filename, time, cars, peoples, trucks, time2, cars2, peoples2, trucks2])
    df.loc[-1] = list(data) # вот это убогий способ я нашел
    df.index = df.index + 1  # мы добавляем в начало а потом пересортируем хах
    df = df.sort_index()


def init():
    df = pd.DataFrame(columns=['Filename', 'Elapsed Time', 'Cars','Peoples', 'Trucks', 'Elapsed Time2', "Cars2", "Peoples2", "Trucks2"])
    counter=0
    
    writeRowInCSV(df, filename,elapsed_time,countedObj['car'], countedObj['person'], countedObj['truck'], elapsed_time2, countedObjMask['car'], countedObjMask['person'], countedObjMask['truck'])
    counter+=1
    if(counter%10 == 0 or counter==1):
        print("Write in CSV file")
        df.to_csv(cfg.TABLE_NAME, index=False)
    