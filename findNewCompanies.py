def getDataFromFile(url) :
    with open(r"" + url + "", "r+", encoding="utf8") as file:
        data = file.read(999999999)
    return data

def getNewCompanies(data):
    resultingData = data
    newCompanies = []
    elementsToFind = []
    currentIndex = 0
    currentCompany = getNextCompany(resultingData, currentIndex)
    currentIndex = currentCompany[1]
    while currentCompany != [-2, -2, -2]:
        name = getName(resultingData, currentIndex)
        address = getAddress(resultingData, currentIndex)
        phone = getPhone(resultingData, currentIndex)
        fax = getFax(resultingData, currentIndex)
        mail = getMail(resultingData, currentIndex)
        website = getWebsite(resultingData, currentIndex)
        service = getService(resultingData, currentIndex)
        domain = getDomain(resultingData, currentIndex)
        nbEmployees = getNbEmployees(resultingData, currentIndex)
        newCompanies.append((name, address, phone, fax, mail, website, service, domain, nbEmployees))
        currentCompany = getNextCompany(resultingData, currentIndex)
        currentIndex = currentCompany[1]
    return newCompanies


def getName(data, startingIndex):
    indexes = findElementsIndexesInOrder(data, ['companyHeader', '>', '<'], startingIndex)
    firstIndex = indexes[1] + 1
    secondIndex = indexes[2]
    return data[firstIndex:secondIndex].strip()

def getAddress(data, startingIndex):
    indexes = findElementsIndexesInOrder(data, ['contactData', '+', '\n', '+', '<'], startingIndex)
    firstIndex = indexes[3] + 1
    secondIndex = indexes[4]
    return data[firstIndex:secondIndex].strip()

def getPhone(data, startingIndex):
    indexes = findElementsIndexesInOrder(data, ['contactData', '+', '\n', '+', '\n', '+', '(', '|'], startingIndex)
    indexes2 = findElementsIndexesInOrder(data, ['contactData', '+', '\n', '+', '\n', '+', '(', '<br/>'], startingIndex)
    firstIndex = indexes[6]
    secondIndex = indexes[7]
    if indexes[7] > indexes2[7]:
        secondIndex = indexes2[7]
    return data[firstIndex:secondIndex].strip()

def getFax(data, startingIndex):
    indexes = findElementsIndexesInOrder(data, ['contactData', '-', '\n', '-', '\n', '-', '|', '(', '<br/>'], startingIndex)
    indexes2 = findElementsIndexesInOrder(data, ['contactData', '-', '\n', '-', '\n', '-', '|', '<br/>'], startingIndex)
    firstIndex = indexes[7]
    secondIndex = indexes[8]
    if indexes[8] > indexes2[7]:
        return '' 
    return data[firstIndex:secondIndex].strip()

def getMail(data, startingIndex):
    indexes = findElementsIndexesInOrder(data, ['<a href="mailto', '>', '<'], startingIndex)
    firstIndex = indexes[1] + 1
    secondIndex = indexes[2]
    return data[firstIndex:secondIndex].strip()

def getWebsite(data, startingIndex):
    indexes = findElementsIndexesInOrder(data, ['<a href="http', 'http', '"'], startingIndex)
    firstIndex = indexes[1]
    secondIndex = indexes[2]
    return data[firstIndex:secondIndex].strip()

def getService(data, startingIndex):
    indexes = findElementsIndexesInOrder(data, ['serviceHeader', 'service"', '>', '<'], startingIndex)
    firstIndex = indexes[2] + 1
    secondIndex = indexes[3]
    return data[firstIndex:secondIndex].strip()

def getDomain(data, startingIndex):
    indexes = findElementsIndexesInOrder(data, ['domaineHeader', 'domaine"', '>', '<'], startingIndex)
    firstIndex = indexes[2] + 1
    secondIndex = indexes[3]
    return data[firstIndex:secondIndex].strip()

def getNbEmployees(data, startingIndex):
    indexes = findElementsIndexesInOrder(data, ['employesHeader', 'employes"', '>', '<'], startingIndex)
    firstIndex = indexes[2] + 1
    secondIndex = indexes[3]
    return data[firstIndex:secondIndex].strip()

