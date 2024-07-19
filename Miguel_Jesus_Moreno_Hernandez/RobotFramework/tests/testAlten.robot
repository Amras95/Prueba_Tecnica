*** Settings ***
Resource    ../resources/keywords/keywords.robot

Suite Teardown    Run Keyword If Any Tests Failed    Log Error And Generate CSV     ${PREV_TEST_MESSAGE}
*** Test Cases ***

Verify Sector pages
    Open Alten Page
    Open drowpdown Sectores and choose "Administración Pública"
    Open drowpdown Sectores and choose "Aeronáutica"
    Open drowpdown Sectores and choose "Automoción"
    Open drowpdown Sectores and choose "Banca, Finanzas & Seguros"
    Open drowpdown Sectores and choose "Defensa, Seguridad & Naval"
    Open drowpdown Sectores and choose "Energía & Medio Ambiente"
    Open drowpdown Sectores and choose "Espacio"
    Open drowpdown Sectores and choose "Ferroviario & Movilidad"
    Open drowpdown Sectores and choose "Life Sciences & Salud"
    Go To Home Page
    Close Browser and generate csv

Verify Sector pages with failed sector
    Open Alten Page
    Open drowpdown Sectores and choose "Error option"
    Close Browser and generate csv

Verify Search text
    Open Alten Page
    Search text "Noticias" 
    Close Browser and generate csv
