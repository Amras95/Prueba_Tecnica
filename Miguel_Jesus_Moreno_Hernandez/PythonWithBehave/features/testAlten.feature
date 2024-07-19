Feature: Test Alten

  Scenario Outline: Verify Sector pages for each sector
    Given I have opened the Alten Page
    When I open the dropdown Sectores and choose "<Sector>"
    Then I should see the page for "<Sector>"
    And I go to the home page
    And I close the browser and generate a CSV for "<Sector>"

    Examples:
      | Sector                         |
      | Administración Pública         |
      | Aeronáutica                    |
      | Automoción                     |
      | Banca, Finanzas & Seguros      |
      | Defensa, Seguridad & Naval     |
      | Energía & Medio Ambiente       |
      | Espacio                        |
      | Ferroviario & Movilidad        |
      | Life Sciences & Salud          |

  Scenario: Verify Search text
    Given I have opened the Alten Page
    When I search text "Noticias"
    Then I close the browser and generate a CSV for "Noticias"