def getNextCompany(data, currentIndex):
    foundElementIndexes = findElementsIndexesInOrder(data, ['+', 'company"'], currentIndex)
    if foundElementIndexes[0] == -1 or foundElementIndexes[1] == -1 or foundElementIndexes[0] > foundElementIndexes[1]:
        return [-2, -2, -2]
    containsReturnCharacterBetween = containsStringBetween(data, foundElementIndexes[0], foundElementIndexes[1], '\n')

    if containsReturnCharacterBetween:
        maximumDistance = 25
        if foundElementIndexes[1] - foundElementIndexes[0] > maximumDistance:
            return getNextCompany(data, foundElementIndexes[1] - maximumDistance)
        else :
            return getNextCompany(data, foundElementIndexes[0] + len('+'))

    return [foundElementIndexes[0], foundElementIndexes[1], currentIndex]

def containsStringBetween(data, indexOne, indexTwo, input):
    currentIndex = indexOne
    foundIt = False
    while currentIndex != indexTwo :
        foundIt = True
        for index in range(len(input)) :
            if input[index] != data[currentIndex + index]:
                foundIt = False
                break
        if foundIt :
            break
        currentIndex += 1

    return foundIt

def findElementsIndexesInOrder(data, arrayOfElementsToFind, startingIndex):
    arrayOfElementsIndexes = []
    searchNextIndex = startingIndex
    for x in arrayOfElementsToFind:
        found = data.find(x, searchNextIndex)
        if found > -1:
            searchNextIndex = found
        arrayOfElementsIndexes.append(found)
    return arrayOfElementsIndexes

def insertIntoJavascript(formattedData):
    javascriptVariable = "const newCompanies = `" + formattedData + "`;"
    return javascriptVariable

def printToFileNewCompanies(newCompanies, outputFile):
    with open(outputFile, 'w', encoding="utf8") as file:
        formattedData = getFormattedDataForTextDocument(newCompanies)
        file.write(formattedData)

def printToJavaScriptFileNewCompanies(newCompanies, outputJavascriptFileName):
    with open(outputJavascriptFileName, 'w', encoding="utf8") as file:
        formattedData = getFormattedDataForTextDocument(newCompanies)
        javascriptString = insertIntoJavascript(formattedData)
        file.write(javascriptString)


def getFormattedDataForTextDocument(newCompanies):
    out = "Nombre de nouvelles compagnies : " + str(len(newCompanies))
    for (name, address, phone, fax, mail, website, service, domain, nbEmployees) in newCompanies :
        if website == 'http://':
            website = ''
        spaceBetween = "\r\n"
        header = "-------------- NOUVELLE ENTREPRISE : ------------"
        nameDisplay = spaceBetween + "Nom : " + name
        addressDisplay = spaceBetween + "Adresse : " + address
        phoneDisplay = spaceBetween + "Téléphone principal : " + phone
        faxDisplay = spaceBetween + "Fax : " + fax
        mailDisplay = spaceBetween + "Courriel : " + mail
        websiteDisplay = spaceBetween + "Site web : " + website
        serviceDisplay = spaceBetween + "Service(s) : " + service 
        domainDisplay = spaceBetween + "Domaine : " + domain
        nbEmployeesDisplay = spaceBetween + "Nombre d'employés : " + nbEmployees
        footer = spaceBetween + "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
        out += spaceBetween + header + nameDisplay + addressDisplay + phoneDisplay + faxDisplay + mailDisplay + websiteDisplay + serviceDisplay + domainDisplay + nbEmployeesDisplay + footer
    return out


tempFileName = 'difflog.txt'
outputJavascriptFileName = 'newCompanies.js'
outputFileName = 'Nouvelles Compagnies.txt'
data = getDataFromFile(tempFileName)
newCompanies = getNewCompanies(data)
printToJavaScriptFileNewCompanies(newCompanies, outputJavascriptFileName)
printToFileNewCompanies(newCompanies, outputFileName)