
def getDataFromFile(url) :
    with open(r"" + url + "", "r+", encoding="utf8") as file:
        data = file.read(999999999)
    return data

def getFormattedDataForHTMLDocument(data) :
    utf8meta = '<meta charset="utf-8">\n'
    compatible = '<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">\n'
    title = '<title>Annuaire d\'entreprises imprimable</title>\n'
    description = '<meta name="description" content="Juste un annuaire d\'entreprises imprimable de la MRC de Lotbinière">\n'
    viewport = '<meta name="viewport" content="width=device-width">\n'
    css = '<link rel="stylesheet" href="index.css">'
    head = "<head>\n\t\t\t\t" + utf8meta + compatible + title + description + viewport + css + "\n</head>\n" 
    newCompaniesScript = '\n<script src="./newCompanies.js"></script>'
    script = '\n<script src="./index.js"></script>\n'
    body = "<body>\n" + data + newCompaniesScript + script + "\n</body>"
    return head + body

def createIndex(data) :
    with open('index.html', 'w', encoding="utf8") as file:
        formattedData = getFormattedDataForHTMLDocument(data)
        file.write(formattedData)

def getEntreprises(data) :
    sectionStartIndex = data.find(
         '********** RESULTS LIST *********'
        ) - 13
    sectionEndIndex = data.find('</section>', sectionStartIndex) + 10
    entreprises = data[sectionStartIndex:sectionEndIndex]
    return entreprises

def removeBackgroundColorTag(data) :
    startIndex = data.find('bgcolor="')
    endIndex = data.find('"', startIndex + 10)
    resultingData = data[0:startIndex-1] + data[endIndex+1:]
    while 'bgcolor=' in resultingData :
        startIndex = resultingData.find('bgcolor="')
        endIndex = resultingData.find('"', startIndex + 10)
        resultingData = resultingData[0:startIndex-1] + resultingData[endIndex+1:]
    return resultingData

def replaceClasses(data):
    #Replace original classes with our own classes
    classesToSearchFor = ['av_textblock_section', 'avia_textblock', 'avia-data-table-wrap', 'avia_responsive_table', 'avia-table avia-data-table avia-table-1 avia-builder-el-3 avia-builder-el-no-sibling', 'avia-heading-row', 'avia-highlight-col', 'textefoncetableau', 'http://http']
    classesToReplaceWith = ['companyListContainer', 'companyList', '', 'company', 'companyTable', 'companyHeading', 'companyHeader', 'personneContactPrincipal', 'http']
    resultingData = replaceMultipleClasses(data, classesToSearchFor, classesToReplaceWith)

    #Replace Company Data decoration
    resultingData = complexReplace(resultingData, ['SERVICES', 'span>', ' ', '<br/>'], ['<span class="service">', '</span>'], 0, 2, 3, 0, 1)
    resultingData = complexReplace(resultingData, ['DOMAINE D’ACTIVITÉ', 'span>', ' ', '<br/>'], ['<span class="domaine">', '</span>'], 0, 2, 3, 0, 1)
    resultingData = complexReplace(resultingData, ['NOMBRE D’EMPLOI', 'span>', ' ', '</td>'], ['<span class="employes">', '</span>'], 0, 2, 3, 0, 1)

    #Replace Company Data Headers decoration
    resultingData = complexReplace(resultingData, ['<span class="texteboldtableau"><strong>SERVICES', 'span>', '<'], ['<span class="serviceHeader">', '</span> ', '<strong>SERVICES</strong>'], 0, 0, 2, 0, 1, 2)
    resultingData = complexReplace(resultingData, ['<span class="texteboldtableau"><strong>DOMAINE D’ACTIVITÉ', 'span>', '<'], ['<span class="domaineHeader">', '</span> ', '<strong>DOMAINE D’ACTIVITÉ</strong>'], 0, 0, 2, 0, 1, 2)
    resultingData = complexReplace(resultingData, ['<span class="texteboldtableau"><strong>NOMBRE D’EMPLOI', 'span>', '<'], ['<span class="employesHeader">', '</span> ', '<strong>NOMBRE D’EMPLOI</strong>'], 0, 0, 2, 0, 1, 2)

    #Add class attributes for contactData and companyInfo
    resultingData = addClassAttributeAtEveryElementForCertainInterval(resultingData, 'contactData', 'td', 1, 1)
    resultingData = addClassAttributeAtEveryElementForCertainInterval(resultingData, 'companyInfo', 'td', 2, 0)
    return resultingData

