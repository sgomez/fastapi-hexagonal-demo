Feature: Add a pizza

    Scenario: Add a new pizza
        Given the pizza "margherita" has next toppings: mozzarella, basil
        When I want to sell it at 10 euros
        Then it will be available in the menu


    Scenario: Cannot add a pizza with a duplicated name
        Given the pizza "margherita" has next toppings: mozzarella, basil
        And it is in the menu at 10 euros
        When I want to add another pizza "margherita"
        Then I get a duplicated name error
