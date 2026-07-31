<div align="center">

# 李承阳 <sup><sub>LEECYANG</sub></sup>

<samp>AI INFRA · OPERATOR OPTIMIZATION · EDGE SYSTEMS</samp>

<sub>南京农业大学 · 电子信息工程技术 · 2027 届</sub>

<br><br>

[项目](#03--项目记录)　·　[代码](#04--公开代码)　·　[邮件](mailto:3439550021@qq.com)

</div>

<br>

<table>
  <tr>
    <td align="center" width="25%">
      <sub>全国大学生计算机系统能力大赛</sub><br>
      <strong>全国第 1</strong><br>
      <sub>算子优化赛道</sub>
    </td>
    <td align="center" width="25%">
      <sub>Atlas 200I DK A2</sub><br>
      <strong>15 FPS</strong><br>
      <sub>3× 实时超分</sub>
    </td>
    <td align="center" width="25%">
      <sub>端到端推理</sub><br>
      <strong>&lt; 100 ms</strong><br>
      <sub>CPU / NPU 协同</sub>
    </td>
    <td align="center" width="25%">
      <sub>农业害虫识别</sub><br>
      <strong>50+ 类 / 95%</strong><br>
      <sub>平均响应 &lt; 500 ms</sub>
    </td>
  </tr>
</table>

## `00 / 自述`

我是李承阳，目前在南京农业大学读电子信息工程技术。

过去一年，我把很多时间花在异构计算和 AI 基础设施上。日常工作包括 Ascend / CUDA 算子优化、模型迁移与量化、显存问题排查，以及推理服务和边缘设备上的工程落地。

我对性能问题很有耐心。一次推理慢在哪里、数据经过了哪些内存、CPU 和 NPU 怎样分工，我通常会沿着调用链一直查下去。这个习惯把我带进了算子开发，也让我开始认真学习运行时、体系结构和并行计算。

## `01 / 主线`

<table>
  <tr>
    <td width="24%"><strong>算子与性能</strong></td>
    <td>GEMM、FlashAttention、Winograd；Ascend C、CUDA、Triton；profiling、定位瓶颈、内存访问与并行策略。</td>
  </tr>
  <tr>
    <td><strong>模型系统</strong></td>
    <td>MindSpore、PyTorch、ONNX；模型迁移、微调、量化、显存调度和多模态能力验证。</td>
  </tr>
  <tr>
    <td><strong>AI 基础设施</strong></td>
    <td>模型接口适配、推理服务、多智能体工作流、Docker、Nginx 和高并发服务组织。</td>
  </tr>
  <tr>
    <td><strong>边缘与硬件</strong></td>
    <td>Atlas 200I DK A2、K230、STM32、FPGA；端侧推理、通信协议、时序控制和软硬件协同。</td>
  </tr>
</table>

<details>
<summary><strong>常用语言与工具</strong></summary>
<br>

```text
C++ / Python / Java / TypeScript / Verilog / SystemVerilog
AscendCL / MindSpore / PyTorch / ONNX / OpenCV / DJL
Docker / Nginx / GitHub Actions / MySQL / Redis
```

</details>

## `02 / 竞赛与校园经历`

| 记录 | 结果 |
|:--|:--|
| 全国大学生计算机系统能力大赛「先导杯」 | 算子优化赛道全国第 1 名 |
| 天翼云「息壤杯」高校 AI 大赛 | 算子优化赛道全国第 24 名 |
| 多智能体项目「灵犀智学」 | 项目负责人，入围挑战杯省赛 |
| 南京农业大学 | 电子信息工程技术本科，2023—2027，专业前 40% |

## `03 / 项目记录`

<details open>
<summary><strong>01　Atlas 200I DK A2 实时超分系统</strong>　<sub>核心开发 · 2025.08—2025.10</sub></summary>
<br>

面向昇腾 310B 边缘平台，我设计了一条从 V4L2 采集、CPU/NPU 协同处理到 HDMI 输出的低延迟流水线。

FSRCNN 模型迁移到 MindSpore 后，我使用图模式、数据下沉和 AMP O3 缩短训练时间，再通过 ATC 导出 OM 模型。推理阶段只把 YCrCb 的亮度通道交给 NPU，色度插值由 CPU 并行处理；AscendCL/C++ 负责内存、模型和任务队列管理。

最终结果：3× 超分稳定超过 15 FPS，端到端延迟低于 100 ms，PSNR 超过 30 dB，SSIM 超过 0.9。

`MindSpore`　`AscendCL`　`C++`　`V4L2`　`HDMI`

</details>

<details>
<summary><strong>02　Open WebUI 多智能体平台与推理服务</strong>　<sub>全栈开发 · 2025.07—2025.10</sub></summary>
<br>

我重构了 Open WebUI 的模型接入层，适配九天、阿里云百炼和 Coze 的接口差异，并加入数据库查询、API 调用等 Agent 工作流。服务通过 Docker 和 Nginx 部署到公网，日常维护涵盖模型路由、并发请求与异常恢复。

`Open WebUI`　`Agent`　`Docker`　`Nginx`　`API Integration`

</details>

<details>
<summary><strong>03　K230 视觉识别与激光打靶小车</strong>　<sub>视觉模块 · 2025.06—2025.07</sub></summary>
<br>

我负责数据标注、YOLOv5 训练、INT8 量化和 K230 NPU 部署，同时编写 K230 与 STM32 之间的通信协议。检测结果通过串口送入主控，驱动机械云台完成实时跟踪。主要调试内容集中在端侧资源占用、推理时延、串口时序和控制闭环。

`YOLOv5`　`K230`　`INT8`　`STM32`　`Serial Protocol`

</details>

<details>
<summary><strong>04　大模型微调与多模态部署</strong>　<sub>AI 工程 · 2025.02—2025.05</sub></summary>
<br>

基于 MindSpore 和 MindNLP 完成 DeepSeek-R1-Distill-Qwen-1.5B 的数据处理、环境搭建、微调与验证。针对目标硬件上的显存瓶颈，我重构了训练脚本和显存调度逻辑，解决 OOM 并稳定训练过程。随后完成 Janus-Pro 的源码级适配，处理编译环境和底层依赖，使图像理解与文本生图能力能在本地运行。

`MindSpore`　`MindNLP`　`DeepSeek-R1`　`Janus-Pro`　`Fine-tuning`

</details>

<details>
<summary><strong>05　农业害虫识别平台</strong>　<sub>项目发起人 / 全栈开发 · 2024.10—2024.11</sub></summary>
<br>

我从零搭建了 Vue + Spring Boot 的前后端分离系统，在 Java 服务中通过 DJL 直接运行 ONNX 模型。Redis 用于缓存热点数据，Docker Compose 负责服务编排。系统覆盖 50 余种害虫，识别准确率约 95%，平均接口响应控制在 500 ms 内。

[`leecyang/agrivision-ai ↗`](https://github.com/leecyang/agrivision-ai)

`Vue`　`Spring Boot`　`DJL`　`ONNX`　`Redis`

</details>

## `04 / 公开代码`

<table>
  <tr>
    <td width="31%"><a href="https://github.com/leecyang/mindyolo"><strong>mindyolo ↗</strong></a><br><sub>Python · MindSpore</sub></td>
    <td>基于 MindSpore 的 YOLO 系列工具箱，记录目标检测模型与训练链路相关实践。</td>
  </tr>
  <tr>
    <td><a href="https://github.com/leecyang/agrivision-ai"><strong>agrivision-ai ↗</strong></a><br><sub>Vue · Java · ONNX</sub></td>
    <td>农业害虫识别平台，包含前端、后端、模型推理、缓存和容器化部署。</td>
  </tr>
  <tr>
    <td><a href="https://github.com/leecyang/ChronoCore"><strong>ChronoCore ↗</strong></a><br><sub>Verilog · FPGA</sub></td>
    <td>包含时钟、闹钟、秒表、按键消抖和数码管驱动的数字系统项目。</td>
  </tr>
  <tr>
    <td><a href="https://github.com/leecyang/Washing_Machine_Controller"><strong>Washing Machine Controller ↗</strong></a><br><sub>SystemVerilog</sub></td>
    <td>围绕有限状态机、时序控制和模块验证完成的控制器设计。</td>
  </tr>
  <tr>
    <td><a href="https://github.com/leecyang/PGA-prediction-engineering-education"><strong>PGA prediction ↗</strong></a><br><sub>Python · Machine Learning</sub></td>
    <td>面向工程教育场景的学生表现预测基线系统。</td>
  </tr>
</table>

<br>

<div align="center">

<samp>南京 · 2027 届 · 3439550021@qq.com</samp>

</div>
