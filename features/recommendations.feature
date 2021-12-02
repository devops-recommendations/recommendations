Feature: The recommendations service back-end
    As a recommendations Owner
    I need a RESTful catalog service
    So that I can keep track of all my recommendations

    Background:
        Given the following recommendations
            | product_id | rec_product_id | type          | interested |
            | 2300       | 1003           | CrossSell     | 170        |
            | 2600       | 1005           | UpSell        | 190        |
            | 2100       | 1008           | Complementary | 160        |

    Scenario: The server is running
        When I visit the "Home Page"
        Then I should see "Recommendations RESTful Service" in the title
        And I should not see "404 Not Found"

    Scenario: Create a Pet and Retrieve it (2 scenarios combined)
        When I visit the "Home Page"
        And I set the "Product_ID" to "2315"
        And I set the "Rec_Product_Id" to "1300"
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
        Then I should see "2315" in the "Product_ID" field
        And I should see "1300" in the "Rec_Product_ID" field
        And I should see "UpSell" in the "Type" dropdown

    Scenario: List all recommendations
        When I visit the "Home Page"
        And I press the "Search" button
        Then I should see "2300" in the results
        And I should see "2600" in the results
        And I should not see "3999" in the results

    Scenario: Search all product with Rec_Product_ID "1003"
        When I visit the "Home Page"
        And I set the "Rec_Product_ID" to "1003"
        And I press the "Search" button
        Then I should see "2300" in the results
        And I should not see "2600" in the results
        And I should not see "2100" in the results

    Scenario: Update a Recommendation
        When I visit the "Home Page"
        And I set the "Product_ID" to "2300"
        And I press the "Search" button
        Then I should see "2300" in the "Product_ID" field
        And I should see "1003" in the "Rec_Product_ID" field
        When I change "Product_ID" to "2888"
        And I press the "Update" button
        Then I should see the message "Success"
        When I copy the "ID" field
        And I press the "Clear" button
        And I paste the "ID" field
        And I press the "Retrieve" button
        Then I should see "2888" in the "Product_ID" field
        When I press the "Clear" button
        And I press the "Search" button
        Then I should see "2888" in the results
        Then I should not see "2300" in the results

    Scenario: Delete a Recommendation
        When I visit the "Home Page"
        And I set the "Product_ID" to "2100"
        And I press the "Search" button
        And I copy the "ID" field
        And I press the "Clear" button
        And I paste the "ID" field
        And I press the "Delete" button
        Then I should see the message "Recommendation has been Deleted!"

    Scenario: Increase the Interested Count of a Recommendation
        When I visit the "Home Page"
        And I set the "product_id" to "2100"
        And I press the "Search" button
        And I copy the "ID" field
        And I press the "Clear" button
        And I paste the "ID" field
        And I press the "Interested" button
        Then I should see the message "Updated Interested Count!"