def addClassAttributeAtEveryElementForCertainInterval(data, classAttributeToAdd, elementToAddTo, findsBeforeStart, findsBeforeEnd):
    resultingData = data
    currentIndex = 0
    completeElementToAddTo = '<' + elementToAddTo
    completeElementToAddToWithSpace = completeElementToAddTo + ' '
    while resultingData.find(completeElementToAddTo, currentIndex) > -1 :
        for i in range(findsBeforeStart):
            currentIndex = resultingData.find(completeElementToAddTo, currentIndex) + len(completeElementToAddToWithSpace)
        resultingData = resultingData[0:currentIndex] + 'class="' + classAttributeToAdd + '" ' + resultingData[currentIndex:]
        for i in range(findsBeforeEnd):
            currentIndex = resultingData.find(completeElementToAddTo, currentIndex) + len(completeElementToAddToWithSpace)
    return resultingData

def findElementsIndexesInOrder(data, arrayOfElementsToFind, startIndex):
    arrayOfElementsIndexes = []
    searchNextIndex = startIndex
    for x in arrayOfElementsToFind:
        found = data.find(x, searchNextIndex)
        if found > -1:
            searchNextIndex = found
        arrayOfElementsIndexes.append(found)
    return arrayOfElementsIndexes

def replaceClass(data, classToSearchFor, classToReplaceWith):
    resultingData = data
    while classToSearchFor in resultingData :
        startIndex = resultingData.find(classToSearchFor)
        endIndex = startIndex + len(classToSearchFor)
        resultingData = resultingData[0:startIndex] + classToReplaceWith + resultingData[endIndex:]
    return resultingData

def replaceMultipleClasses(data, classToSearchForList, classToReplaceWithList):
    resultingData = data
    for idOfClassToSearchFor, classToSearchFor in enumerate(classToSearchForList):
        classToReplaceWith = classToReplaceWithList[idOfClassToSearchFor]
        resultingData = replaceClass(resultingData, classToSearchFor, classToReplaceWith)
    return resultingData

def complexReplace(data, arrayToSearchFor, arrayToReplaceWith, criticalElementIndex, searchReplaceStartIndex, searchReplaceEndIndex, replaceWithBeforeIndex, replaceWithAfterIndex, replaceStartToEndWithIndex = -1):
    startIndex = 0
    endIndex = 0
    resultingData = data
    while True:
        nextFind = findElementsIndexesInOrder(resultingData, arrayToSearchFor, endIndex)
        mustContinue = nextFind[criticalElementIndex] > -1
        if not mustContinue:
            break
        startIndex = nextFind[searchReplaceStartIndex]
        endIndex = nextFind[searchReplaceEndIndex]
        replacement = ''
        if replaceStartToEndWithIndex > -1:
            replacement = arrayToReplaceWith[replaceStartToEndWithIndex]
        else :
            replacement = resultingData[startIndex:endIndex]
        replacement = replacement.strip()
        resultingData = resultingData[0:startIndex] + arrayToReplaceWith[replaceWithBeforeIndex] + replacement + arrayToReplaceWith[replaceWithAfterIndex] + resultingData[endIndex:]
    return resultingData

def redoStyling(data) :
    newData = removeBackgroundColorTag(data)
    newData = replaceClasses(newData)
    return newData

import urllib.request, urllib.error, urllib.parse

url = 'https://www.mrclotbiniere.org/services-au-entreprise/repertoires/repertoire-des-entreprises/?domaines=0&municipalites=0'

response = urllib.request.urlopen(url)
webContent = response.read().decode('UTF-8')
tempFileName = 'Entreprises.html'

with open(tempFileName, 'w', encoding='utf-8') as file:
    file.write(webContent)

createIndex(redoStyling(getEntreprises(getDataFromFile(tempFileName))))
