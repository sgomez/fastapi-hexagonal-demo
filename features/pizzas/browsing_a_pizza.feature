Feature: Browsing pizzas

    Scenario: Browse one pizza details
        Given there are a pizza "margherita" in the menu
        When I want to browse it
        Then I see its details

    Scenario: Browse one pizza that does not exists
        When I want to browse a pizza than does not exists
        Then I see the pizza does not exist
