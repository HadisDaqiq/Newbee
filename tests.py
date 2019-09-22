

import unittest
import server
from model import connect_to_db

#     """

#     tests.addTests(doctest.DocTestSuite(arithmetic))
#     tests.addTests(doctest.DocFileSuite("tests.txt"))
#     return tests



class Test_homepage(unittest.TestCase):
    """Examples of unit tests: discrete code testing."""

    def test_landing_page(self):
        """Make sure index page returns correct HTML."""
        # Create a test client
        client = server.app.test_client()

        # Use the test client to make requests
        result = client.get('/', follow_redirects=True)

        # Compare result.data with assert method
        self.assertIn(b'<p class="navbar-text">Already have an account?</p>', 
            result.data)

            



    def test_logPage(self):
        """Make sure index page returns correct HTML."""

        # Create a test client
        client = server.app.test_client()

        # Use the test client to make requests
        result = client.post('/login', follow_redirects=True, data={'username':'sadaqiq@gmail.com',
                                            'password':'hadis'})

        print("it is printing ")

        # Compare result.data with assert method
        self.assertIn(b'New Event', result.data)
        


 




if __name__ == "__main__":

    connect_to_db(server.app)

    #app.run(port=5000, host='0.0.0.0')

    # If called like a script, run our tests
    unittest.main()




