// Arrow function to get the parameter
// of the specified key
getParameter = (key) => {
  
    // Address of the current window
    address = window.location.search
  
    // Returns a URLSearchParams object instance
    parameterList = new URLSearchParams(address)
  
    // Returning the respected value associated
    // with the provided key
    return parameterList.get(key)
}

function getVariants()  {
    return {
    'Dosquet' : ['Dosquet'],
    'Laurier-Station' : ['Laurier', 'Laurier-Station'],
    'Leclercville': ['Leclercville'],
    'N.-D.-S.-C. d\'Issoudun' : ['N.-D.-S.-C. d\'Issoudun', 'Issoudun'],
    'Saint-Agapit' : ['Saint-Agapit', 'St-Agapit'],
    'Saint-Antoine-de-Tilly' : ['Saint-Antoine-de-Tilly', 'Saint-Antoine', 'St-Antoine-de-Tilly', 'St-Antoine'],
    'Saint-Apollinaire' : ['Saint-Apollinaire', 'St-Apo', 'Saint-Apo', 'St-Apollinaire'],
    'Sainte-Agathe-de-Lotbinière' : ['Sainte-Agathe-de-Lotbinière','Sainte-Agathe', 'Saint-Agathe', 'St-Agathe', 'Ste-Agathe', 'Ste-Agathe-de-Lotbinière'],
    'Sainte-Croix' : ['Sainte-Croix', 'Ste-Croix'],
    'Saint-Édouard-de-Lotbinière' : ['Saint-Édouard-de-Lotbinière', 'Saint-Édouard', 'St-Édouard'],
    'Saint-Flavien' : ['Saint-Flavien', 'St-Flavien'],
    'Saint-Gilles' : ['Saint-Gilles', 'St-Gilles'],
    'Saint-Janvier-de-Joly' : ['Saint-Janvier-de-Joly', 'Joly', 'St-Janvier-de-Joly', 'St-Janvier'],
    'Saint-Narcisse-de-Beaurivage' : ['Saint-Narcisse-de-Beaurivage', 'Saint-Narcisse', 'St-Narcisse', 'St-Narcisse-de-Beaurivage'],
    'Saint-Patrice-de-Beaurivage' : ['Saint-Patrice-de-Beaurivage', 'Saint-Patrice', 'St-Patrice', 'St-Patrice-de-Beaurivage'],
    'Saint-Sylvestre' : ['Saint-Sylvestre', 'St-Sylvestre'],
    'Val-Alain' : ['Val-Alain']
    }
}

function getDomains(companies) {
    let domains = [];
    for(let i = 0; i < companies.length; i++) {
        let company = companies[i];
        let domain = company.getElementsByClassName('domaine')[0].innerText.trim();
        if(domains.indexOf(domain) <= -1)
            domains.push(domain);
    }
    return domains.sort();
}

function getMunicipalities(companies) {
    let municipalities = {
        'Dosquet' : 'G0S 1H0',
        'Laurier-Station' : 'G0S 1N0',
        'Leclercville' : 'G0S 2K0',
        'Lotbinière' : 'G0S 1S0',
        'N.-D.-S.-C. d\'Issoudun' : 'G0S 1L0',
        'Saint-Agapit' : 'G0S 1Z0',
        'Saint-Antoine-de-Tilly' : 'G0S 2C0',
        'Saint-Apollinaire' : 'G0S 2E0',
        'Sainte-Agathe-de-Lotbinière' : 'G0S 2A0',
        'Sainte-Croix' : 'G0S 2H0',
        'Saint-Édouard-de-Lotbinière' : 'G0S 1Y0',
        'Saint-Flavien' : 'G0S 2M0',
        'Saint-Gilles' : 'G0S 2P0',
        'Saint-Janvier-de-Joly' : 'G0S 1M0',
        'Saint-Narcisse-de-Beaurivage' : 'G0S 1W0',
        'Saint-Patrice-de-Beaurivage' : 'G0S 1B0',
        'Saint-Sylvestre' : 'G0S 3C0',
        'Val-Alain' : 'G0S 3H0'
    };
    return municipalities;
}

