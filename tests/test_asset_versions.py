from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from build import versioned_asset


class AssetVersionTests(unittest.TestCase):
    def test_style_changes_refresh_url_but_checkout_line_endings_do_not(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            asset = root / 'style.css'
            with patch('build.ROOT', root):
                asset.write_bytes(b'.paper-step { color: blue; }\n')
                original = versioned_asset('style.css')
                asset.write_bytes(b'.paper-step { color: blue; }\r\n')
                self.assertEqual(versioned_asset('style.css'), original)
                asset.write_bytes(b'.paper-step { color: green; }\n')
                self.assertNotEqual(versioned_asset('style.css'), original)
