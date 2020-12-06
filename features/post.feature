Feature: showing off behave

  Scenario: create a post
    Given We are in the initial state
      When A post is created with data
      | body          | title  | userid |
      | A sky is nice | Sunday | 1      |
      Then We can retrieve only one post with data
      | body          | title  | userid |
      | A sky is nice | Sunday | 1      |