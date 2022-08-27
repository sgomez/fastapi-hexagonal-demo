Feature: Pizza validation

    Scenario: Trying to add a pizza with a long name
        Given I want to add a pizza with a name longer than 100 characters
        When I want to sell it
        Then I get a invalid name error


    Scenario: Trying to add a pizza with an empty name
        Given I want to add a pizza with an empty name
        When I want to sell it
        Then I get a invalid name error
