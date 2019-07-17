def parseDateFromFile(dateFromFile):
    dateFromFile = dateFromFile.strip()
    regexp = r"^\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}"
    result = re.findall(regexp, dateFromFile)
    if not result:
        raise ValueError("Wrong dateFromFile from file")
    date, time = dateFromFile.split(" ")

    year, month, day = date.split("-")
    hours, minuts, seconds = time.split(":")

    parsedData = datetime.datetime(int(year), int(month), int(day),
                                   int(hours), int(minuts), int(seconds))
    return parsedData

