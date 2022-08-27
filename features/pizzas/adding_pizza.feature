Feature: Add a pizza

    Scenario: Add a new pizza
        Given the pizza "margherita" has next toppings: mozzarella, basil
        When I want to sell it
        Then it will be available in the menu
