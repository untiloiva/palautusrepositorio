
*** Settings ***
Resource    resource.robot
Suite Setup    Open And Configure Browser
Suite Teardown    Close Browser
Test Setup    Reset Application Create User And Go To Register Page

*** Test Cases ***
Register With Valid Username And Password
    Set Registration Details    matti    salasana123
    Click    button >> text=Register
    Get Title    ==    Welcome to Ohtu Application!

Register With Too Short Username And Valid Password
    Set Registration Details    ma    salasana123
    Click    button >> text=Register
    Register Page Should Be Open

Register With Valid Username And Too Short Password
    Set Registration Details    matti    sala
    Click    button >> text=Register
    Register Page Should Be Open

Register With Username That Is Already In Use
    Set Registration Details    kalle    salasana123
    Click    button >> text=Register
    Register Page Should Be Open

*** Keywords ***
Reset Application Create User And Go To Register Page
    Reset Application
    Create User    kalle    kalle123
    Go To    ${REGISTER_URL}

Set Registration Details
    [Arguments]    ${username}    ${password}
    Fill Text    id=username    ${username}
    Fill Secret    id=password    $password
    Fill Secret    id=password_confirmation    $password
