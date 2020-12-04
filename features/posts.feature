Feature: showing off behave

  @fixture.webserver
  Scenario: create a post
    Given We are initialized successfully
      When A post is created with data
      | body          | title  | userid |
      | A sky is nice | Sunday | 1      |
      Then We can retrieve a post with data
      | body          | title  | userid |
      | A sky is nice | Sunday | 1      |