function isSameMunicipality(municipality, value) {
    const municipalityVariants = getVariants()[municipality];
    if(municipalityVariants)
    for(let i = 0; i < municipalityVariants.length; i++) {
        const municipalityVariant = municipalityVariants[i];
        if(municipalityVariant.toLowerCase() === value.toLowerCase()) {
            return true;
        }
    }

    return false;
}

function filterByMunicipality(municipality) {
    const municipalityDivs = document.getElementsByClassName("municipalityDiv");
    for (let i = 0; i < municipalityDivs.length; i++) {
        let municipalityDiv = municipalityDivs[i];
        if(!isSameMunicipality(municipalityDiv.getAttribute("municipality"), municipality))
            municipalityDiv.hidden = true;
    }
    return municipalityDivs[municipality];
}

function filterByDomain(domain) {
    const domainDivs = document.getElementsByClassName("domainDiv");
    for(let i = 0; i < domainDivs.length; i++) {
        let domainDiv = domainDivs[i];
        if(domainDiv.getAttribute("domain").toLowerCase() !== domain.toLowerCase())
            domainDiv.hidden = true;
    }
}

function sortAlphabetically(companies) {
    let companiesArray = Array.from(companies);
    companiesArray.sort(function (a, b) {
        let aName = a.getElementsByClassName('companyHeader')[0].innerText;
        let bName = b.getElementsByClassName('companyHeader')[0].innerText;
        if (aName < bName) {
          return -1;
        }
        if (aName > bName) {
          return 1;
        }
        return 0;
      }).forEach(function(val, index) {
        document.getElementsByClassName('companyList')[0].appendChild(val);
      });

      let newCompanyElements = document.getElementsByClassName('company');
      let copy = Array.from(newCompanyElements);
      let companyList = document.getElementsByClassName('companyList')[0];
      for(let i = 0; i < newCompanyElements.length; i++) {
        companyList.removeChild(newCompanyElements[i]);
      }
    return copy;
}

function sortByDomain(domains, companies) {
    let companiesArray = Array.from(companies);
    let companyList = document.getElementsByClassName('companyList')[0];
    for(let i = 0; i < domains.length; i++) {
        let currentDomain = domains[i];
        let formattedDomain = document.createElement('div');
        formattedDomain.classList.add('domainHeading');
        formattedDomain.innerText = currentDomain;
        if(formattedDomain.innerText.trim() === '')
            formattedDomain.innerText = 'Inconnu';
        let elementToBePushed = document.createElement('div');
        elementToBePushed.classList.add('domainDiv');
        elementToBePushed.appendChild(formattedDomain);
        let count = 0;
        for(let j = 0; j < companiesArray.length; j++) {
            let company = companiesArray[j];
            let companyDomain = company.getElementsByClassName('domaine')[0].innerText.trim();
            if(companyDomain === currentDomain) {
                elementToBePushed.appendChild(company);
                count++;
            }
        }
        formattedDomain.innerText = formattedDomain.innerText + " - Quantité d'entreprises : " + count;
        elementToBePushed.setAttribute("domain", currentDomain);
        companyList.appendChild(elementToBePushed);
    }

    let hasCompaniesWithNoDomain = false;
    for(let i = 0; i < companiesArray.length; i++) {
        let company = companiesArray[i];
        let parentNode = company.parentNode;
        let parentClassList = parentNode.className;
        if(parentClassList.indexOf('domainDiv') <= -1) {
            hasCompaniesWithNoDomain = true;
            break;
        }
    }

    if(hasCompaniesWithNoDomain) {
        let formattedMunicipality = document.createElement('div');
        formattedMunicipality.classList.add('domainHeading');
        formattedMunicipality.innerText = 'Inconnu';
        let elementToBePushed = document.createElement('div');
        elementToBePushed.classList.add('domainDiv');
        elementToBePushed.appendChild(formattedMunicipality);
        for(let i = 0; i < companiesArray.length; i++) {
            let company = companiesArray[i];
            let parentNode = company.parentNode;
            if(parentNode === null || parentNode === undefined) {
                elementToBePushed.appendChild(company);
                continue;
            }
            let parentClassList = parentNode.className;
            if(parentClassList.indexOf('domainDiv') <= -1) {
                elementToBePushed.appendChild(company);
            }
        }
        companyList.appendChild(elementToBePushed);
    }

}

