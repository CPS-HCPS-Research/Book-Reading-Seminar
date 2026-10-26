# Repository Maintenance / 仓库维护

成员的完整操作流程见[中文使用说明](user-guide.md)；本文件集中记录管理员设置、发布恢复及维护事项。

## 管理员配置

先检查现有设置，只补充缺失项，不覆盖组织已有规则。仓库保持 `CPS-HCPS-Research/Book-Reading-Seminar`，主分支为 `main`，禁止强制推送或删除远程历史。

本次初始化查询：远程为空、默认分支为main、Issue已开启、规则集列表为空；GitHub连接器返回仓库写入/管理权限，但分支保护接口实际返回403 `Resource not accessible by integration`。仓库角色与集成可调用的管理接口权限不同，不能据此声称保护已生效。以下为需要管理员确认并配置的步骤。

1. 打开仓库 **Settings → General**，确认默认分支为`main`。保留Issues；Discussions仅在团队需要时开启，不必启用Pages或Wiki。
2. 打开 **Settings → Actions → General**，确认组织策略允许本仓库工作流以及`actions/checkout`、`actions/setup-python`。工作流只需`contents: read`；不要授予创建/批准PR权限。外部贡献工作流依GitHub设置由维护者审核运行。
3. 在首次工作流成功后，打开 **Settings → Branches → Add classic branch protection rule**，目标填`main`；如组织已经使用Rulesets，应在现有规则中补齐同等约束，避免叠加冲突。
4. 启用 **Require a pull request before merging**，要求至少1个批准；启用新提交使旧批准失效，以及讨论解决后才能合并。
5. 启用 **Require status checks to pass before merging**，选择本仓库实际运行产生的`repository-check`；要求分支保持最新。检查名称须以Actions实际显示为准，不要选择尚不存在的检查把团队锁住。
6. 保持禁止force push和branch deletion；团队确认维护者审阅安排后可使管理员也遵循规则。不要创建虚构的CODEOWNERS账号或审阅团队。
7. 邀请真实成员，按最小必要权限分配Write/Triage/Read；研讨负责人和审阅人确定后，再决定是否设置CODEOWNERS。
8. 如仓库Security设置提供secret scanning和push protection，确认启用状态；不要因此省略提交前人工检查。

保存后用成员的测试PR确认：直接推送受限、至少1位审阅人批准、`repository-check`通过、未解决讨论阻止合并。这里只说明验收方法，不声称已完成这些设置。

官方依据：[GitHub分支保护配置](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule)。组织策略和界面可能变化，按当前可用选项操作。

## 初始化交付与恢复发布（2026-10-26）

本地已完成27个文本文件，初始提交为`a0bb08d40cbc0300ea44ae0a6eff373db8c35b8d`；本节在后续说明提交中追加。目录、相对链接、模板检查通过；检查器的11项测试通过。没有教材/课件副本、学生汇报文件、已运行Demo或虚构研讨记录。验证仅覆盖本地仓库结构与检查器行为，未运行GitHub Actions或KeYmaera X。

本次发布受阻的实际结果：

- HTTPS克隆、查询及推送：连接`github.com:443`超时。
- SSH推送：`Permission denied (publickey)`。
- GitHub连接器创建README：403 `Resource not accessible by integration`，没有成功写入远程。
- 本机执行环境拒绝写入`.git/config`，所以未能保存`origin`；提交成功不表示已建立远程跟踪。
- 分支保护读取：同样返回集成权限403；未修改保护规则。

有正常网络和仓库写权限的维护者可在自己的终端中恢复发布。先检查当前状态和远程，**仅当origin不存在时**执行`remote add`：

```sh
git status --short --branch
git remote -v
git remote add origin https://github.com/CPS-HCPS-Research/Book-Reading-Seminar.git
git ls-remote --heads origin
```

如果远程仍无分支，执行普通推送：

```sh
git push -u origin main
```

如果远程已经新增提交，先抓取并审阅双方历史，保留本地成果，再决定普通合并或PR迁移；不要强推或重建仓库。认证应通过维护者自己的GitHub凭据管理或已授权SSH密钥完成，不把凭据写入文件、URL或Issue。

推送成功后，打开仓库首页确认交付文件可见，文件清单以`git ls-files`为准（初始27个文件，后续增补完整使用说明），检查Actions中的`repository-check`结果，再执行上面的分支保护设置。该确认步骤尚未完成，不应把本地测试结果报告为远程CI通过。

## 轻量检查的维护

日常运行：

```sh
python3 scripts/check_repository.py
python3 -m unittest discover -s scripts/tests -v
```

检查器规则见[CONTRIBUTING.md](../CONTRIBUTING.md)。有意修改命名或结构规范时，同一PR同步修改文档、检查器和相关失败案例测试。脚本不执行Demo、不联网下载材料、不扫描历史，也不代替版权和学术审阅。

每轮研读结束：核对索引与记录、跟进未解决Issue、记录版本变化、更新教材状态。保留原始可编辑文件和Git历史；纠错通过普通提交完成。
