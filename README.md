# 图书研讨会

**Book Reading Seminar · CPS-HCPS Research**

面向CPS、HCPS及相关基础理论与智能软件研究，持续积累教材研读、原创学习材料、可复现实验和研讨记录。

## 目标与范围

读书会围绕信息物理系统（Cyber-Physical Systems，CPS）、人机物融合系统（Human-Cyber-Physical Systems，HCPS）及相关研究开展教材学习、方法推导和问题讨论。每本教材拥有独立档案，研讨记录按实际日期关联所使用的材料与后续任务。

仓库主要保存原创学习资料和官方资源链接。教材全文、课件及其他第三方材料的公开使用要求见[协作与版权规范](CONTRIBUTING.md)。

## 当前教材

| 教材 | 学习状态 | 常用入口 |
| --- | --- | --- |
| *Logical Foundations of Cyber-Physical Systems* — André Platzer，Springer，2018（LFCPS） | 准备中；负责人及日期待确认 | [教材档案与章节导航](books/LFCPS/README.md) · [章节研读计划](books/LFCPS/schedule.md) |

完整书目与后续教材见[教材目录](CATALOG.md)。“准备中”表示正在筹备，不代表已经完成阅读或开展研讨。

## 研读安排

[整体日程与任务分工](SCHEDULE.md) · [LFCPS建议研读顺序](books/LFCPS/schedule.md) · [研讨记录](sessions/README.md)

目前尚未确认研讨日期和汇报人。整体日程统一维护时间安排，各教材计划维护章节任务与进度。

## 学习材料

| 材料类别 | LFCPS材料入口 | 可复用模板 |
| --- | --- | --- |
| 原创阅读笔记 | [笔记索引](books/LFCPS/notes/README.md) | [阅读笔记模板](templates/notes.md) |
| 可编辑PPT及PDF展示版 | [汇报材料](books/LFCPS/slides/README.md) | [汇报提纲与检查清单](templates/presentation.md) |
| 代码、模型和验证说明 | [实验与演示](books/LFCPS/demos/README.md) | [Demo说明模板](templates/demo.md) |
| 原创习题解答 | [习题索引](books/LFCPS/exercises/README.md) | 使用[笔记模板](templates/notes.md)，补充题号与解答过程 |
| 讨论结论和后续任务 | [研讨记录](sessions/README.md) | [研讨记录模板](templates/session.md) |

## 研讨流程

1. 通过任务单（Issue）提出章节任务，确认范围、汇报人和审阅人。
2. 在工作分支准备笔记、可编辑PPT，以及适用的实验或演示（Demo）。
3. 研讨前发起合并请求（Pull Request，PR），检查来源、假设和可复现性。
4. 开展讨论和技术演示，记录实际观察、讨论结论与未解决问题。
5. 会后修订材料，在真实日期的研讨记录中添加材料链接与后续任务。

建议节奏：**T−7天**确认任务 → **T−3天**提交初稿 → **T−1天**检查材料 → **T日**正式研讨 → **T+2天**整理材料和记录。时间可共同调整，具体要求见[协作规范](CONTRIBUTING.md)。

## 如何参与

先阅读[协作规范](CONTRIBUTING.md)，使用[任务与问题模板](https://github.com/CPS-HCPS-Research/Book-Reading-Seminar/issues/new/choose)明确范围，再通过目标为 `main` 的PR提交材料。首次提交可以是范围明确的草稿，须说明未完成内容和Demo的实际验证状态。

**首次参与：** 查看安排、认领章节、创建分支，再按材料类别归档。PPT保留可编辑源文件，建议附同名PDF。负责人和时间未确认时写“待指定／待定”；研讨结束后再新增真实日期的记录。

完整操作步骤见[使用说明](docs/user-guide.md)，包括首次提交PPT和Demo、PR协作、会后记录及新增教材。正文以中文为主，文件和文件夹名使用英文；教材原名、专业术语及必要的技术标识可保留英文。

在仓库根目录运行检查，需要Python 3.9或更高版本：

```sh
python3 scripts/check_repository.py
python3 -m unittest discover -s scripts/tests -v
```

## 常用资源

- [LFCPS官方资源](books/LFCPS/resources.md)：出版社、作者主页、正式目录、课程、视频、课件索引和KeYmaera X。
- [新增教材流程](CONTRIBUTING.md#新增教材)：使用[教材档案模板](templates/book.md)建立独立档案。
- [仓库维护说明](docs/maintenance.md)：分支保护、质量检查、维护及发布恢复。

仓库尚未设定统一许可证。原创文字、代码和第三方材料分别记录授权情况；公开可见不代表可以自由再分发。
