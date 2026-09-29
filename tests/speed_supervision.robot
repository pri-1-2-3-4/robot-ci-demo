*** Settings ***
Documentation     Speed supervision checks, similar in spirit to ATP overspeed protection.
Library           ../libraries/SpeedSupervision.py
Test Tags         regression

*** Test Cases ***
Normal Running Below Limit
    [Tags]    smoke
    Set Speed Limit    80
    Set Train Speed    60
    Supervision Status Should Be    NORMAL

Overspeed Triggers Brake
    [Tags]    smoke
    Set Speed Limit    80
    Set Train Speed    95
    Supervision Status Should Be    WARNING

Speed Boundaries Around The Limit
    [Documentation]    Boundary value analysis: data-driven with a template keyword.
    [Template]    Status At Speed Should Be
    80    NORMAL
    81    WARNING
    85    WARNING
    86    BRAKE

*** Keywords ***
Status At Speed Should Be
    [Arguments]    ${speed}    ${expected}
    Set Speed Limit    80
    Set Train Speed    ${speed}
    Supervision Status Should Be    ${expected}
