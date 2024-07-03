*** Settings ***
Library    SeleniumLibrary
Library    OperatingSystem
Library    String
Resource    ../resources/variables/variables.robot

*** Keywords ***

Open Alten Page
    [Documentation]    This keyword opens url parameter and maximize window
    Log To Console  \n==== Starting Test ====\n
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Wait Until Element Is Visible    ${BUT_ACCEPT_COOKIES}    30    error= Button Cookies has not loaded
    Wait Until Element Is Enabled    ${BUT_ACCEPT_COOKIES}    30    error= Button Cookies is not enabled
    Click Element    ${BUT_ACCEPT_COOKIES}
    Title Should Be  ${HOME}    message= Page has not loaded correctly
    Capture Page Screenshot  filename=Main_Page_Loaded.png
    Log To Console  \n==== Browser Opened and Maximized ====\n

Open drowpdown Sectores and choose "${option}"
    [Documentation]   Opens dropdown Sectores and choose the option that we gives as parameter
    Log To Console  \n==== Verify step: Open drowpdown Sectores and choose "${option}" ====\n
    Wait Until Element Is Visible    ${DWN_SECTORES}  30  error= The dropdown "Sectores" has not loaded
    Wait Until Element Is Enabled    ${DWN_SECTORES}  30  error= The dropdown "Sectores" is not enabled
    Mouse Over    ${DWN_SECTORES}
    Wait Until Element Is Visible    //ul[@id="menu-header-es-1"]//span[text()="${option}"]   error= The option "${option}" has not loaded correctly
    Wait Until Element Is Enabled    //ul[@id="menu-header-es-1"]//span[text()="${option}"]    error= The option "${option}" is not enabled
    Click Element    //ul[@id="menu-header-es-1"]//span[text()="${option}"]
    ${option_is_visible}    Run Keyword And Ignore Error    Element Should Be Visible  //h1[text()="${option}"]  timeout=10s
    ${option_uppercase}=     Convert to Uppercase    ${option}
    ${option_uppercase_is_visible}    Run Keyword And Ignore Error    Element Should Be Visible  //h1[text()="${option_uppercase}"]  timeout=10s
    Run Keyword If  ${option_is_visible}  Capture Page Screenshot  filename=Page_${option}_Loaded.png
    ...  ELSE IF  ${option_uppercase_is_visible}  Capture Page Screenshot  filename=Page_${option}_Loaded.png
    ...  ELSE    Log Error And Generate CSV    error_message="Page ${option} not loaded correctly"

Go To Home Page
    [Documentation]   Goes to the home page from selected option
    Log To Console  \n==== Verify step: Go To Home ====\n
    Wait Until Element Is Visible    ${BUT_HOME}    30    error= The HOME option is not visible
    Wait Until Element Is Enabled    ${BUT_HOME}    30    error= The HOME option is not enabled
    Click Element    ${BUT_HOME}
    Title Should Be  ${HOME}    message= Page has not loaded correctly
    Capture Page Screenshot  filename=To_Main_Page_Loaded.png

Close Browser and generate csv
    [Documentation]    Closes browser and generate CSV
    Log To Console  \n==== Ending Test====\n
    Create File    path=${PATH}/${TEST NAME}.csv
    ${csv_data}    Create List   Test: ${TEST NAME}   Result: PASSED
    ${csv_data}    Convert To String    ${csv_data}
    Append To File    ${PATH}/${TEST NAME}.csv    ${csv_data}    encoding=UTF-8
    Close Browser

Log Error And Generate CSV
    [Documentation]    Closes browser and generate CSV with errors
    [Arguments]    ${error_message}    
    Log To Console    \n=== ERROR: ${error_message} ===\n
    Create File    path=${PATH}/${PREV_TEST_NAME}.csv
    ${csv_data}    Create List   Test: ${PREV_TEST_NAME}   Result: Failed   Error:${error_message}    
    ${csv_data}    Convert To String    ${csv_data}
    Append To File    ${PATH}/${PREV_TEST_NAME}.csv    ${csv_data}    encoding=UTF-8
    Close Browser
    
Search text "${text}"
    [Documentation]    Search text and verify if its works
    Log To Console    \n=== Verify Search ===\n
    Wait Until Element Is Visible    ${SEARCH_ICON}    30    error="The search icon is not visible"
    Wait Until Element Is Enabled    ${SEARCH_ICON}    30    error="The search icon is not Enabled"
    Click Element    ${SEARCH_ICON}
    Wait Until Element Is Visible    ${SEARCH_INPUT}    30    error="The search input is not visible"
    Wait Until Element Is Enabled    ${SEARCH_INPUT}    30    error="The search input is not Enabled"
    Input Text    ${SEARCH_INPUT}    text=${text}
    Wait Until Element Is Visible    ${RESULT_SEARCH}    30    error="There is no result with the search"
    Log To Console    \n=== Search Verified ===\n
    