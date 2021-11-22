Feature: The recommendations service back-end
    As a recommendations Owner
    I need a RESTful catalog service
    So that I can keep track of all my recommendations

    Background:
        Given the following recommendations
            | product_id | rec_product_id | type          | interested |
            | 13         | 3              | CrossSell     | 70         |
            | 16         | 5              | UpSell        | 9          |
            | 21         | 8              | Complementary | 12         |

    Scenario: The server is running
        When I visit the "Home Page"
        Then I should see "Recommendations RESTful Service" in the title
        And I should not see "404 Not Found"

    Scenario: Create a Pet and Retrieve it (2 scenarios combined)
        When I visit the "Home Page"
        And I set the "Product_ID" to "30"
        And I set the "Rec_Product_Id" to "40"
        And I select "UpSell" in the "Type" dropdown
        And I press the "Create" button
        Then I should see the message "Success"
        When I copy the "ID" field
        And I press the "Clear" button
        Then the "ID" field should be empty
        And the "Product_ID" field should be empty
        And the "Rec_Product_ID" field should be empty
        When I paste the "ID" field
        And I press the "Retrieve" button
        Then I should see "30" in the "Product_ID" field
        And I should see "40" in the "Rec_Product_ID" field
        And I should see "UpSell" in the "Type" dropdown

    Scenario: List all recommendations
        When I visit the "Home Page"
        And I press the "Search" button
        Then I should see "13" in the results
        And I should see "16" in the results
        And I should not see "21" in the results

    Scenario: Search all product with Rec_Product_ID "3"
        When I visit the "Home Page"
        And I set the "Rec_Product_ID" to "3"
        And I press the "Search" button
        Then I should see "13" in the results
        And I should not see "16" in the results
        And I should not see "21" in the results

    Scenario: Update a Recommendation
        When I visit the "Home Page"
        And I set the "Product_ID" to "13"
        And I press the "Search" button
        Then I should see "13" in the "Product_ID" field
        And I should see "3" in the "Rec_Product_ID" field
        When I change "Product_ID" to "88"
        And I press the "Update" button
        Then I should see the message "Success"
        When I copy the "ID" field
        And I press the "Clear" button
        And I paste the "ID" field
        And I press the "Retrieve" button
        Then I should see "88" in the "Product_ID" field
        When I press the "Clear" button
        And I press the "Search" button
        Then I should see "88" in the results
        Then I should not see "13" in the results

    Scenario: Delete a Recommendation
        When I visit the "Home Page"
        And I set the "Product_ID" to "16"
        And I press the "Delete" button
        And I press the "Clear" button
        And I press the "Search" button
        Then I should not see "16" in the results

    Scenario: Increase the Interested Count of a Recommendation
        When I visit the "Home Page"
        And I set the "product_id" to "21"
        And I copy the "ID" field
        And I press the "Clear" button
        And I paste the "ID" field
        And I press the "Intrested" button
        Then I should see "13" in the "Interested" field