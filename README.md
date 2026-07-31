```text
╭─[●]─[○]─[○]─ leecyang@github:~/profile ─────────────────────────────────────
│
│  ██╗     ███████╗███████╗ ██████╗██╗   ██╗ █████╗ ███╗   ██╗ ██████╗
│  ██║     ██╔════╝██╔════╝██╔════╝╚██╗ ██╔╝██╔══██╗████╗  ██║██╔════╝
│  ██║     █████╗  █████╗  ██║      ╚████╔╝ ███████║██╔██╗ ██║██║  ███╗
│  ██║     ██╔══╝  ██╔══╝  ██║       ╚██╔╝  ██╔══██║██║╚██╗██║██║   ██║
│  ███████╗███████╗███████╗╚██████╗   ██║   ██║  ██║██║ ╚████║╚██████╔╝
│  ╚══════╝╚══════╝╚══════╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝
│
│  李承阳  //  AI INFRA · OPERATOR OPTIMIZATION · EDGE SYSTEMS
│
├─[ SESSION 0x4C4359 ]──────────────────────────────────────────────────────────
│  USER       ◢  leecyang
│  EDUCATION  ◢  南京农业大学 · 电子信息工程技术 · 2027
│  CURRENT    ◆  LingXi-Org / LingxiGraph / LingxiNext
│  LOCATION   ◇  Nanjing, China
│  MODES      [█] learning  [▓] profiling  [▒] shipping
│
╰─❯ boot sequence complete _
```

<div align="center">