function sortAndAddByMunicipality(municipalities, companies) {
    let entries = Object.entries(municipalities);
    let companiesArray = Array.from(companies);
    let companyList = document.getElementsByClassName('companyList')[0];
    for(let i = 0; i < entries.length; i++) {
        let currentMunicipality = entries[i][0];
        let currentPostalCode = entries[i][1];
        let formattedMunicipality = document.createElement('div');
        formattedMunicipality.classList.add('municipalityHeading');
        formattedMunicipality.innerText = currentMunicipality;
        let elementToBePushed = document.createElement('div');
        elementToBePushed.classList.add('municipalityDiv');
        elementToBePushed.appendChild(formattedMunicipality);
        let count = 0;
        for(let j = 0; j < companiesArray.length; j++) {
            let company = companiesArray[j];
            let companyInfo = company.getElementsByTagName('td')[0].innerText;
            if(companyInfo.indexOf(currentMunicipality) > -1 || companyInfo.indexOf(currentPostalCode) > -1) {
                elementToBePushed.appendChild(company);
                count++;
            }
        }
        formattedMunicipality.innerText = formattedMunicipality.innerText + " - Quantité d'entreprises : " + count;
        elementToBePushed.setAttribute("municipality", currentMunicipality);
        companyList.appendChild(elementToBePushed);
    }

    let hasCompaniesWithNoMunicipality = false;
    for(let i = 0; i < companiesArray.length; i++) {
        let company = companiesArray[i];
        let parentNode = company.parentNode;
        let parentClassList = parentNode.className;
        if(parentClassList.indexOf('municipalityDiv') <= -1) {
            hasCompaniesWithNoMunicipality = true;
            break;
        }
    }


    if(hasCompaniesWithNoMunicipality) {
        let formattedMunicipality = document.createElement('div');
        formattedMunicipality.classList.add('municipalityHeading');
        formattedMunicipality.innerText = 'Inconnu';
        let elementToBePushed = document.createElement('div');
        elementToBePushed.classList.add('municipalityDiv');
        elementToBePushed.appendChild(formattedMunicipality);
        for(let i = 0; i < companiesArray.length; i++) {
            let company = companiesArray[i];
            let parentNode = company.parentNode;
            if(parentNode === null || parentNode === undefined) {
                elementToBePushed.appendChild(company);
                continue;
            }

            let parentClassList = parentNode.className;
            if(parentClassList.indexOf('municipalityDiv') <= -1) {
                elementToBePushed.appendChild(company);
            }
        }
        companyList.appendChild(elementToBePushed);
    }
}

function sort(companies) {
    let alphabeticallySortedCompanies = sortAlphabetically(companies);
    let mode = getParameter('mode');
    if( mode == 1 ) {
        let domains = getDomains(companies);
        sortByDomain(domains, alphabeticallySortedCompanies);
        const filteredDomain = getParameter('domain');
        if(filteredDomain)
            filterByDomain(filteredDomain);
    }
    else {
        let municipalities = getMunicipalities(companies);
        sortAndAddByMunicipality(municipalities, alphabeticallySortedCompanies);
        const filteredMunicipality = getParameter('municipality');
        if(filteredMunicipality)
            filterByMunicipality(filteredMunicipality);
    }
}


function sortCompanies() {
    let companies = document.querySelectorAll('.company');
    let companyList = document.getElementsByClassName('companyList')[0];
    for(let i = 0; i < companies.length; i++) {
        companyList.removeChild(companies[i]);
    }
    sort(companies);
}

sortCompanies();
