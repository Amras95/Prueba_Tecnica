*** Variables ***
${URL}    https://www.alten.es/
${BROWSER}    Chrome
${BUT_ACCEPT_COOKIES}    //button[@id="tarteaucitronPersonalize2"]
${HOME}    Home - ALTEN Spain
${BUT_HOME}    //ul[@id="menu-header-es-1"]//span[text()="Home"]
${DWN_SECTORES}    //ul[@id="menu-header-es-1"]//span[text()="Sectores"]
${PATH}    ${CURDIR}/../../results/
${SEARCH_ICON}    //div[@id="header-toolbar-2"]/div//button/span
${SEARCH_INPUT}    //div[@id="header-toolbar-2"]//input
${RESULT_SEARCH}    //div[@id="header-toolbar-2"]//span[contains(text(),"resultados")]