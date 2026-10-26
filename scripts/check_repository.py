#!/usr/bin/env python3
"""离线仓库检查，仅使用Python 3.9及以上版本的标准库。

检查当前工作区，不检查历史提交，也不判断Demo的正确性。
Markdown解析仅支持说明文档列出的常见语法，不涵盖全部GitHub扩展语法。
"""

import argparse
import datetime
import html
import os
from pathlib import Path
import re
import subprocess
import sys
import unicodedata
from urllib.parse import unquote, urlsplit


ROOT_FILES = (
    'README.md', 'CATALOG.md', 'SCHEDULE.md', 'CONTRIBUTING.md', '.gitignore',
    'sessions/README.md', '.github/PULL_REQUEST_TEMPLATE.md',
    '.github/workflows/check.yml',
    '.github/ISSUE_TEMPLATE/book-proposal.md',
    '.github/ISSUE_TEMPLATE/seminar-task.md',
    '.github/ISSUE_TEMPLATE/question-errata.md',
    'templates/book.md', 'templates/notes.md', 'templates/presentation.md',
    'templates/demo.md', 'templates/session.md',
)
BOOK_FILES = ('README.md', 'schedule.md', 'resources.md',
              'notes/README.md', 'slides/README.md',
              'demos/README.md', 'exercises/README.md')
CHAPTER = r'ch(?:0[1-9]|[1-9][0-9]+)'
SLUG = r'[a-z0-9]+(?:-[a-z0-9]+)*'
SLIDE_NAME = re.compile(r'(\d{4}-\d{2}-\d{2})-' + CHAPTER + '-' + SLUG
                        + r'\.(pptx|pdf|odp|key)$')
BAD_DIRS = {'.venv', 'venv', '__pycache__', 'node_modules', '.cache',
            '.pytest_cache', '.mypy_cache', 'build', 'dist', 'target',
            'tmp', 'temp', 'local-resources', 'data-private', '.idea', '.vscode'}
BAD_SUFFIXES = {'.pyc', '.pyo', '.swp', '.swo', '.tmp', '.log', '.aux',
                '.out', '.toc', '.class', '.o'}
