import collections

from tests.base import BaseTestCase


from fixtures.users.user_fixture import (
  create_user_response, create_user_mutation,
  get_paginated_users_query,get_paginated_users_response
)

class UsersTestCase(BaseTestCase):
  """Class to test creation of users"""

  def test_succesful_creation_of_users(self):
    """test users are created succesfully"""
    resp = self.query(create_user_mutation)
    self.assertResponseNoErrors(resp, create_user_response)

  def test_listing_paginated_users(self):
    """test successfull querying of users"""
    resp = self.query(get_paginated_users_query)
    self.assertResponseNoErrors(resp, get_paginated_users_response)


