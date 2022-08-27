Feature: Browsing pizzas

    Scenario: Browse available pizzas
        Given there are a pizza "margherita" in the menu
        And there are a pizza "quattro stagioni" in the menu
        When I want to browse all available pizzas
        Then I see 2 pizzas

    Scenario: There are no pizzas in the menu
        Given there are no pizzas in the menu
        When I want to browse all available pizzas
        Then I see there are no pizzas