[`LingxiGraph`](https://github.com/LingXi-Org/LingxiGraph)　·　[`LingxiNext`](https://github.com/LingXi-Org/LingxiNext)　·　[`source`](https://github.com/leecyang?tab=repositories)　·　[`mail`](mailto:3439550021@qq.com)

</div>

```text
╭─[ HIGHLIGHTS.LOG ]───────────────────────────────────────────────────────────
│
├─◆  01 / RANK     全国第 1       计算机系统能力大赛 · 算子优化赛道
├─■  02 / FPS      15 FPS         Atlas 200I DK A2 · 3× 实时超分
├─▰  03 / LATENCY  < 100 ms       端到端推理 · CPU / NPU 协同
└─◇  04 / VISION   50+ 类 / 95%   农业害虫识别 · 平均响应 < 500 ms
│
╰─[ EOF ]── 4 records loaded ──────────────────────────────────────────────────
```

## `┌─[00 / IDENTITY]` `$ whoami --verbose`

我是李承阳，目前在南京农业大学读电子信息工程技术。

过去一年，我把很多时间花在异构计算和 AI 基础设施上。日常工作包括 Ascend / CUDA 算子优化、模型迁移与量化、显存问题排查，以及推理服务和边缘设备上的工程落地。

我对性能问题很有耐心。一次推理慢在哪里、数据经过了哪些内存、CPU 和 NPU 怎样分工，我通常会沿着调用链一直查下去。这个习惯把我带进了算子开发，也让我开始认真学习运行时、体系结构和并行计算。

## `├─[01 / FOCUS]` `$ cat /etc/focus.conf`

```ini
[operator_and_performance]
topics = GEMM, FlashAttention, Winograd, profiling
tooling = Ascend C, CUDA, Triton

[model_systems]
frameworks = MindSpore, PyTorch, ONNX
work = migration, fine-tuning, quantization, memory scheduling

[ai_infrastructure]
work = graph runtime, model adapters, inference services, multi-agent workflows
infra = PostgreSQL, Redis, Docker, Nginx, OpenTelemetry

[edge_and_hardware]
platforms = Atlas 200I DK A2, K230, STM32, FPGA
work = on-device inference, protocols, timing control, hardware-software co-design
```

<details>
<summary><code>╰─❯ printenv TOOLBOX</code></summary>
<br>

```text
C++ / Python / Java / TypeScript / Verilog / SystemVerilog
AscendCL / MindSpore / PyTorch / ONNX / OpenCV / DJL
FastAPI / PostgreSQL / Redis / Docker / Nginx / GitHub Actions
```

</details>

## `├─[02 / LINGXI]` `$ systemctl --user status lingxi.target`

```console
● lingxi.target — open-source multi-agent infrastructure
│
├─▣ Loaded    LingXi-Org
├─◉ Active    active (under development)
├─◆ Core      LingxiGraph.service
├─◇ App       LingxiNext.service
└─⌁ Docs      https://docs.lingxilearn.cn
```

我创建了 [`LingXi-Org`](https://github.com/LingXi-Org)，目前把主要开发精力放在下面两个项目。一个处理运行时和耐久执行，另一个负责具体的多智能体编排与交互界面。

<details open>
<summary><code>● ACTIVE :: LingXi-Org/LingxiGraph · v2.0.1</code></summary>
<br>

[`LingxiGraph`](https://github.com/LingXi-Org/LingxiGraph) 是一个模型供应商中立的耐久多智能体图运行时。它把普通 Python 函数组装成状态图，并提供持久化、失败恢复、流式事件和人工中断。

```text
runtime      Pregel-style plan → execute → commit
durability   typed checkpoint / pending writes / replay / fork
patterns     supervisor / handoff / swarm / plan-execute / map-reduce
control      PostgreSQL lease queue / idempotency / budget / redrive
protocols    REST / resumable SSE / Python SDK / A2A / MCP
safety       OIDC / RBAC / tenant isolation / PostgreSQL RLS / audit
delivery     Docker Compose / Helm / OpenTelemetry / SBOM
```

核心运行时位于 [`graph/executor.py`](https://github.com/LingXi-Org/LingxiGraph/blob/main/src/lingxigraph/graph/executor.py)。并行节点按编译计划执行，状态更新在超步边界确定性归并；异步 checkpoint writer 保证写入顺序。服务端 Worker 采用租约领取任务，带心跳、重试、取消和 dead-letter/redrive 处理。

`Python 3.11+`　`FastAPI`　`PostgreSQL`　`Redis`　`OpenTelemetry`　`MIT`

</details>

<details open>
<summary><code>● ACTIVE :: LingXi-Org/LingxiNext</code></summary>
<br>

[`LingxiNext`](https://github.com/LingXi-Org/LingxiNext) 是基于 LingxiGraph 与原生 Chainlit 的版本化多智能体编排平台。FastAPI、Chainlit、管理后台和图运行时放在同一进程中，PostgreSQL 保存会话、revision 和 checkpoint。

```text
revision     草稿发布后不可变；历史会话固定到原 revision
templates    topic_auction / supervisor / handoff / parallel_review / plan_execute
validation   节点角色 / 允许边 / 必需拓扑 / 循环 / 可达性 / 运行上限
secrets      Fernet 加密 / 掩码返回 / 不进入图状态
web          native Chainlit / Jinja2 admin / SVG graph canvas
runtime      embedded LingxiGraph / PostgreSQL checkpoint
```

[`graph_templates.py`](https://github.com/LingXi-Org/LingxiNext/blob/main/app/graph_templates.py) 负责模板约束、拓扑校验和 revision 编译。管理员只能从受约束模板构图，无法上传 Python 或任意 callable；身份验证、Argon2 密码、CSRF 和 Token 加密集中在 [`security.py`](https://github.com/LingXi-Org/LingxiNext/blob/main/app/security.py)。

`Python`　`JavaScript`　`Chainlit`　`FastAPI`　`PostgreSQL`　`Docker`

</details>

## `├─[03 / PROJECTS]` `$ find ~/projects -maxdepth 1 -type d`

<details open>
<summary><code>◆ PROJECT :: ./WegoLibrary</code>　<sub>FastAPI · React · SQLite</sub></summary>
<br>

[`WegoLibrary`](https://github.com/leecyang/WegoLibrary) 是一个多用户、自托管的到馆与签到助手。仓库包含授权链接解析、微信会话交换、GraphQL 请求、定时任务、用户隔离和 Docker Compose 部署。

协议侧需要处理 HTTP/HTTPS 混合入口、重复 Cookie、短期授权码、TLS EOF 和上游限流。[`traceint_client.py`](https://github.com/leecyang/WegoLibrary/blob/main/backend/app/traceint_client.py) 为这些情况加入双会话换票、重试退避、最小查询校验和明确的错误分类。

</details>

<details>
<summary><code>◆ LIBRARY :: ./NJAU-Auth</code>　<sub>Python · HTTPX · CAS</sub></summary>
<br>

[`NJAU-Auth`](https://github.com/leecyang/NJAU-Auth) 用纯 HTTP 完成南京农业大学统一身份认证，不依赖浏览器自动化。登录流程会提取 `execution` 与动态盐，按 CAS 页面规则生成 AES-128-CBC 密文，并处理图形验证码、短信二次验证与 Cookie 恢复。

仓库已经整理成可安装的 Python 包，提供异步 API、CLI 和基于 `httpx.MockTransport` 的协议测试。

</details>

<details>
<summary><code>◇ WORKER :: ./memos2bark</code>　<sub>TypeScript · Cloudflare Workers · KV</sub></summary>
<br>

[`memos2bark`](https://github.com/leecyang/memos2bark) 把 Memos 动态转发到 Bark。Worker 支持自助注册 webhook、多用户配置、多个 Bark 端点、事件归一化和五分钟去重；Memos Token 只参与注册，不写入 KV。

项目保持单 Worker 结构，包含类型检查、测试和 Cloudflare 一键部署配置。

</details>

<details>
<summary><code>◇ RTL :: ./ChronoCore</code>　<sub>Verilog · Cyclone IV · ModelSim</sub></summary>
<br>

[`ChronoCore`](https://github.com/leecyang/ChronoCore) 是一个模块化 FPGA 数字时钟。顶层连接时钟分频、按键消抖、模式 FSM、时间计数、闹钟、秒表和六位数码管扫描，并附带测试平台与 Quartus 工程文件。

这个仓库保留了我在数字逻辑、跨模块信号组织和时序控制上的早期实践。

</details>

<details>
<summary><code>◇ PROJECT :: ./agrivision-ai</code>　<sub>Vue · Spring Boot · DJL · ONNX</sub></summary>
<br>

[`agrivision-ai`](https://github.com/leecyang/agrivision-ai) 是一个农业害虫识别课程项目。仓库覆盖 Vue 前端、Spring Boot API、MySQL 数据层、DJL/ONNX 推理入口和 Docker Compose，用来练习模型能力与 Java Web 服务的整合。

</details>

## `├─[04 / SOURCE]` `$ grep -R "worth_reading" ~/src`

下面这些文件更能说明我的代码取向。链接直接落到实现，不按仓库热度排序。

| path | why it is here |
|:--|:--|
| [`LingxiGraph/graph/executor.py`](https://github.com/LingXi-Org/LingxiGraph/blob/main/src/lingxigraph/graph/executor.py) | Pregel 超步执行、并行任务归并、checkpoint、interrupt、budget 和 cancellation 集中在同一个不可变编译图模型中。 |
| [`LingxiGraph/server/worker.py`](https://github.com/LingXi-Org/LingxiGraph/blob/main/src/lingxigraph/server/worker.py) | 租约式分布式 Worker，包含心跳、优雅 drain、失败分类、重试与暂停恢复。 |
| [`LingxiNext/graph_templates.py`](https://github.com/LingXi-Org/LingxiNext/blob/main/app/graph_templates.py) | 五类多智能体拓扑的服务端校验与编译，约束角色、边、循环、入口可达性和运行上限。 |
| [`NJAU-Auth/auth_client.py`](https://github.com/leecyang/NJAU-Auth/blob/main/src/njau_auth/auth_client.py) | 纯 HTTP CAS 状态机，覆盖动态盐加密、验证码重试、短信 re-auth、Cookie 导入导出和明确异常类型。 |
| [`WegoLibrary/traceint_client.py`](https://github.com/leecyang/WegoLibrary/blob/main/backend/app/traceint_client.py) | 对不稳定第三方协议的防御式封装：双会话、换票校验、TLS/连接错误重试和响应降级解析。 |
| [`memos2bark/src/index.ts`](https://github.com/leecyang/memos2bark/blob/main/src/index.ts) | 在单个 Cloudflare Worker 中完成 webhook 注册、鉴权、KV 配置、事件去重与并发推送。 |
| [`ChronoCore/digital_clock_top.v`](https://github.com/leecyang/ChronoCore/blob/main/digital_clock_top.v) | 顶层 RTL 集成，连接分频、消抖、FSM、计时和显示模块，适合从硬件边界观察模块划分。 |

## `└─[05 / RECORDS]` `$ cat ~/records/competitions.log`

```text
◆ [rank 01] 全国大学生计算机系统能力大赛「先导杯」 / 算子优化赛道全国第 1 名
◇ [rank 24] 天翼云「息壤杯」高校 AI 大赛 / 算子优化赛道全国第 24 名
▣ [project] 多智能体项目「灵犀智学」 / 项目负责人 / 入围挑战杯省赛
⌁ [degree ] 南京农业大学 / 电子信息工程技术 / 2023—2027 / 专业前 40%
```

```console
╭─[●]─[○]─[○]─ END OF BUFFER ────────────────────────────────────────────────╮
│                                                                            │
│  ╭─[leecyang@github]─[~/profile]                                           │
│  ╰─❯ contact --mail 3439550021@qq.com                                      │
│                                                                            │
│  ▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰  connection ready              │
│                                                                            │
╰─[ process exited with code 0 ]──────────────────────────────────────────────╯
```
