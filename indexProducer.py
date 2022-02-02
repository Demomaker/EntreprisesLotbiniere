
def getDataFromFile(url) :
    with open(r"" + url + "", "r+", encoding="utf8") as file:
        data = file.read()
    return data

def getFormattedDataForHTMLDocument(data) :
    utf8meta = '<meta charset="utf-8">\n'
    compatible = '<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">\n'
    title = '<title>Annuaire d\'entreprises imprimable</title>\n'
    description = '<meta name="description" content="Juste un annuaire d\'entreprises imprimable de la MRC de Lotbinière">\n'
    viewport = '<meta name="viewport" content="width=device-width">\n'
    css = '<link rel="stylesheet" media="screen" href="index.css">'
    head = "<head>\n\t\t\t\t" + utf8meta + compatible + title + description + viewport + css + "\n</head>\n" 
    script = '\n<script src="index.js"></script>\n'
    body = "<body>\n" + data + script + "\n</body>"
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
    startIndex = data.find('av_textblock_section')
    endIndex = startIndex + len('av_textblock_section')
    resultingData = data[0:startIndex] + 'companyListContainer' + data[endIndex:]
    startIndex = resultingData.find('avia_textblock')
    endIndex = startIndex + len('avia_textblock')
    resultingData = resultingData[0:startIndex] + 'companyList' + resultingData[endIndex:]
    while 'avia-data-table-wrap' in resultingData :
        startIndex = resultingData.find('avia-data-table-wrap')
        endIndex = startIndex + len('avia-data-table-wrap')
        resultingData = resultingData[0:startIndex] + '' + resultingData[endIndex:]
        
    while 'avia_responsive_table' in resultingData :
        startIndex = resultingData.find('avia_responsive_table')
        endIndex = startIndex + len('avia_responsive_table')
        resultingData = resultingData[0:startIndex] + 'company' + resultingData[endIndex:]
        
        
    while 'avia-table avia-data-table avia-table-1 avia-builder-el-3 avia-builder-el-no-sibling' in resultingData :
        startIndex = resultingData.find('avia-table avia-data-table avia-table-1 avia-builder-el-3 avia-builder-el-no-sibling')
        endIndex = startIndex + len('avia-table avia-data-table avia-table-1 avia-builder-el-3 avia-builder-el-no-sibling')
        resultingData = resultingData[0:startIndex] + 'companyTable' + resultingData[endIndex:]

    while 'avia-heading-row' in resultingData :
        startIndex = resultingData.find('avia-heading-row')
        endIndex = startIndex + len('avia-heading-row')
        resultingData = resultingData[0:startIndex] + 'companyHeading' + resultingData[endIndex:]

    while 'avia-highlight-col' in resultingData :
        startIndex = resultingData.find('avia-highlight-col')
        endIndex = startIndex + len('avia-highlight-col')
        resultingData = resultingData[0:startIndex] + 'companyHeader' + resultingData[endIndex:]

    while 'textefoncetableau' in resultingData :
        startIndex = resultingData.find('textefoncetableau')
        endIndex = startIndex + len('textefoncetableau')
        resultingData = resultingData[0:startIndex] + 'personneContactPrincipal' + resultingData[endIndex:]

    
    startIndex = 0
    endIndex = 0
    while resultingData.find('<span class="texteboldtableau">SERVICES : </span>', endIndex) != -1:
        startIndex = resultingData.find('<span class="texteboldtableau">SERVICES : </span>', endIndex) + len('<span class="texteboldtableau">SERVICES : </span>')
        endIndex = resultingData.find('<br>', startIndex)
        resultingData = resultingData[0:startIndex] + '<span class="service">' + resultingData[startIndex:endIndex] + '</span>' + resultingData[endIndex:]
    
    
    startIndex = 0
    endIndex = 0
    while resultingData.find('<span class="texteboldtableau">DOMAINE D’ACTIVITÉ :</span>', endIndex) != -1:
        startIndex = resultingData.find('<span class="texteboldtableau">DOMAINE D’ACTIVITÉ :</span>', endIndex) + len('<span class="texteboldtableau">DOMAINE D’ACTIVITÉ :</span>')
        endIndex = resultingData.find('<br>', startIndex)
        resultingData = resultingData[0:startIndex] + '<span class="domaine">' + resultingData[startIndex:endIndex] + '</span>' + resultingData[endIndex:]
    
    startIndex = 0
    endIndex = 0
    while resultingData.find('<span class="texteboldtableau">NOMBRE D’EMPLOI :</span>', endIndex) != -1:
        startIndex = resultingData.find('<span class="texteboldtableau">NOMBRE D’EMPLOI :</span>', endIndex) + len('<span class="texteboldtableau">NOMBRE D’EMPLOI :</span>')
        endIndex = resultingData.find('</tr>', startIndex)
        resultingData = resultingData[0:startIndex] + '<span class="employes">' + resultingData[startIndex:endIndex] + '</span>' + resultingData[endIndex:]
    
    while '<span class="texteboldtableau">SERVICES : </span>' in resultingData :
        startIndex = resultingData.find('<span class="texteboldtableau">SERVICES : </span>')
        endIndex = startIndex + len('<span class="texteboldtableau">SERVICES : </span>')
        resultingData = resultingData[0:startIndex] + '<span class="serviceHeader">SERVICES : </span>' + resultingData[endIndex:]

    while '<span class="texteboldtableau">DOMAINE D’ACTIVITÉ :</span>' in resultingData :
        startIndex = resultingData.find('<span class="texteboldtableau">DOMAINE D’ACTIVITÉ :</span>')
        endIndex = startIndex + len('<span class="texteboldtableau">DOMAINE D’ACTIVITÉ :</span>')
        resultingData = resultingData[0:startIndex] + '<span class="domaineHeader">DOMAINE D’ACTIVITÉ :</span>' + resultingData[endIndex:]

    while '<span class="texteboldtableau">NOMBRE D’EMPLOI :</span>' in resultingData :
        startIndex = resultingData.find('<span class="texteboldtableau">NOMBRE D’EMPLOI :</span>')
        endIndex = startIndex + len('<span class="texteboldtableau">NOMBRE D’EMPLOI :</span>')
        resultingData = resultingData[0:startIndex] + '<span class="employesHeader">NOMBRE D’EMPLOI :</span>' + resultingData[endIndex:]

    currentIndex = 0
    while 'td' in resultingData :
        currentIndex = resultingData.find('td', currentIndex) + len('td ')
        resultingData = resultingData[0:currentIndex] + 'class="contactData"' + resultingData[currentIndex:]
        currentIndex = resultingData.find('td', currentIndex) + len('td ')

    currentIndex = resultingData.find('td', currentIndex) + len('td ')
    while 'td' in resultingData :
        currentIndex = resultingData.find('td', currentIndex) + len('td ')
        resultingData = resultingData[0:currentIndex] + 'class="companyInfo"' + resultingData[currentIndex:]
        currentIndex = resultingData.find('td', currentIndex) + len('td ')
    return resultingData

def redoStyling(data) :
    newData = removeBackgroundColorTag(data)
    newData = replaceClasses(newData)
    return newData

createIndex(redoStyling(getEntreprises(getDataFromFile("Entreprises.html"))))
