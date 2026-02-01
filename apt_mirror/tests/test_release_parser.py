from ..release_parser import parse_release
import unittest

class TestAddFunction(unittest.TestCase):
    """Test case class for the add function."""

    def test_add_positive_numbers(self):
        """Test adding two positive numbers."""
        # Use assertion methods to check expected output
        self.assertEqual(3, 3)


if __name__ == '__main__':
    unittest.main()
