# Repository Maintenance / 仓库维护

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

## 轻量检查的维护

日常运行：

```sh
python3 scripts/check_repository.py
python3 -m unittest discover -s scripts/tests -v
```

检查器规则见[CONTRIBUTING.md](../CONTRIBUTING.md)。有意修改命名或结构规范时，同一PR同步修改文档、检查器和相关失败案例测试。脚本不执行Demo、不联网下载材料、不扫描历史，也不代替版权和学术审阅。

每轮研读结束：核对索引与记录、跟进未解决Issue、记录版本变化、更新教材状态。保留原始可编辑文件和Git历史；纠错通过普通提交完成。