SECRET_PATTERNS = (
    ('private-key', re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')),
    ('github-token', re.compile(r'\bgh[pousr]_[A-Za-z0-9]{36,}\b')),
    ('github-fine-grained-token', re.compile(r'\bgithub_pat_[A-Za-z0-9_]{40,}\b')),
    ('aws-access-key', re.compile(r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b')),
    ('service-api-key', re.compile(r'\bsk-(?:proj-)?[A-Za-z0-9_-]{32,}\b')),
    ('credential-assignment', re.compile(
        r'''(?im)^\s*["']?(?:api[_-]?key|access[_-]?token|password|secret[_-]?key)["']?\s*[:=]\s*["']([A-Za-z0-9_+/=-]{20,})["']''')),
)
TARGET = r'(?:<[^>\n]+>|(?:[^\s()]+|\([^()]*\))+)'
INLINE_LINK = re.compile(r'!?\[[^\]\n]*\]\(\s*(' + TARGET
                         + r')(?:\s+["\'][^\n]*?["\'])?\s*\)')
REFERENCE_DEF = re.compile(r'^\s{0,3}\[([^\]]+)\]:\s*(' + TARGET + ')', re.M)
REFERENCE_USE = re.compile(r'!?\[([^\]\n]+)\]\[([^\]\n]*)\]')
HTML_LINK = re.compile(r'''\b(?:href|src)\s*=\s*["']([^"']+)["']''', re.I)


def markdown_prose(text):
    """去除围栏代码块和行内代码，保留换行以便定位问题。"""
    lines = []
    fence = None
    for line in text.splitlines(keepends=True):
        match = re.match(r'^\s{0,3}(`{3,}|~{3,})', line)
        if fence:
            if match and match[1][0] == fence[0] and len(match[1]) >= len(fence):
                fence = None
            lines.append('\n')
        elif match:
            fence = match[1]
            lines.append('\n')
        else:
            lines.append(line)
    return re.sub(r'(`+)[^\n]*?\1', '', ''.join(lines))


def anchors(text):
    seen, result = {}, set()
    for heading in re.findall(r'^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$',
                              markdown_prose(text), re.M):
        heading = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', heading)
        heading = re.sub(r'<[^>]+>', '', html.unescape(heading)).lower()
        slug = ''.join(c for c in heading if c in ' -_'
                       or unicodedata.category(c)[0] in 'LNM').replace(' ', '-')
        number = seen.get(slug, 0)
        seen[slug] = number + 1
        result.add(slug + ('-' + str(number) if number else ''))
    result.update(re.findall(r'''\b(?:id|name)=["']([^"']+)["']''', text))
    return result


def inventory(root, all_files=False):
    if not all_files:
        try:
            result = subprocess.run(
                ['git', '-C', str(root), 'ls-files', '-z', '--cached',
                 '--others', '--exclude-standard'], capture_output=True, check=True)
            return sorted({Path(os.fsdecode(p)) for p in result.stdout.split(b'\0') if p})
        except (OSError, subprocess.CalledProcessError):
            pass
    result = []
    for base, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = [d for d in dirs if d != '.git']
        for d in list(dirs):
            path = Path(base) / d
            if path.is_symlink():
                result.append(path.relative_to(root))
                dirs.remove(d)
        result.extend((Path(base) / f).relative_to(root) for f in files if f != '.git')
    return sorted(result)


def valid_date(value):
    try:
        datetime.date.fromisoformat(value)
        return True
    except ValueError:
        return False


def check_repository(root, all_files=False):
    root = root.resolve()
    files = inventory(root, all_files)
    names = {p.as_posix() for p in files}
    errors, warnings = [], []

    def fail(path, message):
        errors.append('{}: {}'.format(path, message))

    def require(path):
        if path not in names or not (root / path).is_file():
            fail(path, '待检查文件中缺少必需文件')

    for path in ROOT_FILES:
        require(path)
    book_ids = {p.parts[1] for p in files if len(p.parts) > 2 and p.parts[0] == 'books'}
    if (root / 'books').is_dir():
        book_ids.update(p.name for p in (root / 'books').iterdir() if p.is_dir())
    if not book_ids:
        fail('books', '至少需要一个教材档案')
    for book in sorted(book_ids):
        if not re.fullmatch(r'[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*', book):
            fail('books/' + book, '教材编号不符合命名规范')
        for name in BOOK_FILES:
            require('books/{}/{}'.format(book, name))

    demo_dirs = set()
    for p in files:
        parts = p.parts
        path = root / p
        if path.is_symlink() or any((root.joinpath(*parts[:i])).is_symlink()
                                    for i in range(1, len(parts))):
            fail(p, '不支持符号链接，请在说明文档中提供引用链接')
            continue
        if not path.is_file():
            fail(p, '工作区缺少已跟踪的文件，或该条目类型不受支持')
            continue
        if any(part in BAD_DIRS for part in parts[:-1]):
            fail(p, '包含缓存、依赖、构建产物或仅供本地使用的目录')
        if (p.name in {'.DS_Store', 'Thumbs.db'} or p.name.startswith('~$')
                or p.name.endswith('~') or p.suffix.lower() in BAD_SUFFIXES):
            fail(p, '包含临时文件或生成文件')
        slide = len(parts) >= 4 and parts[0] == 'books' and parts[2] == 'slides'
        if (p.name == '.env' or (p.name.startswith('.env.') and p.name != '.env.example')
                or p.name.lower() in {'credentials.json', 'secrets.json', 'id_rsa', 'id_ed25519'}
                or p.suffix.lower() in {'.pem', '.p12', '.pfx'}
                or (p.suffix.lower() == '.key' and not (slide and SLIDE_NAME.fullmatch(p.name)))):
            fail(p, '文件名涉及敏感信息，请勿提交凭据')
        size = path.stat().st_size
        if size > 25 * 1024 * 1024:
            fail(p, '文件超过25 MiB大小限制')
            continue
        if size > 10 * 1024 * 1024:
            warnings.append('{}: 文件超过10 MiB，建议压缩体积'.format(p))

        if parts[0] == 'sessions' and p.name != 'README.md':
            if len(parts) != 2 or p.suffix != '.md' or not valid_date(p.stem):
                fail(p, '研讨记录路径须采用sessions/YYYY-MM-DD.md格式')
        if len(parts) >= 4 and parts[0] == 'books':
            category = parts[2]
            if category not in {'notes', 'slides', 'demos', 'exercises'}:
                fail(p, '材料类别不符合目录规范')
            if category == 'demos':
                if len(parts) == 4 and p.name != 'README.md':
                    fail(p, 'Demo文件须放入chXX-topic/独立目录')
                elif len(parts) >= 5:
                    demo_dirs.add('/'.join(parts[:4]))
                    if not re.fullmatch(CHAPTER + '-' + SLUG, parts[3]):
                        fail(p, 'Demo目录名不符合规范')
            elif category in {'notes', 'exercises'} and p.suffix == '.md' and p.name != 'README.md':
                pattern = CHAPTER + ('-ex[0-9]+-' if category == 'exercises' else '-') + SLUG + r'\.md'
                if not re.fullmatch(pattern, p.name):
                    fail(p, '章节材料文件名不符合规范')
            elif slide and p.suffix.lower() in {'.pptx', '.pdf', '.odp', '.key'}:
                match = SLIDE_NAME.fullmatch(p.name)
                if not match or not valid_date(match[1]):
                    fail(p, '汇报文件名或日期不符合规范')
                elif p.suffix == '.pdf' and not any(
                        str(p.with_suffix(ext)) in names for ext in ('.pptx', '.odp', '.key')):
                    fail(p, '汇报PDF缺少同名主体的可编辑源文件')
        raw = path.read_bytes()
        if b'\0' in raw:
            continue
        try:
            text = raw.decode('utf-8')
        except UnicodeDecodeError:
            if p.suffix == '.md':
                fail(p, 'Markdown文件须使用UTF-8编码')
            continue
        for label, pattern in SECRET_PATTERNS:
            match = pattern.search(text)
            if match:
                line = text[:match.start()].count('\n') + 1
                fail('{}:{}'.format(p, line), '疑似敏感凭据（{}）'.format(label))
        if p.suffix == '.md' and parts[0] != 'templates' and '{{' in text:
            fail(p, 'templates/以外的文件中存在未填写的模板占位符')
        if p.suffix != '.md':
            continue
        prose = markdown_prose(text)
        targets = [(m[1], m.start()) for m in INLINE_LINK.finditer(prose)]
        targets += [(m[1], m.start()) for m in HTML_LINK.finditer(prose)]
        refs = {m[1].strip().casefold(): m[2] for m in REFERENCE_DEF.finditer(prose)}
        targets += [(m[2], m.start()) for m in REFERENCE_DEF.finditer(prose)]
        for match in REFERENCE_USE.finditer(prose):
            key = (match[2] or match[1]).strip().casefold()
            if key not in refs:
                fail(p, 'Markdown链接引用尚未定义：' + key)
        # 简写引用仅在对应定义存在时才构成链接。
        for target, offset in targets:
            target = html.unescape(target.strip('<>'))
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc:
                continue
            location = '{}:{}'.format(p, prose[:offset].count('\n') + 1)
            if parsed.path.startswith('/'):
                fail(location, '使用了本地绝对路径，请改为仓库内的相对链接')
                continue
            dest = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            try:
                rel = dest.relative_to(root).as_posix()
            except ValueError:
                fail(location, '相对链接指向仓库之外')
                continue
            present = rel in names or any(n.startswith(rel.rstrip('/') + '/') for n in names)
            if dest == root:
                present = True
            if not dest.exists() or not present:
                fail(location, '本地链接目标不存在：' + target)
            elif parsed.fragment and dest.suffix == '.md':
                try:
                    dest_text = dest.read_text(encoding='utf-8')
                except (OSError, UnicodeDecodeError):
                    fail(location, '无法读取Markdown链接目标')
                    continue
                if unquote(parsed.fragment) not in anchors(dest_text):
                    fail(location, 'Markdown标题锚点不存在：' + target)
    # 同时检查本地空Demo目录，因为Git无法保存空目录。
    for book in book_ids:
        base = root / 'books' / book / 'demos'
        if base.is_dir():
            for directory in base.iterdir():
                if directory.is_dir():
                    demo_dirs.add(directory.relative_to(root).as_posix())
    for demo in sorted(demo_dirs):
        require(demo + '/README.md')
    return errors, warnings, len(files)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--all-files', action='store_true', help='同时检查被Git忽略的本地文件')
    args = parser.parse_args()
    errors, warnings, count = check_repository(args.root, args.all_files)
    for message in errors:
        print('错误：' + message)
    for message in warnings:
        print('警告：' + message)
    print('已检查{}个文件：{}个错误，{}个警告。'.format(count, len(errors), len(warnings)))
    print('人工检查事项：版权、学术质量、外部链接、二进制文件内容及Demo正确性。')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
