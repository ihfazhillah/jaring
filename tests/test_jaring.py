import unittest
from unittest.mock import patch, MagicMock, mock_open
import sys
from pathlib import Path

# Add the parent directory to the sys.path to allow importing jaring.py
sys.path.insert(0, str(Path(__file__).parent.parent))

from jaring import parse_file, generate_image_from_text # Import the new function

class TestParseFile(unittest.TestCase):

    @patch('jaring.generate_image_from_text') # Mock the new function
    @patch('jaring.frontmatter.load')
    @patch('jaring.Path')
    @patch('builtins.open', new_callable=mock_open)
    def test_single_img_notation(self, mock_file_open, MockPath, mock_frontmatter_load, mock_generate_image_from_text):
        # Mock frontmatter.load to return a post object
        mock_post = MagicMock()
        mock_post.metadata = {'id': 'test-post-1'}
        mock_post.content = "This is some text. !img{Image Text Here} More text."
        mock_frontmatter_load.return_value = mock_post

        # Mock Path methods (still needed for image_path in generate_image_from_text if not fully mocked)
        mock_path_instance = MagicMock()
        MockPath.return_value = mock_path_instance
        mock_path_instance.parent.mkdir.return_value = None # Mock mkdir
        mock_path_instance.__truediv__.return_value = mock_path_instance # Mock / operator

        # Mock the return value of generate_image_from_text
        mock_generate_image_from_text.return_value = 'assets/images/mocked-image.png'

        result = parse_file("dummy_path.md")

        # Assertions
        self.assertEqual(result['metadata']['id'], 'test-post-1')
        self.assertEqual(result['content'], "This is some text. Image Text Here More text.") # Notation removed, text remains
        self.assertEqual(result['metadata']['og_image'], 'assets/images/mocked-image.png')

        # Verify generate_image_from_text was called
        mock_generate_image_from_text.assert_called_once_with("Image Text Here", "test-post-1", 0)

    @patch('jaring.generate_image_from_text')
    @patch('jaring.frontmatter.load')
    @patch('jaring.Path')
    @patch('builtins.open', new_callable=mock_open)
    def test_multiple_img_notations(self, mock_file_open, MockPath, mock_frontmatter_load, mock_generate_image_from_text):
        mock_post = MagicMock()
        mock_post.metadata = {'id': 'test-post-2'}
        mock_post.content = "First !img{Image One}. Second !img{Image Two}."
        mock_frontmatter_load.return_value = mock_post

        mock_path_instance = MagicMock()
        MockPath.return_value = mock_path_instance
        mock_path_instance.parent.mkdir.return_value = None
        mock_path_instance.__truediv__.return_value = mock_path_instance

        # Mock the return values for multiple calls
        mock_generate_image_from_text.side_effect = [
            'assets/images/mocked-image-0.png',
            'assets/images/mocked-image-1.png'
        ]

        result = parse_file("dummy_path.md")

        self.assertEqual(result['metadata']['id'], 'test-post-2')
        self.assertEqual(result['content'], "First Image One. Second Image Two.")
        self.assertEqual(result['metadata']['og_image'], 'assets/images/mocked-image-0.png') # First image for og_image

        # Verify generate_image_from_text was called twice with correct arguments
        self.assertEqual(mock_generate_image_from_text.call_count, 2)
        mock_generate_image_from_text.assert_has_calls([
            unittest.mock.call("Image One", "test-post-2", 0),
            unittest.mock.call("Image Two", "test-post-2", 1)
        ])

    @patch('jaring.generate_image_from_text')
    @patch('jaring.frontmatter.load')
    @patch('jaring.Path')
    @patch('builtins.open', new_callable=mock_open)
    def test_img_notation_multiline(self, mock_file_open, MockPath, mock_frontmatter_load, mock_generate_image_from_text):
        mock_post = MagicMock()
        mock_post.metadata = {'id': 'test-post-3'}
        mock_post.content = "Start of text.\n!img{Multi-line\nImage Text\nHere.}\nEnd of text."
        mock_frontmatter_load.return_value = mock_post

        mock_path_instance = MagicMock()
        MockPath.return_value = mock_path_instance
        mock_path_instance.parent.mkdir.return_value = None
        mock_path_instance.__truediv__.return_value = mock_path_instance

        mock_generate_image_from_text.return_value = 'assets/images/mocked-image-multiline.png'

        result = parse_file("dummy_path.md")

        self.assertEqual(result['metadata']['id'], 'test-post-3')
        self.assertEqual(result['content'], "Start of text.\nMulti-line\nImage Text\nHere.\nEnd of text.")
        self.assertEqual(result['metadata']['og_image'], 'assets/images/mocked-image-multiline.png')
        mock_generate_image_from_text.assert_called_once_with("Multi-line\nImage Text\nHere.", "test-post-3", 0)

    @patch('jaring.generate_image_from_text')
    @patch('jaring.frontmatter.load')
    @patch('jaring.Path')
    @patch('builtins.open', new_callable=mock_open)
    def test_no_img_notation(self, mock_file_open, MockPath, mock_frontmatter_load, mock_generate_image_from_text):
        mock_post = MagicMock()
        mock_post.metadata = {'id': 'test-post-4'}
        mock_post.content = "This is just plain text with no image notation."
        mock_frontmatter_load.return_value = mock_post

        mock_path_instance = MagicMock()
        MockPath.return_value = mock_path_instance
        mock_path_instance.parent.mkdir.return_value = None
        mock_path_instance.__truediv__.return_value = mock_path_instance

        result = parse_file("dummy_path.md")

        self.assertEqual(result['metadata']['id'], 'test-post-4')
        self.assertEqual(result['content'], "This is just plain text with no image notation.")
        self.assertIsNone(result['metadata']['og_image']) # No image generated, so og_image should be None

        mock_generate_image_from_text.assert_not_called() # generate_image_from_text should not be called

    @patch('jaring.generate_image_from_text')
    @patch('jaring.frontmatter.load')
    @patch('jaring.Path')
    @patch('builtins.open', new_callable=mock_open)
    def test_image_generation_failure(self, mock_file_open, MockPath, mock_frontmatter_load, mock_generate_image_from_text):
        mock_post = MagicMock()
        mock_post.metadata = {'id': 'test-post-5'}
        mock_post.content = "!img{This should fail}"
        mock_frontmatter_load.return_value = mock_post

        mock_path_instance = MagicMock()
        MockPath.return_value = mock_path_instance
        mock_path_instance.parent.mkdir.return_value = None
        mock_path_instance.__truediv__.return_value = mock_path_instance

        # Simulate an exception during image generation
        mock_generate_image_from_text.side_effect = Exception("Simulated Image Generation Error")

        with self.assertRaisesRegex(Exception, "Simulated Image Generation Error"):
            parse_file("dummy_path.md")

        mock_generate_image_from_text.assert_called_once_with("This should fail", "test-post-5", 0)

    @patch('jaring.generate_image_from_text')
    @patch('jaring.frontmatter.load')
    @patch('jaring.Path')
    @patch('builtins.open', new_callable=mock_open)
    def test_img_notation_newline_preservation(self, mock_file_open, MockPath, mock_frontmatter_load, mock_generate_image_from_text):
        mock_post = MagicMock()
        mock_post.metadata = {'id': 'test-post-6'}
        # The crucial part: !img{} is at the end of a line, followed by a newline, then more text
        mock_post.content = "Line before. !img{Image Text}\nLine after."
        mock_frontmatter_load.return_value = mock_post

        mock_path_instance = MagicMock()
        MockPath.return_value = mock_path_instance
        mock_path_instance.parent.mkdir.return_value = None
        mock_path_instance.__truediv__.return_value = mock_path_instance

        mock_generate_image_from_text.return_value = 'assets/images/mocked-image-6.png'

        result = parse_file("dummy_path.md")

        self.assertEqual(result['metadata']['id'], 'test-post-6')
        # Expected: "Line before. Image Text\nLine after."
        self.assertEqual(result['content'], "Line before. Image Text\nLine after.")
        self.assertEqual(result['metadata']['og_image'], 'assets/images/mocked-image-6.png')
        mock_generate_image_from_text.assert_called_once_with("Image Text", "test-post-6", 0)

if __name__ == '__main__':
    unittest.main()