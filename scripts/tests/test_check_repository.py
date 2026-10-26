"""Behavior tests: mutate small temporary repositories; never run submitted Demos."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import check_repository as checker


class RepositoryChecks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for name in checker.ROOT_FILES:
            self.write(name, '# Entry\n')
        for name in checker.BOOK_FILES:
            self.write('books/TEST/' + name, '# Entry\n')

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        return path

    def errors(self, all_files=True):
        return checker.check_repository(self.root, all_files)[0]

    def test_valid_archive_and_relative_links(self):
        self.write('README.md', '[book](books/TEST/README.md#entry)\n'
                   '[directory](books/TEST/)\n[external](https://example.org/a_(b))\n'
                   '[named][book]\n[book]: books/TEST/README.md\n'
                   '```md\n[example](missing.md)\n```\n')
        self.assertEqual([], self.errors())

    def test_missing_book_entry_and_demo_readme(self):
        (self.root / 'books/TEST/README.md').unlink()
        self.write('books/TEST/demos/ch02-flow/model.kyx', 'example')
        result = '\n'.join(self.errors())
        self.assertIn('books/TEST/README.md', result)
        self.assertIn('books/TEST/demos/ch02-flow/README.md', result)

    def test_broken_links_references_and_anchor(self):
        self.write('README.md', '[broken](absent.md)\n[ref][undefined]\n'
                   '[anchor](books/TEST/README.md#absent)\n'
                   '<img src="missing.png">\n')
        result = '\n'.join(self.errors())
        for expected in ('absent.md', 'undefined', '#absent', 'missing.png'):
            self.assertIn(expected, result)

    def test_encoded_paths_parentheses_spaces_and_duplicate_headings(self):
        self.write('books/TEST/notes/asset (1).txt', 'fixture')
        self.write('books/TEST/README.md', '# Title\n## Repeat\n## Repeat\n')
        self.write('README.md', '[a](<books/TEST/notes/asset (1).txt>)\n'
                   '[b](books/TEST/notes/asset%20%281%29.txt)\n'
                   '[c](books/TEST/README.md#repeat-1)\n')
        self.assertEqual([], self.errors())

    def test_bad_material_names_and_invalid_date(self):
        self.write('books/TEST/notes/notes.md', '# Note')
        self.write('books/TEST/slides/2026-02-30-ch01-intro.pptx', 'fixture')
        self.write('sessions/2026-02-30.md', '# Not a valid date')
        result = '\n'.join(self.errors())
        for expected in ('notes.md', 'invalid slide filename', 'session record'):
            self.assertIn(expected, result)

    def test_pdf_requires_editable_source(self):
        self.write('books/TEST/slides/2026-10-26-ch01-intro.pdf', 'fixture')
        self.assertTrue(any('editable source' in e for e in self.errors()))
        self.write('books/TEST/slides/2026-10-26-ch01-intro.pptx', 'fixture')
        self.assertEqual([], self.errors())

    def test_sensitive_files_and_redacted_credential_diagnostic(self):
        self.write('.env', 'fixture')
        secret = 'gh' + 'p_' + 'a' * 36
        self.write('books/TEST/demos/ch02-flow/README.md', secret)
        result = '\n'.join(self.errors())
        self.assertIn('sensitive filename', result)
        self.assertIn('possible credential', result)
        self.assertNotIn(secret, result)

    def test_large_file_and_cache(self):
        self.write('books/TEST/demos/ch02-flow/__pycache__/x.pyc', 'cache')
        large = self.root / 'large.bin'
        with large.open('wb') as output:
            output.truncate(26 * 1024 * 1024)
        result = '\n'.join(self.errors())
        self.assertIn('25 MiB', result)
        self.assertIn('cache', result)

    def test_template_placeholders_only_in_templates(self):
        self.write('templates/notes.md', '# {{title}}')
        self.assertEqual([], self.errors())
        self.write('books/TEST/notes/ch01-topic-person.md', '# {{title}}')
        self.assertTrue(any('unfilled template' in e for e in self.errors()))

    def test_links_cannot_escape_and_symlinks_are_not_read(self):
        self.write('README.md', '[outside](../../outside.md)')
        (self.root / 'outside-link').symlink_to(self.root.parent)
        result = '\n'.join(self.errors())
        self.assertIn('escapes repository', result)
        self.assertIn('symlinks are not supported', result)

    def test_git_ignored_files_excluded_but_tracked_secrets_detected(self):
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        self.write('.gitignore', '.env\ncache.tmp\n')
        self.write('.env', 'fixture')
        self.write('cache.tmp', 'fixture')
        self.assertEqual([], self.errors(all_files=False))
        subprocess.run(['git', '-C', str(self.root), 'add', '-f', '.env'], check=True)
        self.assertTrue(any('sensitive filename' in e for e in self.errors(all_files=False)))


if __name__ == '__main__':
    unittest.main()
