# Book Reading Seminar

**CPS-HCPS Research** · A shared reading and discussion space for textbooks, original learning materials, and reproducible demonstrations.

## Purpose and Scope

We study Cyber-Physical Systems (CPS), Human-Cyber-Physical Systems (HCPS), their theoretical foundations, and related intelligent software research. Each book has its own archive; dated seminar records connect discussions to the materials that informed them.

This repository contains original contributions and resource links. It does not distribute restricted textbooks or teaching materials. See the [contribution and rights policy](CONTRIBUTING.md).

## Current Books

| Book | Status | Entry points |
| --- | --- | --- |
| *Logical Foundations of Cyber-Physical Systems* — André Platzer, Springer, 2018 (LFCPS) | Preparing; coordinator and dates TBD | [Book overview and chapters](books/LFCPS/README.md) · [Reading plan](books/LFCPS/schedule.md) |

See [CATALOG.md](CATALOG.md) for bibliographic records and future books. “Preparing” does not mean that reading or seminars have already taken place.

## Reading Schedule

[Overall schedule and responsibilities](SCHEDULE.md) · [LFCPS proposed sequence](books/LFCPS/schedule.md) · [Seminar records](sessions/README.md).

No seminar date or presenter has been confirmed. The overall schedule is the authoritative calendar; book plans track chapter progress.

## Learning Materials

| Material | LFCPS archive | Reusable template |
| --- | --- | --- |
| Original reading notes | [Notes](books/LFCPS/notes/README.md) | [Notes template](templates/notes.md) |
| Editable presentations and PDF exports | [Slides](books/LFCPS/slides/README.md) | [Presentation checklist](templates/presentation.md) |
| Code, models and verification instructions | [Demos](books/LFCPS/demos/README.md) | [Demo README](templates/demo.md) |
| Original exercise solutions | [Exercises](books/LFCPS/exercises/README.md) | Use the [notes template](templates/notes.md) with exercise references |
| Discussion and follow-up records | [Sessions](sessions/README.md) | [Session template](templates/session.md) |

## Seminar Workflow

1. Propose a chapter/task through an Issue and agree on the presenter, reviewer and scope.
2. Prepare notes, editable slides and an applicable Demo on a working branch.
3. Open a Pull Request before the seminar; check sources, assumptions and reproducibility.
4. Discuss and demonstrate; record what was actually observed and what remains unresolved.
5. Revise materials and link them from a dated session record after the meeting.

Recommended milestones: **T−7** scope and roles → **T−3** draft materials → **T−1** review → **T** seminar → **T+2** final materials and record. Adjust these intervals by agreement; see [CONTRIBUTING.md](CONTRIBUTING.md).

## How to Contribute

Start with the [contribution guide](CONTRIBUTING.md), then use the [Issue templates](https://github.com/CPS-HCPS-Research/Book-Reading-Seminar/issues/new/choose) and a Pull Request targeting `main`. A first submission may be a clearly scoped draft; disclose unrun or incomplete Demos.

**中文参与指引：** 先查看整体安排与教材计划，认领章节后创建分支。笔记、PPT、Demo和习题分别放入教材目录；保留PPT可编辑源文件，建议附同名PDF。通过PR提交并说明验证状态、引用来源和待讨论问题。研讨结束后再新增真实日期的记录；负责人和时间未确认时写“待指定／待定”。

Run the lightweight checks from the repository root (Python 3.9+):

```sh
python3 scripts/check_repository.py
python3 -m unittest discover -s scripts/tests -v
```

## Useful Resources

- [Verified LFCPS official resources](books/LFCPS/resources.md): publisher, author, chapter directory, course, videos, slides and KeYmaera X.
- [Add another book](CONTRIBUTING.md#adding-a-book) using the [book template](templates/book.md).
- [Repository administration](docs/maintenance.md): branch protection, checks and maintenance.

No repository-wide license has been selected. Original text, code and third-party material have separate rights; public visibility is not permission to redistribute them.
