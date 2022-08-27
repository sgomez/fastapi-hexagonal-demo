Feature: Pizza unique name validation

    Scenario: Cannot add a pizza with a duplicated name
        Given there are a pizza "margherita" in the menu
        And I want to create another pizza "margherita"
        When I want to sell it
        Then I get a duplicated name error
