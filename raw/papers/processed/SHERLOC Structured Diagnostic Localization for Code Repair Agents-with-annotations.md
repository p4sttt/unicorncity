2026-6-24
| SHERLOC: |        |     | Structured |        |     | Diagnostic |     |     | Localization |     |     | for |     |
| -------- | ------ | --- | ---------- | ------ | --- | ---------- | --- | --- | ------------ | --- | --- | --- | --- |
| Code     | Repair |     |            | Agents |     |            |     |     |              |     |     |     |     |
Hovhannes Tamoyan1,2, Sean Narenthiran1, Erik Arakelyan1, Mira Mezini2,3 and Boris Ginsburg1
1NVIDIA,SantaClara,CA95051,USA,2TUDarmstadt,Darmstadt,Germany,3hessian.AI&NationalResearchCenter
forAppliedCybersecurityATHENE
LLM agents solve repository-level coding tasks through multi-turn tool use, but utilize half their budget on
locating faults before editing. Dedicated localization frameworks have emerged, yet are still evaluated as file
retrieval rather than actionable diagnosis, producing locations without the diagnostic context a repair agent
needs. We introduce SHERLOC (Structured Hypothesis-driven Exploration and Reasoning for Localization),
a training-free framework pairing a reasoning LLM with compact repository tools and self-recovery, without
6202 nuJ 32  ]LC.sc[  1v02842.6062:viXra fine-tuning or multi-agent orchestration. SHERLOC reaches state-of-the-art localization across model
scales: 84.33% accuracy@1 on SWE-Bench Lite and 81.27% recall@1 on SWE-Bench Verified; at
∼30B parameters, it matches or outperforms other agentic methods. Injecting our locations and diagnostic
findings into repair agents yields, on average, +5.95 pp resolve rate on SWE-Bench Verified while cutting
| localization | and | total | tokens | by 36.7% | and | 23.1%. |     |     |     |     |     |     |     |
| ------------ | --- | ----- | ------ | -------- | --- | ------ | --- | --- | --- | --- | --- | --- | --- |
1. Introduction
|     |     |     |     |     |     |     | SHERLOC |     | Tool Executor |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------- | --- | ------------- | --- | --- | --- | --- |
Repository-level code repair increasingly relies on       File System
LLM agents that interleave extended reasoning with LLM-friendly Tools
     django/
|     |     |     |     |     |     |     | Self-Recovery |     | ◓ View File | ⌥ Repository Tree |     |           a p p | s / |
| --- | --- | --- | --- | --- | --- | --- | ------------- | --- | ----------- | ----------------- | --- | --------------- | --- |
structured tool calls over a codebase [Wei et al., 2022,           co r e /
|     |     |     |     |     |     |     |     |     |     |     |     |           _ _ in | it _ _ . p y |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---------------- | ------------ |
Yao et al., 2022, Schick et al., 2023]. A canoni- Reasoning LLM ◉ Search String ⁂ Import Tree
|     |     |     |     |     |     |     |     |     |     |     |     |           _ _ m | a i n _ _ . py |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --------------- | -------------- |
cal benchmark for evaluating these agents is SWE-      scripts/
|            |          |            |             |           |           |        |     |     | Tool Execution Output |     |     |      extras/ |     |
| ---------- | -------- | ---------- | ----------- | --------- | --------- | ------ | --- | --- | --------------------- | --- | --- | ------------ | --- |
| Bench      | [Jimenez | et         | al., 2024], | built     | from      | GitHub |     |     |                       |     |     |              |     |
| issues and | their    | resolving  | pull        | requests: | from      | a bug  |     |     |                       |     |     |              |     |
| report and | a        | repository | snapshot,   |           | the agent | must   |     |     |                       |     |     |              |     |
propose and verify a bug-fixing code patch. Yet how Figure 1: SHERLOC. A reasoning
|                 |     |       |             |        |        |      |               | Overview |      | of              |      |      |     |
| --------------- | --- | ----- | ----------- | ------ | ------ | ---- | ------------- | -------- | ---- | --------------- | ---- | ---- | --- |
| agents allocate |     | their | interaction | budget | within | this |               |          |      |                 |      |      |     |
|                 |     |       |             |        |        |      | LLM interacts |          | with | a tool executor | over | four |     |
repair loop remains underexplored. In a systematic LLM-friendly tools, with a self-recovery layer
study spanning 5 LLMs and 2 agent frameworks, we correcting failures. SHERLOC achieves
find that agents spend on average 18.5 turns (48% state-of-the-art file-level localization on
of total interaction) locating faults before their first SWE-Bench Lite and Verified, and in
| patch, consuming |     | over | 320k | tokens per | instance | (Sec- |            |      |        |         |             |      |     |
| ---------------- | --- | ---- | ---- | ---------- | -------- | ----- | ---------- | ---- | ------ | ------- | ----------- | ---- | --- |
|                  |     |      |      |            |          |       | downstream | code | repair | yields, | on average, | 5.95 | pp  |
tion L). This makes localization both a performance higher resolve rate with 36.7% and 23.1% fewer
bottleneck and a dominant compute cost, consuming localization and total tokens.
| context | and interaction |               | budget | that | could | otherwise |             |             |     |                |     |                |     |
| ------- | --------------- | ------------- | ------ | ---- | ----- | --------- | ----------- | ----------- | --- | -------------- | --- | -------------- | --- |
| support | patch           | construction. |        |      |       |           |             |             |     |                |     |                |     |
|         |                 |               |        |      |       |           | ers without | fine-tuning |     | or multi-agent |     | orchestration? |     |
Most localization methods retrieve faulty files and When do its locations and findings transfer
(RQ2)
| functions      | [Zhou | et al., | 2012,     | Reddy      | et al., | 2025, Yu   |                |      |         |         |      |             |      |
| -------------- | ----- | ------- | --------- | ---------- | ------- | ---------- | -------------- | ---- | ------- | ------- | ---- | ----------- | ---- |
|                |       |         |           |            |         |            | to code-repair |      | agents, | and how | does | the resolve | rate |
| et al., 2025]; | some  | (e.g.,  | OrcaLoca, | SWE-Debate |         | [Li        |                |      |         |         |      |             |      |
|                |       |         |           |            |         |            | and token      | cost | shift?  |         |      |             |      |
| et al., 2025]) | also  | produce | free-form | report     |         | text. This |                |      |         |         |      |             |      |
view is necessary but incomplete: a file path tells the We introduce SHERLOC (Structured Hypothesis-
agent where to look, but not why, and a file path Localization),
|     |     |     |     |     |     |     | driven Exploration |     | and | Reasoning | for |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------ | --- | --- | --------- | --- | --- | --- |
without a root-cause hypothesis leaves downstream a training-free framework coupling a reasoning LLM
repair under-specified. We hypothesize that explic- with a compact suite of LLM-friendly repository
|                |     |           |            |            |     |        | tools (file | viewing, |     | code search, | repository-tree |     | in- |
| -------------- | --- | --------- | ---------- | ---------- | --- | ------ | ----------- | -------- | --- | ------------ | --------------- | --- | --- |
| itly producing |     | candidate | locations, | root-cause |     | analy- |             |          |     |              |                 |     |     |
sis, and actionable solution guidance yields a richer, spection, and import-graph navigation; Figure 1) and
more transferable localization, and ask: Can lightweight self-recovery mechanisms (context trunca-
(RQ1)
a single reasoning LLM with a compact, structured tion, loop detection, malformed-tool-call repair, final-
tool interface match task-specifically trained localiz- turn synthesis). For each predicted location, SHER-
|     |     |     |     |     |     |     | LOC emits | a   | structured | diagnostic | finding. |     |     |
| --- | --- | --- | --- | --- | --- | --- | --------- | --- | ---------- | ---------- | -------- | --- | --- |
© 2026NVIDIA.Allrightsreserved.

SHERLOC:StructuredDiagnosticLocalizationforCodeRepairAgents
| SWE-Bench Lite |     |     |     |     |     | SWE-Bench Verified |     |     |     |     |     |     |
| -------------- | --- | --- | --- | --- | --- | ------------------ | --- | --- | --- | --- | --- | --- |
SHERLOC: Qwen3-235B 84.33±0.72 SHERLOC: Qwen3-235B 81.27±1.16
OrcaLoca: Claude 3.5 Sonnet 83.33 SHERLOC: DeepSeek-V3 (671B) 79.53±0.47
SWERank: CodeRankEmbed + Qwen2.5-32B 83.21 SHERLOC: Qwen3-30B 75.07±1.24
SWE-Debate: DeepSeek-V3 (671B) 81.67 SHERLOC: DeepSeek-R1 (671B) 73.63±1.59
| SHERLOC: DeepSeek-V3 (671B) |     |     |     | 79.67±2.03 |     |                             |     |     |     |       |     |     |
| --------------------------- | --- | --- | --- | ---------- | --- | --------------------------- | --- | --- | --- | ----- | --- | --- |
|                             |     |     |     |            |     | RepoSearcher: ToolTrain-32B |     |     |     | 68.03 |     |     |
Agentless: Claude 3.5 Sonnet 78.67 Agentless: Claude 3.7 Sonnet 66.84
| SHERLOC: Qwen3-30B          |     |     |                           | 76.33±2.00 |       | Agentless: GPT-4o      |     |     | 62.28 |     |     |     |
| --------------------------- | --- | --- | ------------------------- | ---------- | ----- | ---------------------- | --- | --- | ----- | --- | --- | --- |
| SHERLOC: DeepSeek-R1 (671B) |     |     |                           | 75.78±1.35 |       |                        |     |     |       |     |     |     |
|                             |     |     |                           |            |       | RepoSearcher: Qwen-32B |     |     | 58.79 |     |     |     |
|                             |     |     | 55                        | 65         | 75 85 |                        |     |     |       |     |     |     |
|                             |     |     |                           |            |       | Agentless: Qwen-32B    |     |     | 58.56 |     |     |     |
|                             |     |     | File-level Accuracy@1 (%) |            |       | OrcaLoca: Qwen-32B     |     |     |       |     |     |     |
56.78
|     |     |     |     |     |     |     |     | 50  |     | 60  | 70 80 |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- |
File-level Recall@1 (%)
Figure 2: Localization performance across benchmarks. Left: file-level accuracy@1 on SWE-Bench
Lite; right: file-level recall@1 on SWE-Bench Verified. Labels use compact model names for readability;
scores and uncertainty values match the original table. SHERLOC results are means over 3 seeds (± std);
prior systems report single runs. Backbone sizes differ across systems; Section 4.4 provides a controlled
| cross-model | analysis. |     |     |     |     |     |     |     |     |     |     |     |
| ----------- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
For (RQ1), we evaluate SHERLOC across model tion context. Alongside candidate locations,
families on SWE-Bench Lite and SWE-Bench SHERLOC produces structured findings with
Verified. It reaches state-of-the-art file-level local- 5 fields (location explanation, root cause, solu-
ization on both benchmarks and remains competi- tion idea, dependencies, testing impact) for each
tive at a matched ∼ 30B scale, without supervised predicted location.
fine-tuning, reinforcementlearning, or multi-agentde- • A structure-agnostic localization metric.
bate. Ablationsshowthatthetoolsuite,self-recovery We propose chunk-level metrics over (start, end)
mechanisms,andreasoningmodeallcontribute,while line-numberspans(coveragerecall,precision,and
implicit-knowledge controls show that the gains per- average tightness) as a structure-agnostic alter-
sist when file paths in the issue are masked. native to function-, class-, or module-level evalu-
|     |     |     |     |     |     | ation, | since | not | every patch | target | sits within | a   |
| --- | --- | --- | --- | --- | --- | ------ | ----- | --- | ----------- | ------ | ----------- | --- |
Stronglocalizationdoesnotautomaticallytranslate
|                                          |               |            |             |        |               | syntactic      |         | unit.    |           |                    |          |       |
| ---------------------------------------- | ------------- | ---------- | ----------- | ------ | ------------- | -------------- | ------- | -------- | --------- | ------------------ | -------- | ----- |
| tobetterrepository-levelissueresolution. |               |            |             |        | For(RQ2),     |                |         |          |           |                    |          |       |
|                                          |               |            |             |        |               | • Cross-family |         |          | transfer  | with               | validity | con-  |
| we inject                                | our locations | and        | findings    | into   | two code-     |                |         |          |           |                    |          |       |
|                                          |               |            |             |        |               |                | SHERLOC |          | transfers | across             | model    | fami- |
| repair frameworks                        |               | (OpenHands | [Wang       |        | et al., 2025] | trols.         |         |          |           |                    |          |       |
|                                          |               |            |             |        |               | lies           | (79.53% | recall@1 | with      | DeepSeek-V3-0324); |          |       |
| and SWE-Agent                            |               | [Yang et   | al., 2024]) | across | 5 repair-     |                |         |          |           |                    |          |       |
implicit-knowledgecontrolsshowitsgainspersist
agentbackbones,yieldingonaverage+5.95ppresolve
whenissuepathsaremasked(79.96%vs.81.27%),
ratewith36.7%and23.1%fewerlocalizationandtotal
|               |     |                    |     |        |     | isolating |     | active      | exploration | from | parametric    | fa- |
| ------------- | --- | ------------------ | --- | ------ | --- | --------- | --- | ----------- | ----------- | ---- | ------------- | --- |
| tokens across | the | 10 model-framework |     | pairs. |     |           |     |             |             |      |               |     |
|               |     |                    |     |        |     | miliarity |     | with public | SWE-Bench   |      | repositories. |     |
All agents benefit on both axes (Figures 3 and 4), • Dual-axis transfer to downstream code
but the best intervention depends on agent capabil- repair. Injecting SHERLOC’s findings into
ity: smaller and mid-sized models gain most from all existing code-repair agents yields, on average,
findings, while stronger localizers benefit primarily +5.95 pp resolve rate, with 36.7% and 23.1% re-
from quality filtering. Thus, transfer is positive but ductions in localization and total tokens across
quality-mediated. five repair backbones and two frameworks; a
|                    |               |                |           |       |           | judge-based |          | quality | filter     | preserves | gains     | on reli- |
| ------------------ | ------------- | -------------- | --------- | ----- | --------- | ----------- | -------- | ------- | ---------- | --------- | --------- | -------- |
| Our main           | contributions |                | are:      |       |           |             |          |         |            |           |           |          |
|                    |               |                |           |       |           | able        | findings | while   | preventing | negative  | transfer. |          |
| • A training-free, |               | tool-augmented |           |       | localiza- |             |          |         |            |           |           |          |
|                    |               |                | SHERLOC   | pairs | a single  | 2. Related  |          | Work    |            |           |           |          |
| tion               | framework.    |                |           |       |           |             |          |         |            |           |           |          |
| reasoning          | LLM           | with           | a compact | suite | of LLM-   |             |          |         |            |           |           |          |
friendly repository tools and lightweight self- Tool-augmented LLM reasoning. SHERLOC
recovery, without task-specific training or multi- builds on reasoning-augmented tool use [Wei et al.,
agent orchestration, and reaches state-of-the- 2022, Yao et al., 2022, Schick et al., 2023] and on
art file-level localization on SWE-Bench Lite test-time scaling that adapts reasoning compute to
(84.33% accuracy@1) and SWE-Bench Veri- problem difficulty [Wu et al., 2025, Zhao et al., 2025].
fied (81.27% recall@1). Unlike prior localization systems built on supervised
| •          |     |          |               |     |           | fine-tuning, | reinforcement |     |     | learning, | or multi-agent |     |
| ---------- | --- | -------- | ------------- | --- | --------- | ------------ | ------------- | --- | --- | --------- | -------------- | --- |
| Diagnostic |     | findings | as structured |     | localiza- |              |               |     |     |           |                |     |
2

SHERLOC:StructuredDiagnosticLocalizationforCodeRepairAgents
Qwen3-30B / SA
Qwen3-30B / OH
Coder-Next / SA
Coder-Next / OH
Next-80B / SA
Next-80B / OH
MiniMax / SA
MiniMax / OH
Qwen3-480B / SA
Qwen3-480B / OH
Baseline Shuffl
Al
e
l
d SHER
Q
LO
F
C SHERLOC Oracle
Intervention
krowemarf
/
ledom
riapeR
44.7 40.2 54.0 52.2 76.0
3.5k
49.4 40.2 53.0 52.4 73.4
2k
45.2 43.2 53.2 52.0 64.6
1k
44.6 39.2 53.2 54.6 68.4
0.5k
38.8 33.8 49.4 50.6 71.0
0.25k
38.6 39.2 50.4 47.8 68.4
74.4 61.0 70.4 76.6 89.2 0
72.2 64.0 67.2 72.8 87.8 Qwen3-3 Q 0 w B e / n S 3 A -30 C B o d / e O r- H Ne C x o t d / e S r- A Next N / e O xt H -80B N e / x S t A -80B M / O in H iMax M / i S n A iM Qw ax e n / 3 O - H 4 Q 8 w 0 e B n / 3 S -4 A 80B / OH
63.0 58.6 63.0 64.0 86.2
61.6 57.8 62.6 62.8 82.6
Figure 3: Downstream resolve rates of LLM
repair agents on SWE-Bench Verified. Each
cell reports resolve rate; within each row, deployable
interventions are shaded blue from light (worst) to
dark (best). In row labels, SA denotes SWE-Agent
and OH denotes OpenHands. Oracle GPT-5.2 (light
gray) is an upper reference, not a deployable
intervention. Full numbers in Table 11.
orchestration, ours uses a single LLM with a fixed,
structured tool set.
LLM-based code localization. Recent LLM-
based methods explore repositories interactively or
reason over code graphs: SWE-Debate adjudicates
fault-propagation traces through multi-agent de-
bate [Li et al., 2025]; OrcaLoca uses priority-based
action scheduling and distance-aware context prun-
ing[Yuetal.,2025]; CoSILandLocAgentguideLLM
search through code-graph structure [Jiang et al.,
2025, Chen et al., 2025]; RepoSearcher/ToolTrain
uses tool-integrated reinforcement learning [Ma et al.,
2025]. SHERLOC differs in design: no training, no
auxiliary structures, a compact set of LLM-friendly
repository actions, and self-recovery mechanisms that
stabilize extended-thinking tool use. Whereas prior
work typically targets file- or function-level entity
locations, sometimes with prescriptive modification
plans for downstream patching [Li et al., 2025], our
method additionally produces structured diagnostic
findings alongside each location.
Issue-based retrieval and ranking. Information-
retrieval bug localization treats the bug report as
a query and source files as documents. BugLoca-
snekoT
Baseline — localization SHERLOC — localization
Baseline — rest of run SHERLOC — rest of run
-34% -37%
-31%
-35% -9% -31%
-66%
-35% -61% -26%
Figure 4: Search-efficiency gains from
SHERLOC findings. Localization-phase (hatched)
and full-run (solid) per-instance token costs: baseline
(blue) vs. SHERLOC (green); the delta above each
pair is the localization-token change relative to
baseline. In x-axis labels, SA denotes SWE-Agent
and OH denotes OpenHands. The largest reductions
in localization-token usage occur with bigger models,
even when their resolve rates are already saturated.
Full numbers in Appendix L.
tor [Zhou et al., 2012] ranks files using textual sim-
ilarity and prior bug reports; BLUiR [Saha et al.,
2013] incorporates structured source-code informa-
tion; AmaLgam [Wang and Lo, 2014] combines ver-
sion history, similar reports, and structure. Recent
neural rankers such as SWERank learn issue–code
similarity with task-specific training [Reddy et al.,
2025]. These methods output ranked locations rather
than diagnostic reports; SHERLOC instead frames
localization as active repository reasoning yielding
structured findings.
Fault localization with execution signals. Clas-
sical fault localization assumes access to executable
tests or dynamic traces: spectrum-based methods
rank by suspiciousness from coverage and pass/fail
statistics [Jones et al., 2002, Abreu et al., 2007];
mutation-basedmethodsinjectsyntheticfaultsand
observe test-outcome changes [Moon et al., 2014, Pa-
padakis and Le Traon, 2015]; learning-based exten-
sions train neural models over coverage or graph fea-
tures [Li et al., 2019, Lou et al., 2021]; AutoFL uses
LLM tool calls but still requires at least one fail-
ing test [Kang et al., 2024]. Unlike these execution-
dependent methods, SHERLOC operates from the
issue description and repository snapshot alone, with-
out executing tests or observing coverage.
Localization granularity. Existing localization
studies report at module, file, class, or function
3

SHERLOC:StructuredDiagnosticLocalizationforCodeRepairAgents
level [Kang et al., 2024, Yu et al., 2025, Chen et al.,
instance id: django__django-12858, repo: django/django, commit: f2051eb8
2025]. For repository-level repair, this granularity is Problem description: models.E015 is raised when ordering uses lookups that are not transforms. ./manage.py
check: SystemCheckError: System check identified some issues: ERRORS: app.Stock: (models.E015) 'ordering' refers
not always aligned with the target edit: patches may to the nonexistent field, related field, or lookup 'supply__product__parent__isnull'. However this ordering works
modifyclass-leveldeclarations,imports,configuration fine: >>> list(Stock.objects.order_by('supply__product__parent__isnull').values_list('pk', flat=True)[:5])
logic, or coordinated regions across functions. We
SHERLOC
thereforecomplementfile-levelmetricswithstructure-
agnosticchunk-levelmetricsoverlineranges(coverage
file path: django/db/models/base.py, start line: 1750, end line: 1751
recall, precision, and average tightness) that repre-
Location explanation: The system check for model ordering incorrectly flags ... ignores lookups via get_lookup().

sent predictions and ground truth as (start, end) line- Root cause: In django/db/models/base.py, _check_ordering() fails to recognize that ... in ordering definitions.

Solution idea: Modify the error condition to check both get_transform() ... for the final path segment.

number spans, making no assumption about which
Dependencies: This is standalone in the model system check logic; query execution itself already works correctly.

syntactic unit contains the patch target. Testing impact: Add/update tests in tests/model_checks/ to verify lookups like isnull in ... trigger E015 errors.
Figure 5: Example SHERLOC input and
output. Given a SWE-Bench Verified Django
Issue-resolution agents and benchmark valid-
issue, SHERLOC predicts a line span in
ity. Issue-resolution systems target patch correct-
ness directly: Agentless [Xia et al., 2024] and Au- django/db/models/base.py and emits a structured
diagnostic finding with the location explanation, root
toCodeRover [Zhang et al., 2024] decompose the task
cause, solution idea, dependencies, and testing
into localization, patch generation, and validation;
impact.
agentic systems such as SWE-Agent and OpenHands
integrate navigation, editing, and execution in a sin-
gle loop [Yang et al., 2024, Wang et al., 2025]. We
observations such as snippets, paths, line ranges, and
instead evaluate localization directly and, in separate
dependency summaries. This keeps repository explo-
experiments, inject our findings into existing repair
ration legible while preserving a deterministic exe-
agents to test downstream transfer. Because high file-
cution boundary: the model chooses the action, but
identification accuracy on SWE-Bench can partly
theexecutorvalidatesandrunsit,avoidingincidental
reflect pretraining familiarity [Liang et al., 2025], we
command construction or shell-debug failure modes
apply implicit-knowledge, shuffled, and masked con-
that prior work has shown to derail agent trajectories
trols to separate benchmark-specific signal from tool-
under raw shell access [Yang et al., 2024]. It also lets
assisted diagnostic reasoning.
ususereasoningmodels, whichexcelatmulti-stepde-
liberation but are not necessarily trained for external
tool APIs, without task-specific tool-use fine-tuning.
3. Method
We formulate localization as an iterative, tool- 3.1. Initialization and Context
mediated reasoning problem: given a natural-
Before prompting, we construct a filtered repository
language issue report and a repository snapshot, the
view that removes directories unlikely to contain pro-
system must identify code regions likely to require
duction logic, such as documentation, build artifacts,
modification and produce a diagnostic finding, not
dependency folders, and version-control metadata
merely a ranked location, that explains the suspected
root cause and solution direction. SHERLOC im-
(e.g., /docs, /.git). The initial prompt combines
this filtered tree with the issue description, tool de-
plements this with four components (Figure 1): a
scriptions, and required output format, giving the
reasoning LLM, a deterministic executor mediating
model a global map of the project without loading
repository access, a compact suite of LLM-friendly
source files.
tools, and lightweight self-recovery. The model al-
ternates between reasoning and structured actions
until it has enough evidence to emit final findings
3.2. Tool Suite
andlocations. Itshypothesisstateistheaccumulated
conversation history, including prior observations; no The suite is limited by design: enough to expose
external memory store is maintained. relevant repository evidence, but not so broad as
to invite open-ended software-engineering actions.
View File inspects a file, optionally restricted to
Design principle: reasoning-native tool use. a line range, with fuzzy path matching that sug-
Rather than synthesizing arbitrary shell commands gests corrections for near-miss names. Codebase
or Python scripts for repository actions, the model Search performs repository-wide literal search and
selects from a small fixed set of tools, each with a returns matching snippets with surrounding context.
structured schema for execution (e.g., file path and Repository Tree displays the filtered file hierar-
optional line range) and bounded, model-readable chy (like shell tree), letting the model regain global
4

SHERLOC:StructuredDiagnosticLocalizationforCodeRepairAgents
| context.  | Connected |     | Tree     | summarizes |              | import | rela- |                |     |     |     |     | SHERLOC 0.88 |     |
| --------- | --------- | --- | -------- | ---------- | ------------ | ------ | ----- | -------------- | --- | --- | --- | --- | ------------ | --- |
| tionships | (direct   | and | reverse) | to follow  | dependencies |        |       |                |     |     |     |     |              |     |
|           |           |     |          |            |              |        |       | Qwen3-30B / SA |     |     |     |     | 0.77         |     |
across modules.
|     |     |     |     |     |     |     |     | Qwen3-30B / OH  |     |      |     | 0.75 |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --------------- | --- | ---- | --- | ---- | --- | --- |
|     |     |     |     |     |     |     |     | Coder-Next / SA |     | 0.56 |     |      |     |     |
0.56
Coder-Next / OH
| 3.3. Iterative |     | Interaction |     | Loop         |     |             |     | Next-80B / SA |     |     |     |      | 0.76 |      |
| -------------- | --- | ----------- | --- | ------------ | --- | ----------- | --- | ------------- | --- | --- | --- | ---- | ---- | ---- |
|                |     |             |     |              |     |             |     | Next-80B / OH |     |     |     | 0.75 |      |      |
| At the core    | of  | SHERLOC     |     | is a bounded |     | interaction |     |               |     |     |     |      |      |      |
|                |     |             |     |              |     |             |     | MiniMax / SA  |     |     |     |      |      | 0.90 |
loopofatmost20turns;ateachturnthemodeleither
|               |            |      |            |             |               |           |        | MiniMax / OH    |     |      |      |      | 0.82 |      |
| ------------- | ---------- | ---- | ---------- | ----------- | ------------- | --------- | ------ | --------------- | --- | ---- | ---- | ---- | ---- | ---- |
| makes a       | tool call  | or   | terminates | with        | final         | locations |        |                 |     |      |      |      |      |      |
|               |            |      |            |             |               |           |        | Qwen3-480B / SA |     |      |      |      |      | 0.87 |
| and findings. | The        | loop | has        | four steps. |               |           |        |                 |     |      |      |      |      |      |
|               |            |      |            |             |               | Reasoning |        | Qwen3-480B / OH |     |      |      |      | 0.82 |      |
| and action    | selection: |      | the        | LLM         | receives      | the       | issue, |                 |     |      |      |      |      |      |
|               |            |      |            |             |               |           |        |                 |     | 0.55 | 0.65 | 0.75 | 0.85 |      |
| repository    | context,   | and  | previous   |             | observations, |           | then   |                 |     |      |      |      |      |      |
File-level Hit@1
| decides | whether | additional |     | evidence | is needed |     | and, if |     |     |     |     |     |     |     |
| ------- | ------- | ---------- | --- | -------- | --------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
so, emits one structured action. Action parsing: Figure 6: Localization headroom by
a parser extracts a tool call or a final answer; final downstream LLM agent. File-level Hit@1 of each
|         |         |            |     |       |            |          |     | code repair | LLM | agent’s | own | localization | (blue) | vs. |
| ------- | ------- | ---------- | --- | ----- | ---------- | -------- | --- | ----------- | --- | ------- | --- | ------------ | ------ | --- |
| answers | contain | a findings |     | block | (5 fields: | location |     |             |     |         |     |              |        |     |
explanation, root cause, solution idea, dependencies, SHERLOC (green dashed line, 0.88). The gap
testing impact; see Figure 5 and Section J.1) and between each bar and the SHERLOC line is the
a locations block. Tool execution: the executor agent’s headroom; weaker agents have larger
runs the action and appends the observation to the headroom and gain more from external findings. Full
|              |             |        |              |        |         |      |      | numbers | in Appendix |     | L.  |     |     |     |
| ------------ | ----------- | ------ | ------------ | ------ | ------- | ---- | ---- | ------- | ----------- | --- | --- | --- | --- | --- |
| conversation | history.    |        | Termination: |        | the     | loop | ends |         |             |     |     |     |     |     |
| when a       | valid final | answer | is           | parsed | or when | the  | step |         |             |     |     |     |     |     |
budgetisexhausted,inwhichcaseafinal-turnprompt
| forces synthesis   |     | from | gathered   | evidence. |     |     |     |                                       |          |             |            |         |            |         |
| ------------------ | --- | ---- | ---------- | --------- | --- | --- | --- | ------------------------------------- | -------- | ----------- | ---------- | ------- | ---------- | ------- |
|                    |     |      |            |           |     |     |     | 4.1. Localization                     |          | Performance |            | and     | Efficiency |         |
|                    |     |      |            |           |     |     |     | WeevaluateourframeworkacrossSWE-Bench |          |             |            |         |            | Lite    |
|                    |     |      |            |           |     |     |     | and SWE-Bench                         |          | Verified    |            | using 4 | backbone   | mod-    |
| 3.4. Self-Recovery |     |      | Mechanisms |           |     |     |     |                                       |          |             |            |         |            |         |
|                    |     |      |            |           |     |     |     | els and                               | 3 seeds. | Figure      | 2 compares |         | against    | leading |
We add recovery for common failure modes in multi- localizers including [Li et al., 2025],
SWE-Debate
| turn tool    | use (Section   |     | H): context |                | management |           | (trun- |                |        |     |             |     |          |     |
| ------------ | -------------- | --- | ----------- | -------------- | ---------- | --------- | ------ | -------------- | ------ | --- | ----------- | --- | -------- | --- |
|              |                |     |             |                |            |           |        | SWERank        | [Reddy | et  | al., 2025], | and | OrcaLoca | [Yu |
| cating older | observations), |     |             | loop detection |            | (warnings |        | et al., 2025]. |        |     |             |     |          |     |
| for repeated | unproductive   |     |             | calls),        | implicit   | tool-call |        |                |        |     |             |     |          |     |
OnSWE-BenchLite,ourframeworkwithQwen3-
| recovery        | (parsing        | malformed  |            | but  | unambiguous   |          | re-    |                    |            |             |              |               |        |           |
| --------------- | --------------- | ---------- | ---------- | ---- | ------------- | -------- | ------ | ------------------ | ---------- | ----------- | ------------ | ------------- | ------ | --------- |
|                 |                 |            |            |      |               |          |        | 235B-A22B-Thinking |            |             | (Qwen3-235B) |               | [Yang  | et al.,   |
| quests),        | response-length |            | management |      | (re-prompting |          |        |                    |            |             |              |               |        |           |
|                 |                 |            |            |      |               |          |        | 2025] achieves     |            | 84.33±0.72% | accuracy@1   |               | in     | 5.0 turns |
| when generation |                 | approaches |            | safe | limits),      | and      | final- |                    |            |             |              |               |        |           |
|                 |                 |            |            |      |               |          |        | on average,        | surpassing |             | OrcaLoca     | on            | Claude | 3.5 Son-  |
| turn prompting  |                 | (forcing   | synthesis  |      | when          | the step | bud-   |                    |            |             |              |               |        |           |
|                 |                 |            |            |      |               |          |        | net (83.33%)       | and        | SWERank     |              | on fine-tuned |        | Qwen2.5-  |
get is exhausted).
|            |     |     |     |     |     |     |     | 32B (83.21%). |        | At the                        | chunk       | level, it   | reaches  | 39.14%   |
| ---------- | --- | --- | --- | --- | --- | --- | --- | ------------- | ------ | ----------------------------- | ----------- | ----------- | -------- | -------- |
|            |     |     |     |     |     |     |     | coverage      | recall | and 44.54%                    | precision.  |             |          |          |
|            |     |     |     |     |     |     |     | OnSWE-Bench   |        | Verified,thebestconfiguration |             |             |          |          |
| 4. Results |     |     |     |     |     |     |     | (Qwen3-235B)  |        | achieves                      | 81.27±1.16% |             | recall@1 | with     |
|            |     |     |     |     |     |     |     | 4.7 average   | turns, | a                             | 13.2 pp     | improvement |          | over the |
We evaluate SHERLOC along four axes: (i) the previous state-of-the-art (RepoSearcher / ToolTrain-
quality of its predicted code locations and (ii) the 32B-FT,68.03%)[Maetal.,2025]. Atthechunklevel,
robustness of those predictions to benchmark con- it reaches 41.28% coverage recall and 53.47% preci-
tamination and to LLM backbone choice (addressing sion. Becausepriorsystemsdonotreportchunk-level
RQ1; Sections 4.1, 4.3 and 4.4); and (iii) the transfer metrics, these span scores primarily characterize how
of its outputs to downstream code repair, gated by tightly SHERLOC’s predicted regions cover the gold
(iv) the quality of its diagnostic findings under an edit spans rather than serving as a direct baseline
LLM judge (addressing RQ2; Section 4.6). Through- comparison. At a matched ∼30B scale, Qwen3-30B-
out, we report file-level metrics (precision, recall, F1, A3B-Thinkingreaches75.07±1.24%recall@1,outper-
exact match, hit@1) over the predicted file set and forming every prior open-weight 32B baseline includ-
structure-agnostic chunk-level metrics (coverage re- ing the fine-tuned ToolTrain-32B variant (+7.0 pp)
call, precision, average tightness) over (start, end) and the non-fine-tuned RepoSearcher and OrcaLoca
line-number spans; formal definitions in Section B. on Qwen-32B (+16.3 and +18.3 pp).
5

SHERLOC:StructuredDiagnosticLocalizationforCodeRepairAgents
DeepSeek-V3-0324 [DeepSeek-AI, 2024] reaches Baseline 61.6
79.53±0.47% on Verified, confirming cross-family
Low
20.0
transfer. Fullper-backbonenumbers(includingchunk- n=55
level metrics and tool-engagement) appear in Table 3; Medium
31.5
the complete metric grid is in Section B. n=73
High
38.6
Atthetrajectorylevel, thesearchremainscompact n=101
while scaling with problem difficulty: turns rise from Very High
75.9
4.22 (easy) to 5.05/5.21 (medium/hard) and total n=270
tokens from 21.3k to 32.8k/35.1k (Sections F and G). 0 20 40 60 80
Resolve Rate (%)
4.2. Component Ablations Figure 7: Resolve rate by composite
finding-quality bucket. SWE-Bench Verified /
We ablate each component of our framework and OpenHands / Qwen3-Coder-480B-A35B-Instruct.
showtheimpactofeachseparatetoolandmechanism Buckets: Low [1.0,2.0], Medium (2.0,3.0],
on 100 samples from the SWE-Gym development High (3.0,4.0], Very High (4.0,5.0]. Very-high-quality
set [Pan et al., 2025] (full breakdown in Section A). findings resolve at 75.9%; low-quality findings
Removing any single tool or self-recovery mechanism actively underperform the 61.6% baseline.
degrades localization, with View File (−7.0 pp F1)
andthefinal-turnprompt(−5.0ppF1)asthelargest
contributors, indicating that both code inspection masked-issuesettingandtheheavily-maskedtext-only
and synthesis pressure are central. settingestimatesthecontributionofactiverepository
exploration beyond parametric familiarity.
4.3. ImplicitKnowledgevs.Tool-AssistedRea-
soning 4.4. Backbone Generalization and Tool En-
gagement
Because SWE-Bench repositories are public and
widelyrepresentedinpretrainingcorpora,localization To separate the SHERLOC method from the
accuracycanreflectbothactivereasoningandimplicit backbone, we evaluate 5 models from 2 fami-
knowledge of familiar codebases [Liang et al., 2025]. lies: Qwen3-235B-A22B-Thinking, Qwen3-30B-A3B-
We treat this as a validity concern and conduct a Thinking, and Qwen3-30B-A3B-Instruct [Yang et al.,
controlled masking study with Qwen3-235B on SWE- 2025]; DeepSeek-V3-0324 [DeepSeek-AI, 2024]; and
Bench Verified, progressively removing repository DeepSeek-R1-0528 [DeepSeek-AI, 2025]. Runs use
access and identifying information (Table 5). Even identical code, prompts, tools, and self-recovery; only
when tools, the repository tree, and all file and mod- the backbone changes. Each uses 3 seeds on SWE-
ule paths in the issue are masked, the model still Bench Verified; recall, mean turns, and zero-tool
achieves 57.86% recall@1 from the issue text alone, rate are in Table 3.
often inferring the correct file from error messages,
First, SHERLOC transfers across model fami-
API names, and domain conventions. We interpret
lies: DeepSeek-V3-0324 reaches 79.53% recall, only
this primarily as repository familiarity with widely
1.7 pp below the Qwen3-235B ceiling and 11.5 pp
used foundational libraries, not as direct evidence
above the best published baseline [RepoSearcher,
that individual benchmark instances are memorized.
68.03%; Ma et al., 2025]. Second, tool engage-
Manually inspecting a random sample of 50 success-
ment matters: DeepSeek-R1-0528 makes 41% fewer
ful instances from this setting confirms 2 patterns:
tool calls and 32% fewer turns than Qwen3-235B,
reliance on (i) well-known APIs and libraries, and
with 10% producing locations without any tool call;
(ii) distinctive error messages that uniquely identify a
those zero-tool instances reach 69.3% recall vs. 73.6%
module. Quantitatively (Table 6), implicit recall con-
on its tool-using subset, so active exploration helps
centrates in popular projects (85.3% on scikit-learn,
even strong reasoning models. Third, scale alone is
87.5%onrequests),whilelesscommononeslikepylint
not enough: Qwen3-30B outperforms the larger R1-
and seaborn fall to 33.3%.
0528(75.07%vs.73.63%)whiletakingthemostturns
Crucially, this baseline familiarity does not explain (7.2 on average, vs. 4.7 for Qwen3-235B and 3.2 for
SHERLOC’s full performance. When tools and the R1-0528). R1-0528’s under-exploration is consistent
repository tree are retained but explicit paths are with DeepSeek’s lack of a marked system-role token:
removed from the issue text, SHERLOC reaches the prompt is delivered as bare preamble, reducing
79.96% recall@1, only 1.3 pp below the unmasked tool-use compliance. The Qwen3-30B-Thinking vs.
full system (81.27%). The ≈22 pp gap between this Qwen3-30B-Instruct ablation (Section A.1) reinforces
6

SHERLOC:StructuredDiagnosticLocalizationforCodeRepairAgents
this: reasoningiscriticalforsustainingthemulti-turn
protocol.
4.5. LLM-as-Judge Scoring of Findings
How reliable are the diagnostic findings that SHER-
LOC produces? To answer this, we score each find-
ing’scontentwithanLLM-as-judge. WeuseGPT-5.2
as a ground-truth-patch-conditioned judge that rates
each finding from 1 to 5 on three dimensions: root-
cause correctness, location accuracy, and solu-
tion actionability (prompt details in Section H; full
quality-scoring breakdown in Section J). The compos-
itequalityscoreisthemeanofthesethreedimensions,
andwecallafindinghigh-quality whenthiscomposite
is ≥ 4.0. Across the 499 judged findings, scores are
right-skewed: 270(54%)fallinVeryHigh(>4.0),101
(20%) in High (3.0 to 4.0), 73 (15%) in Medium (2.0
to 3.0), and 55 (11%) in Low (≤2.0) (Table 7). The
≥ 4.0 threshold therefore retains 317/500 instances
(63%) for the Quality-filtered SHERLOC inter-
vention applied downstream in Section 4.6, where
we also motivate this threshold against a sweep of
alternatives.
100
80
60
40
20
0
)%(
egarevoC
85
80
75
70
65
60
55
2.0 2.5 3.0 3.5 4.0 4.5 5.0
Quality-gate threshold
)%(
etar
evloseR
full grid in Table 11): Baseline (vanilla agent execu-
tion);Masked(baselinewithfilepathsandrepository
names masked, extending the implicit-knowledge con-
trol from Section 4.3); Shuffled findings (a SHER-
LOC location and finding from a different random
instance); All SHERLOC findings (SHERLOC’s
predicted locations and findings); Quality-filtered
SHERLOC (only findings with judge score ≥ 4.0,
otherwisefallingbacktobaseline);andOracle GPT-
5.2 (upper-bound finding conditioned on the ground-
truth patch).
Transfer gains depend on model capability.
Every repair-agent backbone benefits from SHER-
LOC findings on both axes (resolve rate and token
efficiency), but the optimal injection variant depends
ontheagent’sbaselinecapability(Table11). Smaller
and mid-sized models gain most from All SHERLOC
findings. For Qwen3-Coder-30B-A3B, SWE-Agent
rises from 44.7% to 54.0% and OpenHands from
49.4%to53.0%;Qwen3-Coder-NextandQwen3-Next-
80B-A3B-Instruct show +8 to +12 pp improvements
across both frameworks (Figure 3). These models
have low baseline resolve and large localization head-
room(Qwen3-Coder-Nextreachesonly0.56Hit@1vs.
our0.88; Figure6), soevenmoderate-qualityfindings
Pass resolve rate close a real gap. More capable models gain most from
Overall resolve rate Quality-filtered SHERLOC findings. MiniMax-M2.5
Coverage and Qwen3-Coder-480B-A35B already localize well;
optimal injecting every finding dilutes the prompt with low-
(4.5)
confidence diagnoses, and MiniMax loses 4 to 5 pp
under All SHERLOC (Table 11). The quality fil-
ter restores positive transfer: MiniMax-M2.5 reaches
76.6%(SWE-Agent,+2.2pp)and72.8%(OpenHands,
+0.6 pp), and Qwen3-Coder-480B-A35B gains +1.0
and +1.2 pp. Token efficiency improves uniformly.
Across all 5 repair models and 2 frameworks, SHER-
LOC findings reduce localization tokens by 9 to 66%
Figure 8: Quality-threshold sweep. Lines (left (36.7% on average) and total tokens by 23.1% on
axis): Pass resolved (blue) is resolve rate among
average (Figure 4 and Section L), giving the agent
instances meeting the threshold; Overall resolved
a targeted starting point and freeing context and
(dashed) is the filtered estimate with 61.6% baseline
interaction budget for repair. The largest cell-level
fallback for rejected instances. Bars (right axis):
efficiency gain is Qwen3-Coder-480B-A35B / SWE-
coverage. Stricter thresholds raise resolve rate while
Agent, where injecting findings cuts localization to-
shrinking coverage; Overall resolved peaks at 4.5.
kens from 188.9k to 64.6k (−66%) while leaving re-
solve rate unchanged at 63.0%, showing that even
for already-saturated repair agents the standalone
localizer pays for itself in search cost alone. The
4.6. Downstream Transfer to Code Repair
masked and shuffled controls remain close to baseline
Task
(Table 16), so gains come from instance-relevant di-
Does better localization translate into better down- agnostic guidance, not surface leakage or unrelated
stream issue resolution? We measure code-repair findings.
resolve rate (fraction of generated patches that pass
the held-out tests) on all 500 SWE-Bench Veri- Quality mediation. Judged finding quality
fied instances [Jimenez et al., 2024], using 2 agentic strongly predicts downstream success. On the Qwen3-
Coder-480B-A35B / OpenHands cell, very-high-
frameworks(SWE-Agent[Yangetal.,2024]andOpen-
Hands [Wang et al., 2025]) across 6 setups (Figure 3;
qualityfindings(composite>4.0)resolveat75.9%vs.
7

SHERLOC:StructuredDiagnosticLocalizationforCodeRepairAgents
20.0% for low-quality ones (Figure 7; 𝑛=4991), and localization without task-specific fine-tuning or multi-
Pearson 𝑟=0.45 between composite score and binary agent orchestration: 84.33% accuracy@1 on SWE-
repair outcome. Bench Lite and 81.27% recall@1 on SWE-Bench
Verified, with matched-scale performance compet-
Quality filtering operationalizes this as retrospec-
itive with other agentic methods. For RQ2, these
tive selection. Splitting the 500 Verified instances
locations and diagnostic findings transfer to existing
at composite 4.0 on the same cell, All-SHERLOC
code-repair agents, yielding on average +5.95 pp re-
lifts resolve rate from 74.8% to 80.4% (+5.7 pp) on
solve rate with 36.7% and 23.1% fewer localization
the 317 high-quality instances and from 38.5% to
and total tokens across 5 repair backbones and 2
31.3%(−7.2pp)onthe183lower-qualityones. Filter-
frameworks, while a judge-based quality filter pre-
ing thus preserves external context on reliable cases
vents negative transfer from unreliable findings.
while avoiding negative transfer where the agent’s
own search is better. The ≥4.0 cut is pre-specified We conclude that localization should be evaluated
as the strictest threshold covering a majority of the not just by file or function retrieval but by diagnostic
benchmark(63%),within2.2ppofthefiltered-overall actionability: a correct file with a misleading
optimum at 4.5 (Table 10 and Fig. 8). diagnosis still misleads the downstream agent.
Beyondbuglocalization,structuredfindingsmayben-
Solution content carries that signal. Two indepen-
efit repository-scale tasks such as test generation,
dent lenses converge: by per-dimension correlation
regressiontriage, refactoring, andmigrationplanning,
on the 480B / OpenHands cell, solution actionability
where intermediate reasoning matters as much as the
is the strongest individual predictor of repair suc-
final action. Replacing our ground-truth-conditioned
cess (𝑟=0.46, vs. 𝑟=0.41 for root-cause and 𝑟=0.36
quality judge with a deployable test-time estimator,
for location accuracy); by causal field ablation on
forexampleonebasedonfindingconsistency,evidence
Qwen3-Coder-30B-A3B / SWE-Agent (Table 9), re-
coverage,andself-checksignals,remainsacentralnext
moving the solution idea field produces the largest
step.
single-field drop while all other reduced variants still
beat the baseline. The transferable signal therefore
comes from correct root-cause and solution content,
not from merely seeing a SHERLOC-formatted hint. Limitations
Findings help most on multi-file bugs. On Implicit-knowledge confound. Our implicit-
the 71 Verified instances requiring 2 or more file
knowledge controls show that ≈58% of localization
changes,All-SHERLOCfindingsimproveresolverate
recall on SWE-Bench Verified is achievable from
by +5.6 pp (32.4% vs. 26.8%).
issuetextalone,withstrongper-repositoryconcentra-
Finally, we separate accuracy from efficiency trans- tion: scikit-learn and requests reach 85–88% masked
fer by injecting findings from the weaker Qwen3-30B recallwhilepylintandseabornfallto33%(SectionE).
SHERLOC(Hit@10.786vs.0.884; Table17). These Headline SWE-Bench localization numbers, ours in-
weaker findings no longer improve Qwen3-Coder-30B- cluded,thereforepartlyreflectLLMpretrainingfamil-
A3B but still improve Qwen3-Coder-Next (SWE- iaritywithwidelydistributedopen-sourcecoderather
Agent 45.2%→49.2%; OpenHands 44.6%→45.4%; Ta- than transferable code reasoning. Our masked-issue
ble 12), and still reduce localization tokens by 16 to control (79.96% with tools retained) bounds but does
32% (24.5% on average) and total tokens by 1 to not eliminate this confound; a clean evaluation would
17% (7.5% on average) across all 4 cells (Table 14). require a held-out repository distribution.
Localizerqualitythusgovernsaccuracytransfer; even
imperfect findings reduce search cost by anchoring
initial exploration.
Benchmark and framework scope. Code-repair
transfer is measured on SWE-Bench Verified
throughtworepairframeworks(SWE-Agent,Open-
5. Conclusion
Hands) and five repair backbones. Generalization to
other benchmarks (e.g., SWE-Bench Multimodal,
Our work on SHERLOC shows that structured di-
multilingual variants), newer benchmark snapshots,
agnostic output, not just location retrieval, is the
additional agent frameworks, and non-Python repos-
operative unit of useful localization. For RQ1, a
itories (JavaScript, Java, C++) remains open. The
single reasoning LLM with compact repository tools
Connected Treetoolreliesonathinlanguage-specific
and self-recovery can reach state-of-the-art file-level
importparser,triviallyimplementedforanylanguage
with a standard import syntax; the rest of SHER-
1Thebenchmarkcontains500instances;oneproducedno
LOC is language-agnostic.
finding.
8

SHERLOC:StructuredDiagnosticLocalizationforCodeRepairAgents
Compute cost of the headline configuration. Computing infrastructure and budget. All
Our best numbers use Qwen3-235B-A22B-Thinking experiments are inference-only and run on inter-
with up to 20 reasoning turns per instance, so the nal compute clusters of NVIDIA H100 (80GB) and
headline localization rows are not directly compara- A100 (80GB) GPUs. Backbones are served via
ble on serving cost to the fine-tuned 32B baselines sglang [Zheng et al., 2024] (localization) and vLLM
we cite. The matched-scale 30B row (75.07% on (downstream code repair), with serving footprints
Verified, +7.0 pp over RepoSearcher) is the most ranging from 2–4 GPUs for the 30B backbones to
cost-comparable point of evidence for the method a full 8-GPU node for Qwen3-235B-A22B-Thinking
itself; the +6.2 pp from 235B over 30B partly reflects and Qwen3-Coder-480B-A35B-Instruct. Aggregating
model scale. the localization grid, component and reasoning-mode
|     |     |     |     |     |     |     | ablations, | implicit-knowledge |     |     | controls, | and | the down- |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ------------------ | --- | --- | --------- | --- | --------- |
streamcode-repairgrid(5repairbackbones×2frame-
|             |     |        |     |              |     |           | works ×          | 7 conditions |     | on all          | 500 SWE-Bench |        | Veri-    |
| ----------- | --- | ------ | --- | ------------ | --- | --------- | ---------------- | ------------ | --- | --------------- | ------------- | ------ | -------- |
| Cross-model |     | prompt |     | sensitivity. |     | Identical |                  |              |     |                 |               |        |          |
|             |     |        |     |              |     |           | fied instances), |              | the | total inference |               | budget | reported |
promptselicitdifferenttool-usebehavioracrossmodel
|           |                   |     |     |            |     |         | in the paper | is  | on the | order | of ∼10,000 | H100/A100 |     |
| --------- | ----------------- | --- | --- | ---------- | --- | ------- | ------------ | --- | ------ | ----- | ---------- | --------- | --- |
| families: | DeepSeek-R1-0528, |     |     | which does | not | support |              |     |        |       |            |           |     |
GPU-hours.
| marked system |     | roles,      | exhibits | 10% zero-tool |     | shortcut-   |     |     |     |     |     |     |     |
| ------------- | --- | ----------- | -------- | ------------- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- |
| ting under    | the | same prompt |          | text (Section |     | 4.4). Pick- |     |     |     |     |     |     |     |
ingabackbonewithsystem-promptsupportsidesteps All SHERLOC localiza-
|                  |     |          |     |          |         |     | Sampling  | parameters. |             |     |         |       |         |
| ---------------- | --- | -------- | --- | -------- | ------- | --- | --------- | ----------- | ----------- | --- | ------- | ----- | ------- |
| this; otherwise, |     | reaching | the | reported | numbers | on  |           |             |             |     |         |       |         |
|                  |     |          |     |          |         |     | tion runs | use         | temperature |     | = 0.99, | top-𝑝 | = 0.95, |
a new backbone may require model-specific prompt top-𝑘 = 0 (disabled), a per-call generation cap of
| adaptation           | rather | than      | a strictly | drop-in      | deployment. |          |                |             |               |           |                 |                 |            |
| -------------------- | ------ | --------- | ---------- | ------------ | ----------- | -------- | -------------- | ----------- | ------------- | --------- | --------------- | --------------- | ---------- |
|                      |        |           |            |              |             |          | 81,920 tokens, |             | and at        | most      | 20 interaction  |                 | turns. All |
|                      |        |           |            |              |             |          | downstream     | code-repair |               | backbones |                 | use temperature |            |
|                      |        |           |            |              |             |          | = 0.7, top-𝑝   | =           | 0.8,          | and top-𝑘 | = 20            | under           | the stock  |
|                      |        |           |            |              |             |          | SWE-Agent      |             | and OpenHands |           | configurations. |                 | The        |
| Quality-based        |        | selection |            | is not yet   | deployable. |          |                |             |               |           |                 |                 |            |
|                      |        |           |            |              |             |          | LLM-as-judge   |             | quality       | scorer    | (GPT-5.2)       | uses            | temper-    |
| The quality-filtered |        | analysis  |            | uses GPT-5.2 |             | [OpenAI, |                |             |               |           |                 |                 |            |
2025a] as an external judge that is shown the ground- ature =0.1 and a 300-token output cap. Full per-run
truth patch. The judge-independent cells in Figure 3 inference parameters are in Section H.
(baseline, masked, shuffled, all-SHERLOC, Oracle We will release the full SHERLOC codebase, in-
| GPT-5.2) | provide | non-judge |     | evidence | for the | 2 trans- |         |                       |     |     |               |     |        |
| -------- | ------- | --------- | --- | -------- | ------- | -------- | ------- | --------------------- | --- | --- | ------------- | --- | ------ |
|          |         |           |     |          |         |          | cluding | tool implementations, |     |     | self-recovery |     | mecha- |
fer regimes, but the per-instance reliability analysis nisms, evaluation scripts, and all per-instance results
| and the | threshold | sweep | in  | Section | J.3 depend | on  |     |     |     |     |     |     |     |
| ------- | --------- | ----- | --- | ------- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
upon publication.
| this external    | supervision. |     |         | The quality-filtered |     | row    |     |     |     |     |     |     |     |
| ---------------- | ------------ | --- | ------- | -------------------- | --- | ------ | --- | --- | --- | --- | --- | --- | --- |
| should therefore |              | be  | read as | an analysis-time     |     | selec- |     |     |     |     |     |     |     |
tion experiment; substituting an open-weight judge Acknowledgments
| (e.g., GPT-OSS |     | [OpenAI, | 2025b]) | for | GPT-5.2 | would |     |     |     |     |     |     |     |
| -------------- | --- | -------- | ------- | --- | ------- | ----- | --- | --- | --- | --- | --- | --- | --- |
remove the proprietary dependency, but the judge WethankSomshubraMajumdar,VahidNoroozi,Wasi
currently scores against the ground-truth patch, so Uddin Ahmad, Nikolai Ludwig, Mehrzad Samadi,
a true test-time mechanism additionally requires a Aleksander Ficek, and Siddhartha Jain (NVIDIA)
patch-freeself-verificationcheckorhumanannotation for valuable discussions and feedback that helped
|     |     |     |     |     |     |     | shape this | work. | The | work benefited |     | from funding | by  |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ----- | --- | -------------- | --- | ------------ | --- |
study.
|                 |     |     |           |     |     |     | the DFG    | (German  | Research |             | Foundation) |     | under the |
| --------------- | --- | --- | --------- | --- | --- | --- | ---------- | -------- | -------- | ----------- | ----------- | --- | --------- |
|                 |     |     |           |     |     |     | Excellence | Strategy |          | – EXC-3057. |             |     |           |
| Reproducibility |     |     | Statement |     |     |     |            |          |          |             |             |     |           |
References
| Theexactprompts(systemprompt, |              |       |            |     | tooldescriptions, |     |             |     |       |              |     |                |     |
| ----------------------------- | ------------ | ----- | ---------- | --- | ----------------- | --- | ----------- | --- | ----- | ------------ | --- | -------------- | --- |
| final-turn                    | prompt,      | judge | prompt)    | and | inference         | pa- |             |     |       |              |     |                |     |
|                               |              |       |            |     |                   |     | Rui Abreu,  |     | Peter | Zoeteweij,   |     | and Arjan      | JC  |
| rameters                      | are provided |       | in Section | H.  | All experiments   |     |             |     |       |              |     |                |     |
|                               |              |       |            |     |                   |     | Van Gemund. |     | On    | the accuracy | of  | spectrum-based |     |
use publicly available models (Qwen3-235B-A22B- fault localization.
|           |                         |     |     |     |            |     |                  |     |          | Testing: | Academic     | and         | Indus- |
| --------- | ----------------------- | --- | --- | --- | ---------- | --- | ---------------- | --- | -------- | -------- | ------------ | ----------- | ------ |
| Thinking, | Qwen3-30B-A3B-Thinking, |     |     |     | Qwen3-30B- |     |                  |     |          |          |              |             |        |
|           |                         |     |     |     |            |     | trial Conference |     | Practice |          | and Research | Techniques, |        |
A3B-Instruct,DeepSeek-V3-0324,DeepSeek-R1-0528)
|            |        |        |     |             |       |        | pages | 89–98, | 2007. |     |     |     |     |
| ---------- | ------ | ------ | --- | ----------- | ----- | ------ | ----- | ------ | ----- | --- | --- | --- | --- |
| served via | sglang | [Zheng | et  | al., 2024]; | model | names, |       |        |       |     |     |     |     |
versions, and all hyperparameters are specified. Eval- Zhaoling Chen, Robert Tang, Gangda Deng, Fang
uation is conducted on the public SWE-Bench Lite Wu,JialongWu,ZhiweiJiang,ViktorPrasanna,Ar-
and SWE-Bench Verified benchmarks using their man Cohan, and Xingyao Wang. Locagent: Graph-
official evaluation harnesses. guided llm agents for code localization. In
Pro-
9

SHERLOC:StructuredDiagnosticLocalizationforCodeRepairAgents
ceedings of the 63rd Annual Meeting of the Asso- Yiling Lou, Qihao Zhu, Jinhao Dong, Xia Li, Zeyu
|         |                   |     |     |             |         |     | Sun, Dan | Hao, | Lu Zhang, | and Lingming | Zhang. |
| ------- | ----------------- | --- | --- | ----------- | ------- | --- | -------- | ---- | --------- | ------------ | ------ |
| ciation | for Computational |     |     | Linguistics | (Volume | 1:  |          |      |           |              |        |
Long Papers), pages 8697–8727. Association for Boosting coverage-based fault localization via
Computational Linguistics, 2025. doi: 10.18653/ graph-basedrepresentationlearning.
Proceedingsof
v1/2025.acl-long.426. URLhttps://aclanthology. the 29th ACM Joint Meeting on European Software
org/2025.acl-long.426/. Engineering Conference and Symposium on the
(ESEC/FSE),
|     |     |     |     |     |     |     | Foundations | of Software |     | Engineering |     |
| --- | --- | --- | --- | --- | --- | --- | ----------- | ----------- | --- | ----------- | --- |
DeepSeek-AI. Deepseek-v3 technical report, 2024. pages 664–676, 2021.
URL https://arxiv.org/abs/2412.19437.
|     |     |     |     |     |     |     | Zexiong Ma, | Chao | Peng, | Qunhong Zeng, | Pengfei |
| --- | --- | --- | --- | --- | --- | --- | ----------- | ---- | ----- | ------------- | ------- |
DeepSeek-AI. Deepseek-r1: Incentivizing reasoning Gao, Yanzhen Zou, and Bing Xie. Tool-integrated
capability in llms via reinforcement learning, 2025. reinforcement learning for repo deep search, 2025.
URL https://arxiv.org/abs/2501.12948.
URL https://arxiv.org/abs/2508.03012.
Zhonghao Jiang, Xiaoxue Ren, Meng Yan, Wei Jiang, Seokhyeon Moon, Yunho Kim, Moonzoo Kim, and
YongLi,andZhongxinLiu.Cosil: Issuelocalization Shin Yoo. Ask the mutants: Mutating faulty pro-
via llm-driven code graph searching, 2025. URL grams for fault localization. In Proceedings of the
https://arxiv.org/abs/2503.22424.
|          |            |      |       |           |     |           | IEEE International |     | Conference     | on Software      | Test- |
| -------- | ---------- | ---- | ----- | --------- | --- | --------- | ------------------ | --- | -------------- | ---------------- | ----- |
|          |            |      |       |           |     |           | ing, Verification  |     | and Validation | (ICST),pages153– |       |
| Carlos E | Jimenez,   | John | Yang, | Alexander |     | Wettig,   | 162, 2014.         |     |                |                  |       |
| Shunyu   | Yao, Kexin | Pei, | Ofir  | Press,    | and | Karthik R |                    |     |                |                  |       |
Narasimhan. SWE-bench: Can language models OpenAI. Gpt-5 system card. OpenAI Sys-
resolve real-world github issues? In The Twelfth tem Card, 2025a. URL https://openai.
|               |     |            |     |          |             |     | com/index/gpt-5-system-card/. |     |     |     | Archived |
| ------------- | --- | ---------- | --- | -------- | ----------- | --- | ----------------------------- | --- | --- | --- | -------- |
| International |     | Conference | on  | Learning | Representa- |     |                               |     |     |     |          |
tions,2024. URLhttps://openreview.net/forum? at https://web.archive.org/web/2025/https:
| id=VTF8yNQM66. |     |     |     |     |     |     | //openai.com/index/gpt-5-system-card/. |     |     |     |     |
| -------------- | --- | --- | --- | --- | --- | --- | -------------------------------------- | --- | --- | --- | --- |
James A Jones, Mary Jean Harrold, and John Stasko. OpenAI. gpt-oss-120b & gpt-oss-20b
Visualization of test information to assist fault lo- model card. OpenAI Open-Weight Re-
| calization. | In  |     |     |     |     |     |     |     |     |     |     |
| ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Proceedings of the 24th International lease, 2025b. URL https://openai.com/
Conference on Software Engineering (ICSE), pages index/gpt-oss-model-card/. Archived at
| 467–477, | 2002. |     |     |     |     |     |     |     |     |     |     |
| -------- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
https://web.archive.org/web/2025/https:
//openai.com/index/gpt-oss-model-card/.
| SungminKang, | GabinAn, |     | andShinYoo. |     | Aquantita- |     |     |     |     |     |     |
| ------------ | -------- | --- | ----------- | --- | ---------- | --- | --- | --- | --- | --- | --- |
tiveandqualitativeevaluationofllm-basedexplain- Jiayi Pan, Xingyao Wang, Graham Neubig, Navdeep
able fault localization. Proceedings of the ACM on Jaitly, Heng Ji, Alane Suhr, and Yizhe Zhang.
Software Engineering, 1(FSE):Article 64, 2024. doi: Training software engineering agents and verifiers
10.1145/3660771.
|     |     |     |     |     |     |     | with swe-gym, |     | 2025. | URL https://arxiv.org/ |     |
| --- | --- | --- | --- | --- | --- | --- | ------------- | --- | ----- | ---------------------- | --- |
abs/2412.21139.
| Han Li, Yuling | Shi,  | Shaoxin | Lin, | Xiaodong |        | Gu, Heng |                |     |      |                          |     |
| -------------- | ----- | ------- | ---- | -------- | ------ | -------- | -------------- | --- | ---- | ------------------------ | --- |
| Lian, Xin      | Wang, | Yantao  |      | Jia, Tao | Huang, | and      |                |     |      |                          |     |
|                |       |         |      |          |        |          | Mike Papadakis | and | Yves | Le Traon. Metallaxis-fl: |     |
Qianxiang Wang. Swe-debate: Competitive multi- mutation-basedfaultlocalization. Software Testing,
agent debate for software issue resolution. Reliability, 25(5-7):605–628, 2015.
|          |                   |     |     |       |     | arXiv | Verification  | and    |       |                  |      |
| -------- | ----------------- | --- | --- | ----- | --- | ----- | ------------- | ------ | ----- | ---------------- | ---- |
| preprint | arXiv:2507.23348, |     |     | 2025. |     |       |               |        |       |                  |      |
|          |                   |     |     |       |     |       | Revanth Gangi | Reddy, | Tarun | Suresh, JaeHyeok | Doo, |
Xia Li, Wei Li, Yuqun Zhang, and Lingming Zhang. Ye Liu, Xuan Phi Nguyen, Yingbo Zhou, Semih
Deepfl: Integrating multiple fault diagnosis dimen- Yavuz, Caiming Xiong, Heng Ji, and Shafiq Joty.
sions for deep fault localization. In Proceedings of Swerank: Software issue localization with code
|             |         |         |               |     |           |       | ranking,2025. | URLhttps://arxiv.org/abs/2505. |     |                |           |
| ----------- | ------- | ------- | ------------- | --- | --------- | ----- | ------------- | ------------------------------ | --- | -------------- | --------- |
| the 28th    | ACM     | SIGSOFT | International |     | Symposium |       |               |                                |     |                |           |
| on Software | Testing |         | and Analysis  |     | (ISSTA),  | pages | 07849.        |                                |     |                |           |
| 169–180,    | 2019.   |         |               |     |           |       |               |                                |     |                |           |
|             |         |         |               |     |           |       | Ripon K.      | Saha, Matthew                  |     | Lease, Sarfraz | Khurshid, |
Shanchao Liang, Spandan Garg, and and Dewayne E. Perry. Improving bug localization
Roshanak Zilouchian Moghaddam. The swe- using structured information retrieval. In
Proceed-
bench illusion: When state-of-the-art llms ings of the 28th IEEE/ACM International Confer-
remember instead of reason, 2025. URL ence on Automated Software Engineering, pages
| https://arxiv.org/abs/2506.12286. |     |     |     |     |     |     | 345–355, | 2013. |     |     |     |
| --------------------------------- | --- | --- | --- | --- | --- | --- | -------- | ----- | --- | --- | --- |
10

SHERLOC:StructuredDiagnosticLocalizationforCodeRepairAgents
Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Yang Su, Yichang Zhang, Yinger Zhang, Yu Wan,
RobertaRaileanu,MariaLomeli,LukeZettlemoyer, Yuqiong Liu, Zekun Wang, Zeyu Cui, Zhenru
NicolaCancedda,andThomasScialom.Toolformer: Zhang, Zhipeng Zhou, and Zihan Qiu. Qwen3 tech-
Language models can teach themselves to use tools. nical report, 2025. URL
https://arxiv.org/abs/
| arXiv preprint |     | arXiv:2302.04761, |     |     | 2023. |     | 2505.09388. |     |     |     |     |     |     |
| -------------- | --- | ----------------- | --- | --- | ----- | --- | ----------- | --- | --- | --- | --- | --- | --- |
Shaowei Wang and David Lo. Version history, similar JohnYang,CarlosE.Jimenez,AlexanderWettig,Kil-
report, and structure: Putting them together for ian Lieret, Shunyu Yao, Karthik Narasimhan, and
| improved | bug | localization. |     | In          |     |        |             |     |            |                |     |     |            |
| -------- | --- | ------------- | --- | ----------- | --- | ------ | ----------- | --- | ---------- | -------------- | --- | --- | ---------- |
|          |     |               |     | Proceedings |     | of the | Ofir Press. |     | Swe-agent: | Agent-computer |     |     | interfaces |
22nd International Conference on Program Com- enable automated software engineering, 2024. URL
prehension, pages 53–63, 2014. https://arxiv.org/abs/2405.15793.
| Xingyao Wang, |     | Boxuan | Li, Yufan | Song, | Frank | F. Xu, |        |      |               |     |          |     |           |
| ------------- | --- | ------ | --------- | ----- | ----- | ------ | ------ | ---- | ------------- | --- | -------- | --- | --------- |
|               |     |        |           |       |       |        | Shunyu | Yao, | Jeffrey Zhao, |     | Dian Yu, | Nan | Du, Izhak |
Xiangru Tang, Mingchen Zhuge, Jiayi Pan, Yueqi Shafran, Karthik Narasimhan, and Yuan Cao. Re-
| Song, Bowen |     | Li, Jaskirat |     | Singh, | Hoang | H. Tran, |                  |     |           |     |     |        |             |
| ----------- | --- | ------------ | --- | ------ | ----- | -------- | ---------------- | --- | --------- | --- | --- | ------ | ----------- |
|             |     |              |     |        |       |          | Act: Synergizing |     | reasoning |     | and | acting | in language |
Fuqiang Li, Ren Ma, Mingzhang Zheng, Bill Qian, models. arXiv preprint arXiv:2210.03629, 2022.
Yanjun Shao, Niklas Muennighoff, Yizhe Zhang, URL https://arxiv.org/abs/2210.03629.
| Binyuan | Hui, | Junyang | Lin, | Robert | Brennan, | Hao |     |     |     |     |     |     |     |
| ------- | ---- | ------- | ---- | ------ | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
Peng, Heng Ji, and Graham Neubig. Openhands: Zhongming Yu, Hejia Zhang, Yujie Zhao, Hanxian
An open platform for ai software developers as Huang, Matrix Yao, Ke Ding, and Jishen Zhao.
generalist agents, 2025. URL https://arxiv.org/ Orcaloca: An llm agent framework for software
abs/2407.16741. issuelocalization. arXiv preprint arXiv:2502.00350,
2025.
| Jason Wei, | Xuezhi | Wang,   | Dale     | Schuurmans, |         | Maarten |         |        |         |       |       |      |         |
| ---------- | ------ | ------- | -------- | ----------- | ------- | ------- | ------- | ------ | ------- | ----- | ----- | ---- | ------- |
| Bosma,     | Brian  | Ichter, | Fei Xia, | Ed          | H. Chi, | Quoc V. |         |        |         |       |       |      |         |
|            |        |         |          |             |         |         | Yuntong | Zhang, | Haifeng | Ruan, | Zhiyu | Fan, | and Ab- |
Le, and Denny Zhou. Chain-of-thought prompt- hik Roychoudhury. Autocoderover: Autonomous
ing elicits reasoning in large language models. In program improvement, 2024. URL
https://arxiv.
Advances in Neural Information Processing Sys- org/abs/2404.05427.
| tems, volume |     | 35, pages | 24824–24837, |     |     | 2022. URL |     |     |     |     |     |     |     |
| ------------ | --- | --------- | ------------ | --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
https://arxiv.org/abs/2201.11903. Zhengyi Zhao, Shubo Zhang, Zezhong Wang, Huimin
|     |     |     |     |     |     |     | Wang, | Yutian | Zhao, | Bin | Liang, | Yefeng | Zheng, |
| --- | --- | --- | --- | --- | --- | --- | ----- | ------ | ----- | --- | ------ | ------ | ------ |
Menghua Wu, Cai Zhou, Stephen Bates, and Tommi Binyang Li, Kam-Fai Wong, and Xian Wu. T2:
Jaakkola. Thought calibration: Efficient and con- An adaptive test-time scaling strategy for contex-
| fident          | test-time     | scaling.     |       | In           |     |            |               |            |               |           |                |            |            |
| --------------- | ------------- | ------------ | ----- | ------------ | --- | ---------- | ------------- | ---------- | ------------- | --------- | -------------- | ---------- | ---------- |
|                 |               |              |       | Proceedings  |     | of the     | tual question |            | answering.    |           | In Proceedings |            | of the     |
| 2025 Conference |               | on Empirical |       | Methods      |     | in Natural |               |            |               |           |                |            |            |
|                 |               |              |       |              |     |            | 2025          | Conference | on            | Empirical |                | Methods    | in Natu-   |
| Language        | Processing,   |              | pages | 14291–14305. |     | Associ-    |               |            |               |           |                |            |            |
|                 |               |              |       |              |     |            | ral Language  |            | Processing,   |           | pages          | 3731–3756. | Asso-      |
| ation for       | Computational |              |       | Linguistics, |     | 2025. doi: |               |            |               |           |                |            |            |
|                 |               |              |       |              |     |            | ciation       | for        | Computational |           | Linguistics,   |            | 2025. doi: |
10.18653/v1/2025.emnlp-main.722. URL https: 10.18653/v1/2025.emnlp-main.185. URL
https:
//aclanthology.org/2025.emnlp-main.722/.
//aclanthology.org/2025.emnlp-main.185/.
| Chunqiu | Steven | Xia, Yinlin |     | Deng, | Soren | Dunn, and |         |        |            |     |      |          |      |
| ------- | ------ | ----------- | --- | ----- | ----- | --------- | ------- | ------ | ---------- | --- | ---- | -------- | ---- |
|         |        |             |     |       |       |           | Lianmin | Zheng, | Liangsheng |     | Yin, | Zhiqiang | Xie, |
Lingming Zhang. Agentless: Demystifying llm- Chuyue Sun, Jeff Huang, Cody Hao Yu, Shiyi Cao,
| based | software | engineering |     | agents, | 2024. | URL |     |     |     |     |     |     |     |
| ----- | -------- | ----------- | --- | ------- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
ChristosKozyrakis,IonStoica,JosephE.Gonzalez,
https://arxiv.org/abs/2407.01489. Clark Barrett, and Ying Sheng. Sglang: Efficient
|                |         |             |             |            |           |             | execution    | of              | structured                        | language    |              | model              | programs, |
| -------------- | ------- | ----------- | ----------- | ---------- | --------- | ----------- | ------------ | --------------- | --------------------------------- | ----------- | ------------ | ------------------ | --------- |
| An Yang,       | Anfeng  | Li, Baosong |             | Yang,      | Beichen   | Zhang,      |              |                 |                                   |             |              |                    |           |
|                |         |             |             |            |           |             | 2024.        | URL             | https://arxiv.org/abs/2312.07104. |             |              |                    |           |
| Binyuan        | Hui,    | Bo Zheng,   | Bowen       |            | Yu, Chang | Gao,        |              |                 |                                   |             |              |                    |           |
| Chengen        | Huang,  | Chenxu      |             | Lv, Chujie | Zheng,    | Day-        |              |                 |                                   |             |              |                    |           |
|                |         |             |             |            |           |             | Jian Zhou,   | Hongyu          | Zhang,                            |             | and David    |                    | Lo. Where |
| iheng Liu,     | Fan     | Zhou,       | Fei         | Huang,     | Feng      | Hu, Hao     |              |                 |                                   |             |              |                    |           |
|                |         |             |             |            |           |             | should       | the             | bugs be                           | fixed?      | more         | accurate           | infor-    |
| Ge, Haoran     |         | Wei, Huan   | Lin,        | Jialong    |           | Tang, Jian  |              |                 |                                   |             |              |                    |           |
|                |         |             |             |            |           |             | mation       | retrieval-based |                                   | bug         | localization |                    | based on  |
| Yang, Jianhong |         | Tu,         | Jianwei     | Zhang,     | Jianxin   | Yang,       |              |                 |                                   |             |              |                    |           |
|                |         |             |             |            |           |             | bug reports. |                 | Proceedings                       |             | of the       | 34th International |           |
| Jiaxi Yang,    |         | Jing Zhou,  | Jingren     |            | Zhou,     | Junyang     |              |                 |                                   |             |              |                    |           |
|                |         |             |             |            |           |             | Conference   |                 | on Software                       | Engineering |              | (ICSE),            | pages     |
| Lin, Kai       | Dang,   | Keqin       | Bao,        | Kexin      | Yang,     | Le Yu,      |              |                 |                                   |             |              |                    |           |
|                |         |             |             |            |           |             | 14–24,       | 2012.           |                                   |             |              |                    |           |
| Lianghao       | Deng,   | Mei         | Li,         | Mingfeng   | Xue,      | Mingze      |              |                 |                                   |             |              |                    |           |
| Li, Pei        | Zhang,  | Peng        | Wang,       | Qin        | Zhu,      | Rui Men,    |              |                 |                                   |             |              |                    |           |
| Ruize Gao,     | Shixuan |             | Liu, Shuang |            | Luo,      | Tianhao Li, |              |                 |                                   |             |              |                    |           |
Tianyi Tang, Wenbiao Yin, Xingzhang Ren, Xinyu Localization Analyses
| Wang, | Xinyu | Zhang, | Xuancheng |     | Ren, | Yang Fan, |     |     |     |     |     |     |     |
| ----- | ----- | ------ | --------- | --- | ---- | --------- | --- | --- | --- | --- | --- | --- | --- |
11

SHERLOC:StructuredDiagnosticLocalizationforCodeRepairAgents
A. Component Ablations: Tools and Table 1: Tool-suite ablation on 100 SWE-Gym
|     |     |     |     |     |     |     | development |     | issues. | Each | row | removes | one |     |
| --- | --- | --- | --- | --- | --- | --- | ----------- | --- | ------- | ---- | --- | ------- | --- | --- |
Self-Recovery
|     |     |     |     |     |     |     | localization | tool | while | holding | the | base | model, |     |
| --- | --- | --- | --- | --- | --- | --- | ------------ | ---- | ----- | ------- | --- | ---- | ------ | --- |
Tables 1 and 2 evaluate the localization agent on the prompt, self-recovery settings, and evaluation set
|          |          |         |     |         |             |     | fixed. File-level |     | columns | report |     | precision, | recall, | F1, |
| -------- | -------- | ------- | --- | ------- | ----------- | --- | ----------------- | --- | ------- | ------ | --- | ---------- | ------- | --- |
| same 100 | randomly | sampled |     | SWE-Gym | development |     |                   |     |         |        |     |            |         |     |
issues. We ablate one component at a time while exact match, and set accuracy; chunk-level columns
|         |             |        |               |     |            |        | report coverage |                | recall | and    | tightness. | Parenthesized |           |      |
| ------- | ----------- | ------ | ------------- | --- | ---------- | ------ | --------------- | -------------- | ------ | ------ | ---------- | ------------- | --------- | ---- |
| holding | the base    | model, | prompts,      |     | sampling   | setup, |                 |                |        |        |            |               |           |      |
|         |             |        |               |     |            |        | values are      | absolute-point |        | deltas | from       | the           | all-tools | full |
| and all | other tools | or     | self-recovery |     | mechanisms | fixed. |                 |                |        |        |            |               |           |      |
system.
File-levelmetrics(precision,recall,F1,exactmatch,
andsetaccuracy)arecomputedoverthepredictedfile
|     |     |     |     |     |     |     | AblatedTool |     | File-Level |     |     | File-Level(set) | Chunk-Level |     |
| --- | --- | --- | --- | --- | --- | --- | ----------- | --- | ---------- | --- | --- | --------------- | ----------- | --- |
set; chunk-level metrics (coverage recall and average Prec. Rec. F1 Exact Acc. Cov.Rec.Tight.
|     |     |     |     |     |     |     | AllTools | 77.1 | 58.23 | 63.19 | 37.0 |     | 56.31 27.49 | 27.97 |
| --- | --- | --- | --- | --- | --- | --- | -------- | ---- | ----- | ----- | ---- | --- | ----------- | ----- |
tightness)arecomputedover(start,end)line-number
|     |     |     |     |     |     |     | w/oViewFile | 69.66(-7.4)51.70(-6.5)56.19(-7.0) |     |     | 35.0(-2.0) | 49.95(-6.36) | 22.32 | 19.40 |
| --- | --- | --- | --- | --- | --- | --- | ----------- | --------------------------------- | --- | --- | ---------- | ------------ | ----- | ----- |
spans. Parenthesized values are absolute-point deltas w w / / o o C R o ep d o eb T a r s e e e Search 7 7 1 6 . . 7 3 3 3 ( ( - - 5 0 . . 3 7 ) ) 5 5 6 3 . . 8 4 8 2 ( ( - - 1 4 . . 3 8 ) ) 5 6 7 2 . . 7 3 0 4 ( ( - - 5 0 . . 4 8 ) ) 3 3 8 2 . . 0 0 ( ( + -5 1 . . 0 0 ) ) 5 5 0 5 . . 5 9 9 6 ( ( - - 5 0 . . 7 3 2 5 ) ) 2 2 1 8 . . 7 2 5 0 2 2 6 0 . .4 0 2 2
|             |        |               |     |             |     |            | w/oConnectedTree | 71.50(-5.6)   | 54.65(-3.5) | 58.63(-4.5) | 35.0(-2.0) | 52.05(-4.26) |     | 26.50 23.41 |
| ----------- | ------ | ------------- | --- | ----------- | --- | ---------- | ---------------- | ------------- | ----------- | ----------- | ---------- | ------------ | --- | ----------- |
| relative    | to the | corresponding |     | full-system |     | row in the |                  |               |             |             |            |              |     |             |
| same table. |        |               |     |             |     |            | Table 2:         |               |             |             |            |              | 100 |             |
|             |        |               |     |             |     |            |                  | Self-recovery |             | ablation    |            | on           |     |             |
Across both ablations, the largest performance SWE-Gym development issues. Each row
|            |            |              |                  |             |      |              | removes       | one recovery/control |        |                    | mechanism |         | while  |      |
| ---------- | ---------- | ------------ | ---------------- | ----------- | ---- | ------------ | ------------- | -------------------- | ------ | ------------------ | --------- | ------- | ------ | ---- |
| drops come | from       | removing     |                  | View        | File | (tool suite) |               |                      |        |                    |           |         |        |      |
|            |            |              |                  |             |      |              | holding       | the base             | model, | tool               | suite,    | prompt, |        | and  |
| and the    | final-turn | prompt       | (self-recovery), |             |      | confirming   |               |                      |        |                    |           |         |        |      |
|            |            |              |                  |             |      |              | evaluation    | set                  | fixed. | Columns            | match     | Table   | 1;     |      |
| that code  | inspection | and          | forced           | final-turn  |      | synthesis    |               |                      |        |                    |           |         |        |      |
|            |            |              |                  |             |      |              | parenthesized |                      | values | are absolute-point |           |         | deltas | from |
| are the    | two most   | load-bearing |                  | components. |      |              |               |                      |        |                    |           |         |        |      |
the full system.
| A.1. Reasoning-Mode |     |     | Ablation: |     | Thinking | vs. |                  |     |            |      |                 |      |                     |     |
| ------------------- | --- | --- | --------- | --- | -------- | --- | ---------------- | --- | ---------- | ---- | --------------- | ---- | ------------------- | --- |
|                     |     |     |           |     |          |     | AblatedComponent |     | File-Level |      | File-Level(set) |      | Chunk-Level         |     |
|                     |     |     |           |     |          |     |                  |     | Prec.      | Rec. | F1 Exact        | Acc. | Cov.Rec.Tight.Prec. |     |
Instruct All(fullsystem) 77.1 58.23 63.19 37.0 56.31 27.49 27.97 49.22
|     |     |     |     |     |     |     | w/oImplicitToolDetection | 74.0(-3.1) | 53.78(-4.4) | 59.14(-4.0) | 36.0(-0.1) | 52.63(-3.6) | 25.94 | 21.78 49.37 |
| --- | --- | --- | --- | --- | --- | --- | ------------------------ | ---------- | ----------- | ----------- | ---------- | ----------- | ----- | ----------- |
To isolate the contribution of extended reasoning, w w / / o o L C o o o n p te D xt et M ec a t n io a n gement 7 7 3 6 . . 3 6 3 6 ( ( - - 3 0 . . 7 4 ) ) 5 5 5 6 . . 1 7 6 4 ( ( - - 3 1 . . 0 4 ) ) 6 5 1 9 . . 7 8 8 4 ( ( - - 1 3 . . 4 3 ) )3 3 9 6 . . 0 0 ( ( + -0 2 . . 1 0 ) ) 5 5 4 4 . . 6 0 7 5 ( ( - - 1 2 . . 6 2 ) ) 2 2 6 6 . . 5 1 2 8 3 2 0 8 . . 8 0 6 4 4 5 8 2 . .3 0 8 2
|                  |                        |              |            |                |           |          | w/oResponseLengthMgmt.74.26(-2.8)56.53(-1.7) |                                                       |     | 60.62(-2.5) | 35.0(-2.0)   | 53.71(-2.6) | 26.92 | 27.95 52.58 |
| ---------------- | ---------------------- | ------------ | ---------- | -------------- | --------- | -------- | -------------------------------------------- | ----------------------------------------------------- | --- | ----------- | ------------ | ----------- | ----- | ----------- |
|                  |                        |              |            |                |           |          | w/oFinalTurnPrompt                           | 72.5(-4.6)54.08(-4.1)58.19(-5.0)31.0(-6.0)50.75(-5.5) |     |             |              |             | 27.76 | 23.66 49.30 |
| we compare       | Qwen3-30B-A3B-Thinking |              |            |                |           | against  |                                              |                                                       |     |             |              |             |       |             |
| its non-thinking |                        | counterpart  |            | Qwen3-30B-A3B- |           |          |                                              |                                                       |     |             |              |             |       |             |
| Instruct,        | which                  | shares       | the        | same           | parameter | count,   |                                              |                                                       |     |             |              |             |       |             |
|                  |                        |              |            |                |           |          | B. Per-Backbone                              |                                                       |     |             | Localization |             |       | Met-        |
| architecture,    | prompts,               |              | and tools. | The            | Instruct  | model    | rics                                         |                                                       |     |             |              |             |       |             |
| achieves         | only                   | 10.2% recall | on         | Verified       | and       | 11.7% on |                                              |                                                       |     |             |              |             |       |             |
Lite, versus74.0%and76.7%fortheThinkingmodel:
|     |     |     |     |     |     |     | Table 3 | reports | the | complete | evaluation |     | of  | SHER- |
| --- | --- | --- | --- | --- | --- | --- | ------- | ------- | --- | -------- | ---------- | --- | --- | ----- |
a ∼65 pp gap. The failure is not gradual degrada- LOC across all four backbone models on both SWE-
| tion but | near-total | collapse: |     | 87% of | Instruct | samples |       |          |           |     |     |           |           |     |
| -------- | ---------- | --------- | --- | ------ | -------- | ------- | ----- | -------- | --------- | --- | --- | --------- | --------- | --- |
|          |            |           |     |        |          |         | Bench | Lite and | SWE-Bench |     |     | Verified, | including |     |
fail to produce any valid output (success rate 13%), chunk-level metrics and tool-engagement statistics.
| with the | model | averaging | 0.2 | predicted | locations | per |     |     |     |     |     |     |     |     |
| -------- | ----- | --------- | --- | --------- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
File-levelmetricssummarizecorrectnessatthefileset
| instanceversus1.3fortheThinkingvariant. |     |     |     |     |     | Without |                    |     |         |     |          |              |     |        |
| --------------------------------------- | --- | --- | --- | --- | --- | ------- | ------------------ | --- | ------- | --- | -------- | ------------ | --- | ------ |
|                                         |     |     |     |     |     |         | level, chunk-level |     | metrics |     | quantify | localization |     | tight- |
extended chain-of-thought, the model cannot sustain ness and coverage, and the rightmost two columns
| the multi-turn |     | tool-use | protocol | that | SHERLOC | re- |         |             |     |       |       |           |       |     |
| -------------- | --- | -------- | -------- | ---- | ------- | --- | ------- | ----------- | --- | ----- | ----- | --------- | ----- | --- |
|                |     |          |          |      |         |     | capture | interaction |     | shape | (mean | reasoning | turns | and |
quires. Thisablation,controlledwithinasinglemodel the fraction of instances solved without any tool call).
family, shows that thinking-mode reasoning is critical Allvaluesarepercentagesunlessnoted. Twopatterns
forthismulti-turnexplorationanddiagnosisprotocol.
|     |     |     |     |     |     |     | stand out: | Qwen3-235B-A22B-Thinking |     |     |     |     | leads | every |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ------------------------ | --- | --- | --- | --- | ----- | ----- |
file-levelmetriconbothbenchmarks,andatthechunk
|     |     |     |     |     |     |     | level DeepSeek-V3-0324 |     |     | achieves |     | the highest | coverage |     |
| --- | --- | --- | --- | --- | --- | --- | ---------------------- | --- | --- | -------- | --- | ----------- | -------- | --- |
recallandchunkprecisionbuttheloosestspans(tight-
ness10–15%,vs.27–36%forQwen3-235B),indicating
|     |     |     |     |     |     |     | wider predictions |     | that | cover | more | lines | but | localize |
| --- | --- | --- | --- | --- | --- | --- | ----------------- | --- | ---- | ----- | ---- | ----- | --- | -------- |
less precisely.
|     |     |     |     |     |     |     |     |     |     | At  | the | file level, | we  | report |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----------- | --- | ------ |
Metric definitions.
|     |     |     |     |     |     |     | Precision, | Recall,   |     | and | their harmonic |     | mean   | (F1-    |
| --- | --- | --- | --- | --- | --- | --- | ---------- | --------- | --- | --- | -------------- | --- | ------ | ------- |
|     |     |     |     |     |     |     | Score),    | alongside |     |     | Match,         | a   | binary | indica- |
Exact
|     |     |     |     |     |     |     | tor of perfect   |       | set equality, |       | and      | Set Accuracy, |              | the |
| --- | --- | --- | --- | --- | --- | --- | ---------------- | ----- | ------------- | ----- | -------- | ------------- | ------------ | --- |
|     |     |     |     |     |     |     | Jaccard          | index | (intersection |       | over     | union)        | of predicted |     |
|     |     |     |     |     |     |     | and ground-truth |       | file          | sets, | averaged | across        | instances.   |     |
12

SHERLOC:StructuredDiagnosticLocalizationforCodeRepairAgents
Table 3: Full evaluation across backbones and benchmarks. File-level, chunk-level, and
tool-engagement metrics on both SWE-Bench Lite and Verified; the engagement columns explain the
| recall gap | between | Qwen3-235B |     | and | DeepSeek-R1-0528. |            |     |             |     |     |            |     |     |
| ---------- | ------- | ---------- | --- | --- | ----------------- | ---------- | --- | ----------- | --- | --- | ---------- | --- | --- |
|            |         |            |     |     |                   | File-Level |     | Chunk-Level |     |     | Engagement |     |     |
Backbone Bench Recall Prec. F1 Exact Cov.Rec. Tight. Prec. Turns Zero-tool
76.33
Qwen3-30B-A3B-Thinking Lite ±2.00 74.59 75.15 73.00 25.53 22.96 31.13 7.4 0.1
79.67
DeepSeek-V3-0324 Lite 68.20 71.81 58.00 49.26 10.63 46.67 4.4 3.3
±2.03
75.78
DeepSeek-R1-0528 Lite 71.45 72.72 68.00 36.49 20.72 39.44 3.4 12.0
±1.35
84.33
Qwen3-235B-A22B-Thinking Lite 81.10 82.14 78.08 39.14 27.52 44.54 5.0 0.0
±0.72
75.07
Qwen3-30B-A3B-Thinking Verified 78.50 74.96 67.80 29.80 29.40 39.40 7.2 0
±1.24
79.53
DeepSeek-V3-0324 Verified 75.47 75.46 60.20 54.40 14.50 56.40 4.7 0
±0.47
73.63
DeepSeek-R1-0528 Verified 76.12 73.39 65.20 37.70 25.70 45.90 3.2 10
±1.59
81.27
Qwen3-235B-A22B-Thinking Verified 87.55 83.53 75.20 41.28 36.36 53.47 4.7 0
±1.16
At the chunk level, using a strict containment cri- Table 4: Failure taxonomy. Most localization
terion, measures the fraction of failures stem from selecting the wrong file after
|              | Coverage | Recall |                 |     |        |         |          |             |            |     |        |           |     |
| ------------ | -------- | ------ | --------------- | --- | ------ | ------- | -------- | ----------- | ---------- | --- | ------ | --------- | --- |
|              |          |        |                 |     |        |         | reaching | the correct | directory, |     | rather | than from |     |
| ground-truth |          | chunks | fully contained |     | within | predic- |          |             |            |     |        |           |     |
tions, Precision measures the fraction of predictions failing to search broadly enough.
thatcontainatleastoneground-truthchunk,andAv-
erage Tightness measures the ratio of ground-truth Failure Category 𝑛 %
| chunk size | to   | prediction | size   | for correctly |        | covered |           |       |              |       |       |     |       |
| ---------- | ---- | ---------- | ------ | ------------- | ------ | ------- | --------- | ----- | ------------ | ----- | ----- | --- | ----- |
|            |      |            |        |               |        |         | Reasoning | error | (saw correct | file, | wrong |     | 22 40 |
| chunks.    | Mean | turns      | is the | average       | number | of rea- |           |       |              |       |       |     |       |
selection)
| soning | turns | per trajectory, |     | and Zero-tool |     | is the |            |          |            |     |             |     |       |
| ------ | ----- | --------------- | --- | ------------- | --- | ------ | ---------- | -------- | ---------- | --- | ----------- | --- | ----- |
|        |       |                 |     |               |     |        | Close miss | (correct | directory, |     | wrong file) |     | 15 27 |
fractionoftrajectoriesthatproducelocationswithout
|     |     |     |     |     |     |     | Wrong module |     | entirely |     |     |     | 14 25 |
| --- | --- | --- | --- | --- | --- | --- | ------------ | --- | -------- | --- | --- | --- | ----- |
making any tool call. For SWE-Bench Lite, all Multi-file bug (3+ ground-truth files) 2 4
reported metrics are averaged over the same seeds Insufficient exploration 1 2
used in Figure 2. For SWE-Bench Verified, recall Ambiguous problem description 1 2
| is a multi-seed |         | mean (± | std)     | over 3 | seeds;   | remaining |                       |     |     |     |          |     |     |
| --------------- | ------- | ------- | -------- | ------ | -------- | --------- | --------------------- | --- | --- | --- | -------- | --- | --- |
| file/chunk      | metrics | are     | reported | on     | the seed | used in   |                       |     |     |     |          |     |     |
|                 |         |         |          |        |          |           | D. Implicit-Knowledge |     |     |     | Controls |     |     |
Section 4.4.
|     |     |     |     |     |     |     | Table 5 | reports | the controlled |     | degradation |     | study |
| --- | --- | --- | --- | --- | --- | --- | ------- | ------- | -------------- | --- | ----------- | --- | ----- |
C. Failure Taxonomy on Zero-Recall from Section 4.3. All rows use Qwen3-235B-A22B-
|     |     |     |     |     |     |     | Thinking | on SWE-Bench |     | Verified; |     | the top | section |
| --- | --- | --- | --- | --- | --- | --- | -------- | ------------ | --- | --------- | --- | ------- | ------- |
Instances
|     |     |     |     |     |     |     | is cumulative, |      | with each | row          | keeping | every          | restric- |
| --- | --- | --- | --- | --- | --- | --- | -------------- | ---- | --------- | ------------ | ------- | -------------- | -------- |
|     |     |     |     |     |     |     | tion from      | rows | above     | and removing |         | one additional |          |
TounderstandSHERLOC’slimitations,wemanually
categorize all 55 instances where the system achieves source of repository evidence. For the masked-paths
zero recall@1 on SWE-Bench Verified (Table 4). condition, we report two masking variants: masking
|              |     |         |      |              |       |        | explicit | Python | file paths, | and | additionally | masking |     |
| ------------ | --- | ------- | ---- | ------------ | ----- | ------ | -------- | ------ | ----------- | --- | ------------ | ------- | --- |
| The dominant |     | failure | mode | is reasoning | error | (40%): |          |        |             |     |              |         |     |
themodelexploredthecorrectarea,oftenviewingthe module and line references. Both yield the same re-
|              |     |           |            |          |     |             | call, indicating |     | that file | paths | alone carry | most | of the |
| ------------ | --- | --------- | ---------- | -------- | --- | ----------- | ---------------- | --- | --------- | ----- | ----------- | ---- | ------ |
| ground-truth |     | file, but | ultimately | selected |     | a different |                  |     |           |       |             |      |        |
file in its final answer. Combined with close misses issue-text leakage signal. The final row is a separate,
(27%,correctdirectorybutwrongfile),67%offailures non-cumulative control: only file paths in the issue
textaremasked,whilethefullSHERLOCisretained.
| stem frompicking |     | thewrong |     | file among | nearby | candi- |     |     |     |     |     |     |     |
| ---------------- | --- | -------- | --- | ---------- | ------ | ------ | --- | --- | --- | --- | --- | --- | --- |
dates rather than from failing to reach the right area. This isolates how much of SHERLOC’s recall comes
fromactiveexplorationaftertheobvioussurface-path
| Only 4% | involve | genuinely | multi-file |     | bugs | where the |     |     |     |     |     |     |     |
| ------- | ------- | --------- | ---------- | --- | ---- | --------- | --- | --- | --- | --- | --- | --- | --- |
ground truth spans 3+ files. By repository, failures leakage is removed (79.96%, only 1.3 pp below the
concentrate in matplotlib (21% failure rate), sympy unmaskedfullsystem),showingthattool-assistedrea-
|             |             |        |          |               |             |          | soning recovers |     | nearly | all of | the path-leakage |     | signal. |
| ----------- | ----------- | ------ | -------- | ------------- | ----------- | -------- | --------------- | --- | ------ | ------ | ---------------- | --- | ------- |
| (19%),      | and xarray  | (14%), |          | while django, |             | the most |                 |     |        |        |                  |     |         |
| represented | repository, |        | has      | a lower       | 11% failure | rate,    |                 |     |        |        |                  |     |         |
| consistent  | with        | higher | implicit | familiarity.  |             |          |                 |     |        |        |                  |     |         |
13

SHERLOC:StructuredDiagnosticLocalizationforCodeRepairAgents
| Table | 5: Implicit-knowledge |     |     | controls |     | on  |     |     |     |     |     |     |     |
| ----- | --------------------- | --- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
35000
| SWE-Bench                   |           | Verified |             |             |      |           |                |       |     |     |     |     |     |
| --------------------------- | --------- | -------- | ----------- | ----------- | ---- | --------- | -------------- | ----- | --- | --- | --- | --- | --- |
| (Qwen3-235B-A22B-Thinking). |           |          |             | Progressive |      | ablation: |                | 30000 |     |     |     |     |     |
| each                        | row keeps | every    | restriction | from        | rows | above and | snekot egarevA |       |     |     |     |     |     |
25000
| removes | one | additional | source | of repository |     | evidence. |     |     |     |     |     |     |     |
| ------- | --- | ---------- | ------ | ------------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
19,525
20000
| The      | final row | is a non-cumulative |            | masked-issue |             |           |     |       |     |     |     |     |     |
| -------- | --------- | ------------------- | ---------- | ------------ | ----------- | --------- | --- | ----- | --- | --- | --- | --- | --- |
| control: | tools     | and the             | repository | tree         | are         | retained, |     | 15000 |     |     |     |     |     |
| and only | file      | paths in            | the issue  | text         | are masked. | The       |     |       |     |     |     |     |     |
9,037
10000
| ≈22 | pp gap | between | this masked-issue |     | control |     |     |     |     |     |     |     |     |
| --- | ------ | ------- | ----------------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
4,542
| (79.96%) | and      | the heavily-masked |              | text-only |        | setting |     | 5000 |     |     |     |     |     |
| -------- | -------- | ------------------ | ------------ | --------- | ------ | ------- | --- | ---- | --- | --- | --- | --- | --- |
| (57.86%) | isolates | the                | contribution | of        | active |         |     | 0    |     |     |     |     |     |
repository exploration, since both endpoints have file LLM Tool Input
| paths    | masked | from the         | issue. | Δ is | the recall | drop |        |            |           |     |                |            |       |
| -------- | ------ | ---------------- | ------ | ---- | ---------- | ---- | ------ | ---------- | --------- | --- | -------------- | ---------- | ----- |
|          |        |                  |        |      |            |      | Figure | 9: Average | token     |     | usage          | by message | type. |
| relative | to     | the full system. |        |      |            |      |        |            |           |     |                |            |       |
|          |        |                  |        |      |            |      | LLM    | reasoning  | dominates |     | per-trajectory |            | token |
consumption.
| Setting(cumulative)                  |                       |     |     |     | Recall@1(%) | Δ           |     |     |     |     |     |     |              |
| ------------------------------------ | --------------------- | --- | --- | --- | ----------- | ----------- | --- | --- | --- | --- | --- | --- | ------------ |
| FullSHERLOC(tools+repotree+rawissue) |                       |     |     |     |             | 81.27 —     |     |     |     |     |     |     |              |
| −tools                               |                       |     |     |     |             | 68.28 −13.0 |     |     |     |     |     |     |              |
| −repotree                            |                       |     |     |     |             | 64.91 −16.4 |     |     |     |     |     |     |              |
|                                      | +maskfilepathsinissue |     |     |     |             | 57.86 −23.4 |     |     |     |     |     |     | Mean: 28,563 |
60
|                                 | +maskmodule/linerefs |     |     |     |     | 57.86 −23.4 |           |     |     |     |     |     |     |
| ------------------------------- | -------------------- | --- | --- | --- | --- | ----------- | --------- | --- | --- | --- | --- | --- | --- |
| Maskedissueonly(non-cumulative) |                      |     |     |     |     |             |           | 50  |     |     |     |     |     |
| FullSHERLOC+maskedissuepaths    |                      |     |     |     |     | 79.96 −1.3  | ycneuqerF |     |     |     |     |     |     |
40
30
| E.  | Per-Repository |        |     | Breakdown |     | of Im- |     |     |     |     |     |     |     |
| --- | -------------- | ------ | --- | --------- | --- | ------ | --- | --- | --- | --- | --- | --- | --- |
|     | plicit         | Recall |     |           |     |        |     | 20  |     |     |     |     |     |
10
| Table | 6 shows | file-level | recall | for one | masked | setting |     |     |     |     |     |     |     |
| ----- | ------- | ---------- | ------ | ------- | ------ | ------- | --- | --- | --- | --- | --- | --- | --- |
0
| brokendownbyrepository. |     |     | Popular,well-documented |     |     |     |     |     |               |        |                      |     |     |
| ----------------------- | --- | --- | ----------------------- | --- | --- | --- | --- | --- | ------------- | ------ | -------------------- | --- | --- |
|                         |     |     |                         |     |     |     |     | 0   | 20,000 40,000 | 60,000 | 80,000100,000120,000 |     |     |
projects (scikit-learn, requests) show substantially Total tokens per trajectory
| higher       | implicit | recall        | than less | common             | ones        | (pylint, |              |     |              |      |             |     |        |
| ------------ | -------- | ------------- | --------- | ------------------ | ----------- | -------- | ------------ | --- | ------------ | ---- | ----------- | --- | ------ |
|              |          |               |           |                    |             |          | Figure       | 10: | Total tokens | per  | trajectory. |     | The    |
| seaborn).    |          | This supports | the       | implicit-knowledge |             | in-      |              |     |              |      |             |     |        |
|              |          |               |           |                    |             |          | distribution |     | is compact,  | with | a mean      | of  | ≈28.6k |
| terpretation |          | from Table    | 5:        | model              | familiarity | with     |              |     |              |      |             |     |        |
tokens.
| repository  |                | APIs and error       | patterns |                | remains   | a strong   |          |            |                      |            |      |           |           |
| ----------- | -------------- | -------------------- | -------- | -------------- | --------- | ---------- | -------- | ---------- | -------------------- | ---------- | ---- | --------- | --------- |
| signal      | even           | after explicit       | file     | paths          | and       | repository |          |            |                      |            |      |           |           |
| identifiers | are            | masked.              |          |                |           |            |          |            |                      |            |      |           |           |
|             |                |                      |          |                |           |            | F.       | Token      | Composition          |            |      | of        | Localiza- |
| Table       | 6:             |                      |          |                | recall@1. | is         |          |            |                      |            |      |           |           |
|             | Per-repository |                      | implicit |                |           | 𝑁          |          | tion       | Trajectories         |            |      |           |           |
| the number  |                | of SWE-Bench         |          | Verified       | instances | per        |          |            |                      |            |      |           |           |
| repository. |                | Popular repositories |          | (scikit-learn, |           |            |          |            |                      |            |      |           |           |
|             |                |                      |          |                |           |            | To       | complement | the trajectory-level |            |      | results,  | we report |
| requests)   | exhibit        | substantially        |          | higher         | implicit  | recall     |          |            |                      |            |      |           |           |
|             |                |                      |          |                |           |            | detailed | token      | usage                | statistics | from | SHERLOC’s |           |
than less common ones (pylint, seaborn). reasoning traces on SWE-Bench Verified with
|     |     |     |     |     |     |     | Qwen3-235B-A22B-Thinking. |     |     |     | Figure | 9   | shows that |
| --- | --- | --- | --- | --- | --- | --- | ------------------------- | --- | --- | --- | ------ | --- | ---------- |
Repository 𝑁 Recall@1(%) the majority of tokens are consumed by the model’s
pallets/flask 1 100.0 reasoning process itself (19.5k tokens on average),
|     |                           |     |     |     |     |      | followed | by   | tool outputs | (9.0k) | and         | input | messages     |
| --- | ------------------------- | --- | --- | --- | --- | ---- | -------- | ---- | ------------ | ------ | ----------- | ----- | ------------ |
|     | psf/requests              |     |     | 8   |     | 87.5 |          |      |              |        |             |       |              |
|     |                           |     |     |     |     |      | (4.5k).  | This | indicates    | that   | computation |       | is dominated |
|     | scikit-learn/scikit-learn |     |     | 32  |     | 85.3 |          |      |              |        |             |       |              |
astropy/astropy 22 74.1 by internal deliberation rather than excessive tool
|     | pydata/xarray         |     |     | 22  |     | 66.7 | querying. |            |                    |        |                |            |           |
| --- | --------------------- | --- | --- | --- | --- | ---- | --------- | ---------- | ------------------ | ------ | -------------- | ---------- | --------- |
|     | django/django         |     |     | 231 |     | 64.0 |           |            |                    |        |                |            |           |
|     |                       |     |     |     |     |      | The       | total      | token distribution |        | per            | trajectory | (Fig-     |
|     | pytest-dev/pytest     |     |     | 19  |     | 57.1 |           |            |                    |        |                |            |           |
|     |                       |     |     |     |     |      | ure       | 10) is     | centered           | around | 28.6k          | tokens     | (median   |
|     | matplotlib/matplotlib |     |     | 34  |     | 55.0 |           |            |                    |        |                |            |           |
|     |                       |     |     |     |     |      | 24.0k),   | suggesting | a compact          |        | yet expressive |            | reasoning |
|     | sympy/sympy           |     |     | 75  |     | 51.9 |           |            |                    |        |                |            |           |
sphinx-doc/sphinx 44 49.1 process. These results confirm that SHERLOC’s
pylint-dev/pylint 10 33.3 trajectories remain computationally efficient while
|     | mwaskom/seaborn |     |     | 2   |     | 33.3 | capturing | detailed | reasoning      |     | traces.           |     |        |
| --- | --------------- | --- | --- | --- | --- | ---- | --------- | -------- | -------------- | --- | ----------------- | --- | ------ |
|     | Overall         |     |     | 500 |     | 60.7 |           |          |                |     |                   |     |        |
|     |                 |     |     |     |     |      |           |          |                |     | For completeness, |     | we in- |
|     |                 |     |     |     |     |      | Detailed  |          | Distributions. |     |                   |     |        |
14

SHERLOC:StructuredDiagnosticLocalizationforCodeRepairAgents
clude detailed violin plots (Figures 11 and 12) visu-
alizing the full distributions of token and turn usage
across problem difficulty levels. These figures com-
plement the trajectory statistics summarized in Sec-
tion 4.4 by highlighting the variance and spread of
trajectories beyond the mean and boxplot summaries.
120,000
100,000
80,000
60,000
40,000
20,000
0
<15 min fix 15 min - 1 hour 1-4 hours
(n=194) (n=261) (n=42)
Problem difficulty
snekot
latoT
Figure 11: Token distribution by problem
difficulty. Violin plot across easy, medium, and
hard SWE-Bench Verified instances.
14
12
10
8
6
4
2
0
<15 min fix 15 min - 1 hour 1-4 hours
(n=194) (n=261) (n=42)
Problem difficulty
snrut
fo
rebmuN
21.3k to 32.8k and 35.1k. Thus, most of the difficulty
effect appears as a shift from very short searches to
moderately longer, context-heavier searches rather
than as a large increase in the number of tool inter-
actions.
The scatter plots show the same story at instance
level. Difficulty has a positive but not determinis-
tic relationship with both turns (𝑟=0.208) and total
tokens (𝑟=0.292), so SHERLOC allocates more com-
pute to harder cases while still exhibiting substantial
within-bin variation. This variation is important:
some “easy” issues still produce long outliers above
80k tokens, and many 1–4 hour issues finish within
3–6 turns. In practice, the fixed difficulty label cap-
tures only part of localization cost; issue ambiguity,
repositorytopology,andthesizeofretrievedevidence
also affect how much reasoning the agent spends.
Finally, turns and tokens are strongly coupled
(𝑟=0.694), with an average slope of roughly 7.1k to-
kens per additional turn. The remaining vertical
spread at a fixed turn count indicates that token
cost is not merely a function of conversation length:
high-fanout files, broad dependency views, and long
snippets can make two trajectories with the same
number of turns differ substantially in total context
consumed. This supports the interpretation in Sec-
tion 4.4: SHERLOC’s efficiency comes from keeping
most trajectories compact, while still allowing longer,
evidence-rich searches when the problem demands
them.
H. Implementation Details
System Prompt. The system prompt instructs
the model to act as a bug-localization assistant, pro-
viding structured output via <think>, <tool_call>,
Figure 12: Turn distribution by problem and <locations> tags. The prompt emphasizes ex-
difficulty. Violin plot across easy, medium, and haustive exploration (“prefer over-inspecting code to
hard SWE-Bench Verified instances. missing a second edit site”) and prohibits code fixes.
The user message contains the problem statement
followed by the filtered repository tree.
G. Difficulty-Conditioned Trajec- Key instructions (abbreviated):
tory Cost
You are a bug-localization assistant.
Figures 13 to 20 expand the trajectory statistics sum-
Primary Goal: Locate every file and precise
marized in Section 4.4 with difficulty-conditioned dis-
line-number range that must be edited. Never
tributions,computedonSWE-BenchVerifiedwith
propose code changes. Return locations only
Qwen3-235B-A22B-Thinking. The central pattern is
afterinspectingenoughsourcecodetobecertain
adaptive but modest scaling: trajectories are short
you have found all of them.
overall (mean 4.7 turns, median 4), yet harder bench-
Interaction protocol: (1) Read the Problem
mark categories require measurably deeper searches.
Description. (2) First response must be a tool
Reasoning turns increase from 4.22 on the easiest is-
call, never locations. (3) Keep issuing tool calls
suesto5.05onmediumissuesand5.21onthehardest
until fully confident. (4) Only then reply with
issues, while total tokens increase more sharply from a <locations> block.
15

SHERLOC:StructuredDiagnosticLocalizationforCodeRepairAgents
| 0.4 |     |     | r = 0.208    |     |                         |     |
| --- | --- | --- | ------------ | --- | ----------------------- | --- |
|     |     |     | 14 p = 0.000 |     | <15 min fix (n=194)     |     |
|     |     | KDE |              |     | 15 min - 1 hour (n=261) |     |
Mean: 4.7
|     |     |             | snrut fo rebmuN 12 |     | 1-4 hours (n=42) |     |
| --- | --- | ----------- | ------------------ | --- | ---------------- | --- |
| 0.3 |     | Median: 4.0 |                    |     |                  |     |
|     |     |             | 10                 |     | Linear trend     |     |
ytisneD
8
0.2
6
4
0.1
2
0
0.0
|     |                 |       | <15 min fix |     | 15 min -           | 1-4 hours |
| --- | --------------- | ----- | ----------- | --- | ------------------ | --------- |
| 2 4 | 6 8 10          | 12 14 |             |     | 1 hour             |           |
|     | Number of turns |       |             |     | Problem difficulty |           |
Figure13: Turns per trajectory(mean4.8,median4). Figure14: Turns vs. difficulty(𝑟=0.206,𝑝<0.001).
| r = 0.283 |                         |     |         | Pearson r = 0.694         |     |     |
| --------- | ----------------------- | --- | ------- | ------------------------- | --- | --- |
| p = 0.000 | <15 min fix (n=194)     |     |         | slope = 7,042 tokens/turn |     |     |
| 120,000   | 15 min - 1 hour (n=261) |     | 120,000 |                           |     |     |
1-4 hours (n=42)
| snekot latoT 100,000 |              |     | 100,000      |     |     |     |
| -------------------- | ------------ | --- | ------------ | --- | --- | --- |
|                      | Linear trend |     | snekot latoT |     |     |     |
| 80,000               |              |     | 80,000       |     |     |     |
| 60,000               |              |     | 60,000       |     |     |     |
40,000
|     |     |     | 40,000 |     | <15 min fix (n=194) |     |
| --- | --- | --- | ------ | --- | ------------------- | --- |
15 min - 1 hour (n=261)
20,000
1-4 hours (n=42)
20,000
| 0           |                    |           |     |       | Trend (r=0.694) |       |
| ----------- | ------------------ | --------- | --- | ----- | --------------- | ----- |
| <15 min fix | 15 min -           | 1-4 hours | 0   |       |                 |       |
|             | 1 hour             |           |     | 0 2 4 | 6 8 10          | 12 14 |
|             | Problem difficulty |           |     |       | Number of turns |       |
Figure15: Tokens vs. difficulty(𝑟=0.281,𝑝<0.001). Figure16: Turns vs. tokens(𝑟=0.694;7.1ktokens/turn).
| 14 μ=4.22 | μ=5.05 | μ=5.21 |         | μ=21,323 | μ=32,797 | μ=35,148 |
| --------- | ------ | ------ | ------- | -------- | -------- | -------- |
| M=4       | M=5    | M=5    | 120,000 | M=17,269 | M=27,755 | M=30,805 |
snrut fo rebmuN 12
100,000
| 10  |     |     | snekot latoT |     |     |     |
| --- | --- | --- | ------------ | --- | --- | --- |
80,000
8
60,000
6
40,000
4
20,000
2
| 0   |     |     | 0   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- |
<15 min fix 15 min - 1 hour 1-4 hours <15 min fix 15 min - 1 hour 1-4 hours
| (n=194) | (n=261)            | (n=42) |     | (n=194) | (n=261)            | (n=42) |
| ------- | ------------------ | ------ | --- | ------- | ------------------ | ------ |
|         | Problem difficulty |        |     |         | Problem difficulty |        |
Figure17: Turn distribution by difficulty. Medians: 4,5, Figure18: Token distribution by difficulty. Medians:
| 5.                   |     | 17.3k,27.8k,30.8k. |        |     |     |     |
| -------------------- | --- | ------------------ | ------ | --- | --- | --- |
| snrut fo rebmun naeM |     |                    | 50,000 |     |     |     |
snekot latot naeM
| 6       | 5.05    | 5.21   |        |        |         |        |
| ------- | ------- | ------ | ------ | ------ | ------- | ------ |
|         | (n=261) | (n=42) | 40,000 |        | 32,797  | 35,148 |
| 4.22    |         |        |        |        |         | (n=42) |
| (n=194) |         |        |        |        | (n=261) |        |
| 4       |         |        | 30,000 | 21,323 |         |        |
(n=194)
20,000
2
10,000
| 0   |     |     | 0   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- |
<15 min fix 15 min - 1-4 hours <15 min fix 15 min - 1-4 hours
|     | 1 hour             |     |     |     | 1 hour             |     |
| --- | ------------------ | --- | --- | --- | ------------------ | --- |
|     | Problem difficulty |     |     |     | Problem difficulty |     |
Figure19: Mean turns by difficulty. Means: 4.22,5.05, Figure20: Mean tokens by difficulty. Means: 21.3k,
| 5.21. |     | 32.8k,35.1k. |     |     |     |     |
| ----- | --- | ------------ | --- | --- | --- | --- |
16

SHERLOC:StructuredDiagnosticLocalizationforCodeRepairAgents
Tool Descriptions. Four tools are described in ## Issue Description
natural language within the system prompt: {problem_statement}
## Ground Truth Patch (what actually fixed
• view_file: Inspects file contents, optionally re-
the issue)
stricted to a line range (view_range: [start,
{gt_patch}
end]). Includes dependency metadata showing
import relationships. ## Finding to Evaluate
• codebase_search: Repository-wide case- {finding}
insensitive literal search. Returns matching files
## Predicted Locations
with line numbers and 20-line context windows.
{locations}
• repo_tree: Displays the repository file structure
with per-file line counts. Rate the finding on these dimensions (1-5
scale):
• connected_tree: Shows import dependencies.
Witha fileargument,showsdirectimportsand 1. Root Cause Correctness (1=completely
reverse imports; without, shows repository-wide wrong, 5=perfectly identifies the root
import overview. cause): Does the finding correctly identify
WHY the bug occurs?
Final-Turn Prompt. Whentheremaininginterac- 2. Location Accuracy (1=wrong files,
5=exact files and line ranges): Do the
tion steps reach a threshold, the following instruction
predicted locations match the ground truth
is injected:
patch files?
You have reached the maximum number of tool 3. Solution Actionability (1=no useful
calls. You must now reply with <findings> guidance, 5=clear actionable fix approach):
and <locations> blocks. Does the solution idea provide enough
In <findings>, provide bullet points guidance to implement a fix?
explaining why each location needs
Respond in this exact JSON format:
modification, the root cause, and the
{"root_cause": <1-5>, "location_accuracy":
solution idea (without showing code). In
<1-5>, "solution_actionability": <1-5>,
<locations>, emit every file and line range
"reasoning": "<brief explanation>"}
that needs editing.
Prompts are generated for the 499 instances with
Self-Recovery Prompts. Loop detection: When SHERLOC findings. Judge calls use temperature
the system detects repeated identical tool calls, =0.1andmaximumoutputlength=300tokens, and
it injects a warning: “Loop detected! You the JSON scores are parsed into a composite score by
have attempted [tool] N times with the same averaging the 3 dimensions.
parameters. DO NOT repeat the same command.
Try a different approach.”
Responselengthmanagement: Ifaresponseexceeds Inference Parameters. All localization runs use
the safe token limit, the system re-prompts with: temperature =0.99 and maximum generation length
“Please be more concise: reduce your thinking =81,920tokens. Themaximumnumberofinteraction
to only the most essential analysis steps.” turnsis20. Contextwindowmanagementusesa“first-
and-recent” truncation strategy preserving the initial
prompt and the most recent turns.
Quality Judge Prompt. For the quality-gradient,
quality-filtered,andthreshold-sensitivityanalyses,we
use GPT-5.2 (openai/openai/gpt-5.2) as a ground-
Self-Recovery Mechanisms. SHERLOC in-
truth-patch-conditioned judge. Each judge call re-
cludes lightweight self-recovery mechanisms for com-
ceives the issue description, the ground-truth patch,
mon failure modes in multi-turn LLM tool use:
the SHERLOC finding, and the predicted locations.
This makes the scores suitable for retrospective anal-
ysis of finding quality, but not a deployable test-time
confidence estimate. The prompt template is: Context management. When the conversation
exceedsthecontextbudget,weusea“first-and-recent”
truncation strategy: the initial issue and repository
You are evaluating the quality of a bug
overview are preserved, as are the most recent turns,
localization analysis ("finding") for a
software issue. while older intermediate observations are dropped.
17

SHERLOC:StructuredDiagnosticLocalizationforCodeRepairAgents
Loopdetection. Theexecutortracksrepeatedtool detected by matching test_*, tests/, conftest.py,
calls and injects a warning when the model attempts *_test.py, reproduc*, repro_*, or repro.*.
unproductive cycles, prompting it to change strategy
rather than reread the same evidence.
• localize: SWE-Agent str_replace_editor view;
OpenHands read and browse; shell commands
matching ls, cat, head, tail, grep, rg, ripgrep,
Implicit tool-call recovery. If the model ex-
ag, find, tree, less, more, file, wc -l, nl,
presses a valid tool request but omits the canonical
column, stat, pwd, sed -n, xargs grep, or a
wrapper,theparserrecoverstheintendedactionwhen
bare cd PATH.
it can do so unambiguously. This prevents minor for-
• repair: source edits via SWE-Agent
matting errors from wasting a turn.
(str_replace_editor str_replace, insert,
create, undo_edit) or OpenHands (edit); shell
Response length management. If a generation sed -i ... on a non-test path.
approaches the safe output limit, the system re-
• make_test: the same edit/create operations, but
on a path matching the test/reproduction pat-
prompts the model to provide a shorter response
terns above.
so that the tool call or final answer is not lost to
truncation.
• run_test: shell commands containing pytest,
py.test, unittest, nosetests, tox, coverage
run; python ... invocations whose script name
Final-turn prompting. When the step budget is or inline code mentions reproduc* / repro_* /
nearly exhausted, SHERLOC injects an instruction test_* or imports something specifically (e.g.,
to stop exploring and synthesize the best available python -c "from foo import bar; ...").
diagnostic finding and location set. • prepare_env: pip install, conda install,
apt-get install,npm install,poetry install,
setup.py install/develop/build, source ...,
Code-Repair Analyses export ..., chmod, chown, which, env,
virtualenv, activate.
I. Agent Step Distribution Across • think: OpenHands-only think action; SWE-
Agent has no analogous action and contributes
Repair Backbones
zero here.
We analyze how our 5 repair-model backbones • finish: explicit submit (SWE-Agent) or finish
(OpenHands).
(Qwen3-Coder-30B-A3B, Qwen3-Coder-Next, Qwen3-
Next-80B-A3B-Instruct, MiniMax-M2.5, Qwen3-
• other: anything not matched by the rules above;
Coder-480B-A35B) distribute their interaction steps
inpracticemostlyrmcleanupofagent-createdre-
production scripts and unparsed bash one-liners.
across action purposes under both the SWE-Agent
and OpenHands repair frameworks at baseline (no
external findings injected), establishing what an un- Donut charts (Figure 21) report the base-
aidedrepair-agenttrajectoryspendsitsactionbudget line percentage breakdown of actions for each
on. model×framework cell.
Scope of Counted Actions. Each trajectory con- Baseline Action Distribution. Across all 10
tributestheactions the repair agent itself emitsinits (backbone, framework) cells, localize is consistently
baseline code-repair run on SWE-Bench Verified the largest labeled category, confirming the Section 1
(Figure 21). The Qwen3-Coder-30B-A3B + Open- framing that localization dominates the repair-agent
Hands baseline cell uses the all-SHERLOC-findings interaction budget. The absolute reduction in total
trajectories as a proxy. agent turns when SHERLOC findings are injected is
reported in Table 13.
Classifier rules. A rule-based classifier maps each
agent action to one of eight purposes. We classify the J. Finding Quality and Diagnostic
action type first, then for shell commands we strip a Context
leading cd PATH &&prefix(whenpresent)andclassify
theremainingcommand,sothatcd /testbed && pip Figure 7 in Section 4.6 shows the quality-bucketed
install -e . is correctly attributed to prepare_env resolve rates: “Very High” quality findings (≥4.0) re-
rather than navigation. Test/reproduction paths are solve at 75.9%, compared to 20.0% for “Low” quality,
18

SHERLOC:StructuredDiagnosticLocalizationforCodeRepairAgents
38
actions
)enilesab(
tnegA-EWS
Qwen3-Coder-30B Qwen3-Coder-NextQwen3-Next-80B-Instruct MiniMax-M2.5 Qwen3-Coder-480B
40 25 63 48
actions actions actions actions
46
actions
)enilesab(
sdnaHnepO
29 24 52 63
actions actions actions actions
Localize Repair Make test Run test Prepare env Think Finish Other
Figure 21: Baseline action-purpose distribution per repair-agent trajectory. Across the 5 backbones
and 2 frameworks, repair agents spend a substantial fraction of their actions on localize (gray) even before any
patch is attempted, supporting the Section 1 framing that localization dominates the repair-agent interaction
budget.
Table 7: Score distribution over the 499 judged findings with composite score ≥ 4.0) identifies the
SHERLOC findings on SWE-Bench Verified. subsetwherediagnosticcontextismostlikelytotrans-
Bucket boundaries match Figure 7. fer, while falling back to the agent’s own search on
harder or lower-confidence instances. A retrospective
Bucket Score range n % sensitivity analysis of this threshold is provided in
Low [1.0,2.0] 55 11.0 Appendix J.3.
Medium (2.0,3.0] 73 14.6
High (3.0,4.0] 101 20.2
VeryHigh (4.0,5.0] 270 54.1
J.1. Representative Findings Across Quality
Total 499 100.0
Levels
We first show 7 representative SHERLOC outputs
a gap exceeding 55 pp. The point-biserial correlation acrossthequalityspectrumtoillustratethefull5-field
between composite quality score and binary resolve finding format.
outcome is 𝑟 = 0.45 (𝑝 < 0.001, 𝑛=499), with solu- Toillustratethequalitygradient,wealsoshowhigh-
tionactionabilityasthestrongestindividualpredictor
and low-quality findings for representative instances.
(𝑟 =0.46).
These two lines of evidence (the code-repair inter-
vention grid and the per-instance quality analysis) High-quality SHERLOC finding (composite
underpin our main claim: diagnostic actionability, score 5.0/5.0). Instance: astropy__astropy-7166
not just file or function retrieval, is the operative (property docstrings not inherited).
unit of useful localization. When SHERLOC pro-
duces accurate root-cause analysis with actionable
Root cause: inspect.isfunction returns
solution guidance, the patching agent resolves issues
False for property objects, causing the
atratesapproachingtheoracleceiling; whentheanal- InheritDocstrings metaclass to skip docstring
ysis is inaccurate, the finding provides no advantage inheritance for properties despite them being
or actively misleads. A judge-based quality filter is valid docstring-bearing attributes.
therefore needed to prevent negative transfer from
Location: astropy/utils/misc.py:L531-L533
unreliable findings.
Solution idea: The condition should be ex-
This finding has a practical implication: repair
panded to recognize properties (and potentially
agents should not consume localization findings uni-
other descriptor types) while maintaining exist-
formly. A retrospective quality filter (keeping only ing behavior for functions/methods.
19

SHERLOC:StructuredDiagnosticLocalizationforCodeRepairAgents
Table 8: Representative SHERLOC findings across the quality spectrum. GT: ground-truth file
modified by the gold patch. Pred: file predicted by SHERLOC. Blue indicates a correct prediction, orange a
mismatch. Finding text is shown in sans-serif to mark it as illustrative example output.
| Instance |     |     | Locations |     |     | Finding |     |     |     |     |     |     |     | Score |
| -------- | --- | --- | --------- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | ----- |
django__django-14034 GT:django/forms/boundfield.py Locationexplanation: MultiValueField.clean()infields.pyappearstoshort-circuit 1.00
|     |     |     |       |                        |     | validationwhenallsubfieldvaluesareempty.                     |     |     |     | Rootcause:     | Thefindingclaimsthisskips |                      |        |     |
| --- | --- | --- | ----- | ---------------------- | --- | ------------------------------------------------------------ | --- | --- | --- | -------------- | ------------------------- | -------------------- | ------ | --- |
|     |     |     | Pred: | django/forms/fields.py |     |                                                              |     |     |     |                |                           |                      |        |     |
|     |     |     |       |                        |     | validationforrequiredsubfieldsunderrequire_all_fields=False. |     |     |     |                |                           | Solutionidea:        | Remove |     |
|     |     |     |       |                        |     | theempty-valueshortcutsorequiredsubfieldsarealwaysvalidated. |     |     |     |                |                           | Dependencies:        | The    |     |
|     |     |     |       |                        |     | proposedchangeislocalizedtoMultiValueField.                  |     |     |     | Testingimpact: |                           | Addtestsforpartially |        |     |
requiredsubfieldsinMultiValueField.
django__django-15554 GT:django/db/models/sql/query.py Locationexplanation: Join.equals()indatastructures.pyexcludesfiltered_relation 2.00
|     |     |     |       |                                        |     | fromequalitychecks.                           | Rootcause: | DistinctFilteredRelationjoinsonthesamepathcanbe |                |                                         |                             |     |     |     |
| --- | --- | --- | ----- | -------------------------------------- | --- | --------------------------------------------- | ---------- | ----------------------------------------------- | -------------- | --------------------------------------- | --------------------------- | --- | --- | --- |
|     |     |     | Pred: | django/db/models/sql/datastructures.py |     |                                               |            |                                                 |                |                                         |                             |     |     |     |
|     |     |     |       |                                        |     | deduplicateddespitehavingdifferentconditions. |            |                                                 |                | Solutionidea:                           | Comparethefulljoinidentity, |     |     |     |
|     |     |     |       |                                        |     | includingfiltered_relation.                   |            | Dependencies:                                   |                | Thisaffectscorejoindeduplicationandmust |                             |     |     |     |
|     |     |     |       |                                        |     | preserveexistingjoinoptimizationbehavior.     |            |                                                 | Testingimpact: |                                         | Addtestsformultiple         |     |     |     |
FilteredRelationinstancesonthesamepath.
pydata__xarray-4687 GT:xarray/core/computation.py Locationexplanation: xr.whereincomputation.pyfailstopreserveattributesbecauseits 4.33
|     |     |     |       |                            |     | apply_ufunccalllackskeep_attrs=True. |                                                     |                                                 | Rootcause:                               | xarraydefaultstodroppingattributes |     |     |     |     |
| --- | --- | --- | ----- | -------------------------- | --- | ------------------------------------ | --------------------------------------------------- | ----------------------------------------------- | ---------------------------------------- | ---------------------------------- | --- | --- | --- | --- |
|     |     |     | Pred: | xarray/core/computation.py |     |                                      |                                                     |                                                 |                                          |                                    |     |     |     |     |
|     |     |     |       |                            |     | duringthisoperation.                 | Solutionidea:                                       |                                                 | Addkeep_attrs=Truetotheapply_ufunccallin |                                    |     |     |     |     |
|     |     |     |       |                            |     | where(). Dependencies:               | ThechangeshouldpropagatethroughbothDataset.whereand |                                                 |                                          |                                    |     |     |     |     |
|     |     |     |       |                            |     | DataArray.where.                     | Testingimpact:                                      | Addtestsintests/test_computation.pyforattribute |                                          |                                    |     |     |     |     |
preservation.
django__django-13028 GT:django/db/models/sql/query.py Locationexplanation: check_filterableinquery.pychecksfilterableonmodelinstances, 4.67
Pred: django/db/models/sql/query.py notonlyqueryexpressions. Rootcause: Amodelfieldnamedfilterable=Falseismistaken
|     |     |     |     |     |     | fortheexpressioncapabilityflag,triggeringNotSupportedError. |     |     |     |                | Solutionidea:  |                       | Validate |     |
| --- | --- | --- | --- | --- | --- | ----------------------------------------------------------- | --- | --- | --- | -------------- | -------------- | --------------------- | -------- | --- |
|     |     |     |     |     |     | filterableonlyforactualqueryexpressions.                    |     |     |     | Dependencies:  | Addtherelevant |                       |          |     |
|     |     |     |     |     |     | expression-typeimportandupdatethechecklogic.                |     |     |     | Testingimpact: |                | Addregressiontestsfor |          |     |
filtersovermodelswithafilterablefield.
sympy__sympy-19637 GT:sympy/core/sympify.py Locationexplanation: sympy/core/sympify.pyreferenceskernoutsidetheblockwhereitis 4.67
Pred: sympy/core/sympify.py defined. Rootcause: hit = kern in sisoutsidetheif ’ ’ in sblock,soinputswithout
|     |     |     |     |     |     | spacesleavekernundefined. |                                                      | Solutionidea: | Movetheassignmentinsidetheconditionalblock. |     |     |     |                |     |
| --- | --- | --- | --- | --- | --- | ------------------------- | ---------------------------------------------------- | ------------- | ------------------------------------------- | --- | --- | --- | -------------- | --- |
|     |     |     |     |     |     | Dependencies:             | NootherfilesarerequiredbecausekernSisself-contained. |               |                                             |     |     |     | Testingimpact: |     |
Addtestsforspacelessinputssuchas(2*x)/(x-1).
matplotlib__matplotlib-20488 GT:lib/matplotlib/image.py Locationexplanation: image.pyadjustss_vminonlywhenitisnegative,butlogarithmic 5.00
Pred: lib/matplotlib/image.py normalizationrequiresvmin > 0. Rootcause: Zero-valueddatacanleaves_vminatzero,
|     |     |     |     |     |     | producingnon-finitelog-scalevaluesandaninvalidvmin/vmaxerror. |                            |     |     |               |                | Solutionidea:          | Adjust    |     |
| --- | --- | --- | --- | --- | --- | ------------------------------------------------------------- | -------------------------- | --- | --- | ------------- | -------------- | ---------------------- | --------- | --- |
|     |     |     |     |     |     | s_vminwhenitis<=                                              | 0,notonlywhenitisnegative. |     |     | Dependencies: |                | OtherLogNormvalidation |           |     |
|     |     |     |     |     |     | alreadymasksnon-positivevalues,sothechangeislocalized.        |                            |     |     |               | Testingimpact: |                        | Updatethe |     |
huge-rangelog-scaletesttocoverzero-valueboundaries.
psf__requests-2317 GT:requests/sessions.py Locationexplanation: sessions.pynormalizesHTTPmethodswithbuiltin_str(method), 5.00
|     |     |     |       |                      |     | whichconvertsbytestringsintoliteralstringslike"b’GET’".                |     |     |     |     | Rootcause: | InPython3, |          |     |
| --- | --- | --- | ----- | -------------------- | --- | ---------------------------------------------------------------------- | --- | --- | --- | --- | ---------- | ---------- | -------- | --- |
|     |     |     | Pred: | requests/sessions.py |     |                                                                        |     |     |     |     |            |            |          |     |
|     |     |     |       |                      |     | str(bytes)producesadebugrepresentationratherthandecodingthemethodname. |     |     |     |     |            |            | Solution |     |
idea: Replacebuiltin_strwithproperbyte-to-textdecoding,e.g.,to_native_string.
|     |     |     |     |     |     | Dependencies:            | Theissueisisolatedtomethodnormalizationbeforeuppercasingandrequest |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------------------------ | ------------------------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     | dispatch. Testingimpact: | Addrequesttestsforbyte-stringHTTPmethods.                          |     |     |     |     |     |     |     |
Outcome: Resolved. The finding precisely identifies Outcome: Not resolved. The actual fix
the root cause and the exact lines that need modifi- was in django/db/models/sql/query.py, adjusting
|     | cation.     |           |         |                              |                      |            | Query.output_field, |           |          | a completely |        | different  | root       |     |
| --- | ----------- | --------- | ------- | ---------------------------- | -------------------- | ---------- | ------------------- | --------- | -------- | ------------ | ------ | ---------- | ---------- | --- |
|     |             |           |         |                              |                      |            | cause and           | location. |          |              |        |            |            |     |
|     | Low-quality |           | SHERLOC |                              | finding              | (composite |                     |           |          |              |        |            |            |     |
|     |             | 1.0/5.0). |         | Instance:                    |                      |            | J.2. Ablating       |           | Finding  | Components   |        |            |            |     |
|     | score       |           |         |                              | django__django-12663 |            |                     |           |          |              |        |            |            |     |
|     | (nested     | subquery  |         | annotations).                |                      |            |                     |           |          |              |        |            |            |     |
|     |             |           |         |                              |                      |            | SHERLOC             | outputs   |          | more than    | file   | names:     | each find- |     |
|     |             |           |         |                              |                      |            | ing contains        | a         | location | explanation, |        | root-cause | anal-      |     |
|     |             |           |         |                              |                      |            | ysis, solution      |           | idea,    | dependency   | notes, | and        | testing    |     |
|     |             | Root      | cause:  | In Lookup.get_prep_lookup(), |                      |            |                     |           |          |              |        |            |            |     |
there is no special handling for LazyObject- impact. To isolate which parts of this diagnostic
derivedtypes. ThecodeassumesallRHSvalues object matter, we construct reduced finding splits
|     |     | are either | expressions | or  | direct values | ready for |          |      |            |     |         |     |             |     |
| --- | --- | ---------- | ----------- | --- | ------------- | --------- | -------- | ---- | ---------- | --- | ------- | --- | ----------- | --- |
|     |     |            |             |     |               |           | from the | same | Qwen3-235B |     | SHERLOC |     | predictions |     |
get_prep_value.
|     |     |                          |                                  |       |           |             | used in                        | the code-repair |         | experiments. |          | The        | component |     |
| --- | --- | ------------------------ | -------------------------------- | ----- | --------- | ----------- | ------------------------------ | --------------- | ------- | ------------ | -------- | ---------- | --------- | --- |
|     |     |                          |                                  |       |           |             | runs use                       | SWE-Bench       |         | Verified,    |          | OpenHands, | and       |     |
|     |     | Location:                | django/db/models/lookups.py:L14, |       |           |             |                                |                 |         |              |          |            |           |     |
|     |     | L70-L75                  |                                  |       |           |             | Qwen3-Coder-480B-A35B-Instruct |                 |         |              |          | under      | the same  |     |
|     |     |                          |                                  |       |           |             | repair-agent                   |                 | prompt  | and          | decoding | settings   | as the    |     |
|     |     | Solution                 |                                  | idea: |           | Modify      |                                |                 |         |              |          |            |           |     |
|     |     |                          |                                  |       |           |             | 480B OpenHands                 |                 |         | intervention | runs.    | The        | reduced   |     |
|     |     | Lookup.get_prep_lookup() |                                  |       | to        | detect      |                                |                 |         |              |          |            |           |     |
|     |     |                          |                                  |       |           |             | splits are                     | generated       | by      | retaining    | selected | bullets    | from      |     |
|     |     | LazyObject               | instances                        |       | and force | their eval- |                                |                 |         |              |          |            |           |     |
|     |     |                          |                                  |       |           |             | each SHERLOC                   |                 | finding | while        | leaving  | the        | predicted |     |
uation.
20

SHERLOC:StructuredDiagnosticLocalizationforCodeRepairAgents
locations unchanged. Thus, every non-baseline com- not helpful. As the threshold rises, accepted-instance
ponent row supplies the same SHERLOC file/line resolve increases monotonically from 59.1% to 83.1%,
locations; only the textual diagnostic fields vary. So- showing that high-scoring findings are much more
keeps only the solution-idea bullet. likely to help. The 4.0 threshold used for the actual
| lution idea | only |     |     |     |     |     |     |     |     |     |     |     |     |
| ----------- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Location explanation + root cause keeps the location quality-filtered intervention is a pre-specified high-
explanation and root-cause bullets. Location explana- quality operating point that still covers a majority of
|        |            |     |          |      | keeps | all 3, while | the benchmark |     | (317/500 | instances). |     | The | 4.5 row has |
| ------ | ---------- | --- | -------- | ---- | ----- | ------------ | ------------- | --- | -------- | ----------- | --- | --- | ----------- |
| tion + | root cause | +   | solution | idea |       |              |               |     |          |             |     |     |             |
excluding dependency notes and testing impact. The the best filtered estimate in hindsight, but it accepts
quality-filtered reference row is different: it injects fewer than half the benchmark and was not run as
thefull5-fieldfindingandlocationsonlyforinstances a separate intervention; we therefore use it only as
with composite judge score ≥ 4.0, and falls back to sensitivity evidence, not as the reported code-repair
| the baseline | prompt |     | with | no locations |     | or findings | result. |     |     |     |     |     |     |
| ------------ | ------ | --- | ---- | ------------ | --- | ----------- | ------- | --- | --- | --- | --- | --- | --- |
otherwise.
| Table          | 9   | shows      | that | for      | Qwen3-Coder-30B- |               |         |             |     |     |              |     |     |
| -------------- | --- | ---------- | ---- | -------- | ---------------- | ------------- | ------- | ----------- | --- | --- | ------------ | --- | --- |
|                |     |            |      |          |                  |               | K. Full | Code-Repair |     |     | Resolve-Rate |     |     |
| A3B/SWE-Agent, |     | actionable |      | solution |                  | guidance car- |         |             |     |     |              |     |     |
Grid
| ries marginally |     | more | signal | than | the other | fields: the |     |     |     |     |     |     |     |
| --------------- | --- | ---- | ------ | ---- | --------- | ----------- | --- | --- | --- | --- | --- | --- | --- |
solution-idea-onlyvariantoutperformsthebaselineby
|                               |              |                          |              |                   |            |               | Table 11     | gives      | the exact  | resolve-rate  |           | grid      | visualized   |
| ----------------------------- | ------------ | ------------------------ | ------------ | ----------------- | ---------- | ------------- | ------------ | ---------- | ---------- | ------------- | --------- | --------- | ------------ |
| 6.5 pp,                       | while        | the location-explanation |              |                   |            | + root-cause- |              |            |            |               |           |           |              |
|                               |              |                          |              |                   |            |               | in Figure    | 3: every   | cell       | is a          | SWE-Bench |           | Verified     |
| only variant                  | gives        | a                        | slightly     | smaller           | gain       | (+6.1 pp).    |              |            |            |               |           |           |              |
|                               |              |                          |              |                   |            |               | resolve      | rate (%)   | over       | 500 instances |           | for one   | (backbone,   |
| Combininglocationexplanation, |              |                          |              |                   | rootcause, | andsolu-      |              |            |            |               |           |           |              |
|                               |              |                          |              |                   |            |               | framework,   | condition) |            | triple.       | Table     | 12        | mirrors the  |
| tion idea                     | (i.e.        | removing                 | only         | dependencies      |            | + testing     |              |            |            |               |           |           |              |
|                               |              |                          |              |                   |            |               | same grid    | but        | injects    | the weaker    |           | Qwen3-30B | SHER-        |
| impact)                       | is strongest |                          | among        | the               | reduced    | textual vari- |              |            |            |               |           |           |              |
|                               |              |                          |              |                   |            |               | LOC findings |            | instead,   | isolating     | how       | localizer | quality      |
| ants at                       | +7.3         | pp. The                  | full-finding |                   | references | show          |              |            |            |               |           |           |              |
|                               |              |                          |              |                   |            |               | propagates   | to         | downstream |               | resolve   | rate.     |              |
| that adding                   | every        | field                    | is           | not automatically |            | better        |              |            |            |               |           |           |              |
|                               |              |                          |              |                   |            |               | Four         | patterns   | stand      | out           | in Table  | 11.       | (i) The best |
| for this                      | strong       | repair                   | model:       | auxiliary         |            | dependency    |              |            |            |               |           |           |              |
and testing-impact notes can add context, but the of All / QF SHERLOC exceeds Baseline in ev-
maintransferablesignalistheeditdirectioncaptured ery one of the 10 backbone×framework cells (mean
by the solution idea, with all reduced variants land- +5.95 pp), confirming the RQ2 transfer claim. (ii)
ing within 1.8–3.2 pp of full SHERLOC (+9.3 pp). The best intervention depends on backbone capabil-
ity: weakermodels(Qwen3-Coder-30B,Qwen3-Coder-
| This motivates |     | the downstream |     |     | framing: | localization |     |     |     |     |     |     |     |
| -------------- | --- | -------------- | --- | --- | -------- | ------------ | --- | --- | --- | --- | --- | --- | --- |
should be evaluated not only as file retrieval, but Next,Qwen3-Next-80B-A3B-Instruct)gainmostfrom
as diagnostic context whose actionable content can (up to +11.8 pp), while strong lo-
All SHERLOC
change a repair agent’s trajectory. calizers (MiniMax-M2.5, Qwen3-Coder-480B-A35B)
|     |     |     |     |     |     |     | require | quality | filtering | to    | avoid       | negative | transfer: |
| --- | --- | --- | --- | --- | --- | --- | ------- | ------- | --------- | ----- | ----------- | -------- | --------- |
|     |     |     |     |     |     |     | MiniMax | loses   | 4–5 pp    | under | All SHERLOC |          | but re-   |
J.3. Quality-Filter Threshold Sensitivity covers +2.2 pp / +0.6 pp under QF SHERLOC. (iii)
TheShuffledcontroldegradesresolveratein9ofthe
| The quality-filtered                   |              |              | analysis      | in        | Section      | 4.6 uses      | a                     |               |           |              |               |              |               |
| -------------------------------------- | ------------ | ------------ | ------------- | --------- | ------------ | ------------- | --------------------- | ------------- | --------- | ------------ | ------------- | ------------ | ------------- |
|                                        |              |              |               |           |              |               | 10 cells,             | confirming    |           | that gains   | come          | from         | instance-     |
| fixed composite                        |              | threshold    |               | of 4.0    | to decide    | whether       |                       |               |           |              |               |              |               |
|                                        |              |              |               |           |              |               | relevant              | diagnostic    | context   |              | rather        | than         | from merely   |
| an SHERLOC                             |              | finding      | should        | be        | shown        | to the repair |                       |               |           |              |               |              |               |
|                                        |              |              |               |           |              |               | having                | structured    | text      | in the       | prompt.       | (iv)         | The           |
| agent.                                 | Table 10     | asks         | whether       | this      | threshold    | is mean-      |                       |               |           |              |               |              | Ora-          |
|                                        |              |              |               |           |              |               | cle GPT-5.2           |               | column    | (64.6–89.2%) |               | shows        | substantial   |
| ingful or                              | arbitrary.   | It           | is a post-hoc |           | selection    | analysis,     |                       |               |           |              |               |              |               |
|                                        |              |              |               |           |              |               | remaining             | headroom      |           | above        | All           | / QF         | SHERLOC       |
| notanewcode-repairrunateverythreshold: |              |              |               |           |              | foreach       |                       |               |           |              |               |              |               |
|                                        |              |              |               |           |              |               | (47.8–76.6%),         |               | leaving   | room         | to improve    |              | the localizer |
| threshold,                             | we           | accept       | only          | findings  | whose        | GPT-5.2       |                       |               |           |              |               |              |               |
|                                        |              |              |               |           |              |               | toward                | a patch-aware |           | ceiling.     |               |              |               |
| composite                              | quality      | score        | meets         | the       | threshold,   | measure       |                       |               |           |              |               |              |               |
| the observed                           | full-SHERLOC |              |               | resolve   | rate         | on that ac-   |                       |               |           |              |               |              |               |
| cepted                                 | subset,      | and estimate |               | the       | remaining    | instances     |                       |               |           |              |               |              |               |
|                                        |              |              |               |           |              |               | L. Localization-Phase |               |           |              |               | Compute      |               |
| as falling                             | back         | to the       | 61.6%         | baseline. |              | The analysis  |                       |               |           |              |               |              |               |
|                                        |              |              |               |           |              |               | Cost                  | for           | Repair    |              | Agents        |              |               |
| therefore                              | tests        | 2 properties |               | of        | this filter: | whether       |                       |               |           |              |               |              |               |
| higher                                 | judged       | finding      | quality       | selects   | instances    | where         |                       |               |           |              |               |              |               |
|                                        |              |              |               |           |              |               | Table 13              | reports       | the       | per-instance |               | cost of      | the localiza- |
| diagnostic                             | context      | transfers    |               | better,   | and          | how much      |                       |               |           |              |               |              |               |
|                                        |              |              |               |           |              |               | tion sub-phase        |               | of issue  | resolution   |               | on SWE-Bench |               |
| coverage                               | is lost      | as the       | threshold     |           | becomes      | stricter.     |                       |               |           |              |               |              |               |
|                                        |              |              |               |           |              |               | Verified              | for           | SWE-Agent |              | and OpenHands |              | across        |
The key reading is that the judge score is a useful the 5 repair models, with and without SHERLOC
selection signal. At low thresholds, the accepted set findings, alongside the cost of the standalone SHER-
is large but resolves at roughly the baseline rate, so LOC localizer that produces those findings. The lo-
passing almost every finding to the repair agent is calization phase is defined as the prefix of the agent’s
21

SHERLOC:StructuredDiagnosticLocalizationforCodeRepairAgents
Table 9: Component decomposition of SHERLOC findings on SWE-Bench Verified (SWE-Agent
framework). Except for the baseline and quality-filtered rows, all rows receive the same predicted SHERLOC
locations for every instance; only the retained textual finding fields differ. The bold “Full SHERLOC” row is
the canonical reference from Table 11; indented “w/o ...” rows are cumulative ablations, with parenthesized
values giving absolute-point deltas from Full SHERLOC. Deeper indentation removes additional fields (e.g.
the 2-indent rows further ablate the Loc + Root cause + Sol idea variant by dropping either Sol idea or both
Loc and Root cause). Evaluable(n) is the number of instances where the variant injects at least one
non-empty bullet; Strict(n) is the stricter subset where the injected bullet set exactly matches the variant’s
intent.
Model Intervention Resolved(%) Evaluable(n) Strict(n)
Baseline (no findings, no locations) 44.7 500 500
Full SHERLOC (all 5 fields) 54.0 500 500
w/o Dependencies and Testing 52.0 (-2.0) 494 482
Qwen3-Coder-30B-A3B
impact
w/o Solution idea 50.8 (-3.2) 490 482
w/o Location and Root cause 51.2 (-2.8) 494 494
Quality-filtered SHERLOC (≥4.0) 52.2 (-1.8) 500 500
Baseline (no findings, no locations) 74.4 500 500
Full SHERLOC (all 5 fields) 70.4 500 500
w/o Dependencies and Testing 68.8 (-1.6) 494 482
MiniMax-M2.5
impact
w/o Solution idea 72.0 (+1.6) 490 482
w/o Location and Root cause 72.2 (+1.8) 494 494
Quality-filtered SHERLOC (≥4.0) 76.6 (+6.2) 500 500
Table 10: Quality-threshold sweep on the LOC findings instructs the model to (𝑖) orient itself
predicted findings. SWE-Bench Verified / in the repository (working directory, version, layout),
OpenHands / Qwen3-Coder-480B-A35B-Instruct (𝑖𝑖) read and verify the source file(s) named in the
setting. We sweep the GPT-5.2 composite score findings, (𝑖𝑖𝑖) locate and inspect the relevant existing
required to accept a full SHERLOC finding. tests, and (𝑖𝑣) write a reproduction script before ap-
Accepted(n) is the number of instances passing the plying any source-level fix. All of these steps appear
threshold; Coverage(%) is Accepted / 500. Pass inthelocalizationphaseandarereportedbythetable;
resolved(%) is the observed resolve rate among only the actual repair edits and post-edit iterations
accepted instances; Overall resolved(%) combines fall outside it.
accepted full-SHERLOC outcomes with a 61.6%
baseline fallback for rejected instances (a Input tokens are tokens sent to the model on each
call (system prompt plus the full prior conversation,
retrospective estimate, not a separately run
intervention). Higher thresholds select more reliable including tool outputs returned in earlier turns); out-
findings at the cost of coverage; the same trend is put tokens are tokens emitted by the model on each
call (assistant text, reasoning, and the function name
plotted in Figure 8.
plus arguments of any emitted tool call). Tool out-
puts themselves are only counted on the input side of
Threshold Accepted(n) Coverage(%) Passresolved(%) Overallresolved(%)
2.0 455 91.0 59.1 59.3 the next call. Localization total is the sum of local-
2 3 . . 5 0 3 4 9 1 5 9 7 8 9 3 . . 0 8 6 6 2 1 . . 8 6 6 6 1 2 . . 6 5 ization input and output; full-run input/output are
3.5 352 70.4 67.6 65.8
4.0 317 63.4 71.3 67.7 the same metrics summed over the entire interaction
4.5 230 46.0 79.6 69.9
5.0 177 35.4 83.1 69.2 (localizationplusrepair). Resolved istheSWE-Bench
official resolve rate, included to show that compute
reductions from SHERLOC are visible even when
interaction trace that precedes its first edit action of resolve rate is comparable: stronger repair models
any kind. thatalreadysolveahighfractionofinstancesontheir
own can still benefit on the cost axis.
We emphasize that this prefix measures everything
theagentdoesbeforeitstartsediting,andthatthisis
not the same as “unconstrained search from scratch”
once findings are injected. Inspection of the traces Per-Backbone Cost-Accuracy Trends. For
shows that the standard agent prompt under SHER- Qwen3-Coder-30B-A3B, SHERLOC improves both
22

SHERLOC:StructuredDiagnosticLocalizationforCodeRepairAgents
Table 11: Full issue-resolution results on SWE-Bench Verified. Values are resolve rates (%);
SHERLOC finding rows use Qwen3-235B-A22B-Thinking findings. Each cell reports the completed run(s);
| missing artifacts | are | marked | “–”. |     |     |     |     |     |     |     |     |     |
| ----------------- | --- | ------ | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Model Framework Baseline Masked Shuffled All SHERLOC QF SHERLOC Oracle GPT-5.2
|     |     |     | SWE-Agent |     | 44.7 | 45.4 | 40.2 |     | 54.0 |     | 52.2 | 76.0 |
| --- | --- | --- | --------- | --- | ---- | ---- | ---- | --- | ---- | --- | ---- | ---- |
Qwen3-Coder-30B-A3B
|                  |     |     | OpenHands |     | 49.4 | 46.0 | 40.2 |     | 53.0 |     | 52.4 | 73.4 |
| ---------------- | --- | --- | --------- | --- | ---- | ---- | ---- | --- | ---- | --- | ---- | ---- |
| Qwen3-Coder-Next |     |     | SWE-Agent |     | 45.2 | 41.2 | 43.2 |     | 53.2 |     | 52.0 | 64.6 |
|                  |     |     | OpenHands |     | 44.6 | 44.6 | 39.2 |     | 53.2 |     | 54.6 | 68.4 |
|                  |     |     | SWE-Agent |     | 38.8 | 41.6 | 33.8 |     | 49.4 |     | 50.6 | 71.0 |
Qwen3-Next-80B-A3B-Instruct OpenHands 38.6 38.2 39.2 50.4 47.8 68.4
|     |     |     | SWE-Agent |     | 74.4 | 74.5 | 61.0 |     | 70.4 |     | 76.6 | 89.2 |
| --- | --- | --- | --------- | --- | ---- | ---- | ---- | --- | ---- | --- | ---- | ---- |
MiniMax-M2.5
|     |     |     | OpenHands |     | 72.2 | 71.8 | 64.0 |     | 67.2 |     | 72.8 | 87.8 |
| --- | --- | --- | --------- | --- | ---- | ---- | ---- | --- | ---- | --- | ---- | ---- |
|     |     |     | SWE-Agent |     | 63.0 | 61.8 | 58.6 |     | 63.0 |     | 64.0 | 86.2 |
Qwen3-Coder-480B-A35B
|     |     |     | OpenHands |     | 61.6 | 62.8 | 57.8 |     | 62.6 |     | 62.8 | 82.6 |
| --- | --- | --- | --------- | --- | ---- | ---- | ---- | --- | ---- | --- | ---- | ---- |
Table 12: Issue-resolution results with findings from the weaker Qwen3-30B SHERLOC.
Baseline, Masked, Shuffled, and GPT-5.2 columns are the same completed runs as Table 11; only
Oracle
All SHERLOC reflects the 30B-produced findings. QF-SHERLOC is omitted because the 30B findings
were not quality-scored. Values are resolve rates (%); bold marks the best score among Baseline, Masked,
| Shuffled, | and All | SHERLOC | (Oracle |     | excluded). |     |     |     |     |     |     |     |
| --------- | ------- | ------- | ------- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- |
Model Framework Baseline Masked Shuffled All SHERLOC Oracle GPT-5.2
|     |     |     | SWE-Agent |     |     | 44.7 | 45.4 | 40.2 |     |     | 43.8 | 76.0 |
| --- | --- | --- | --------- | --- | --- | ---- | ---- | ---- | --- | --- | ---- | ---- |
Qwen3-Coder-30B-A3B
|     |     |     | OpenHands |     |     | 49.4 | 46.0 | 40.2 |     |     | 42.2 | 73.4 |
| --- | --- | --- | --------- | --- | --- | ---- | ---- | ---- | --- | --- | ---- | ---- |
|     |     |     | SWE-Agent |     |     | 45.2 | 41.2 | 43.2 |     |     | 49.2 | 64.6 |
Qwen3-Coder-Next
|     |     |     | OpenHands |     |     | 44.6 | 44.6 | 39.2 |     |     | 45.4 | 68.4 |
| --- | --- | --- | --------- | --- | --- | ---- | ---- | ---- | --- | --- | ---- | ---- |
efficiency and accuracy: paired with SWE-Agent, saving device rather than an accuracy-improving one.
the effective localization total falls from 101.8k to Qwen3-Next-80B-A3B-Instruct sits between the 30B
65.8k tokens while resolve rate increases from 44.7% and 480B regimes and behaves like the 30B case:
to 54.0%; paired with OpenHands, localization total SHERLOC lowers localization total tokens (161.4k
falls from 361.1k to 234.1k tokens while resolve rate to 32.9k with SWE-Agent; 181.6k to 105.2k with
increases from 49.4% to 53.0%. For MiniMax-M2.5, a OpenHands), lowers full-run token totals (−48.4%
muchstrongerrepairmodel,thepictureseparatescost with SWE-Agent after adding the localizer cost;
from accuracy: SHERLOC lowers localization cost −33.0% with OpenHands), and increases resolve
substantially (116.3k to 105.6k with SWE-Agent; rateby10–12ppin bothframeworks(38.8%to 49.4%
428.3k to 293.5k with OpenHands) and lowers full- and 38.6% to 50.4%). Like the 30B model, this is a
run token totals, even though resolve rate decreases regime where predicted findings are simultaneously
by about 4 to 5 points. Thus, predicted diagnos- cost-saving and accuracy-improving, even though the
tic context can be useful as a compute-saving de- localization phase already runs at a relatively low
vice even when it is not accuracy-improving for a turn count (9.2–9.6 turns at baseline).
| strong model. | Qwen3-Coder-Next |               |         | behaves |        | like the |       |             |     |          |                 |     |
| ------------- | ---------------- | ------------- | ------- | ------- | ------ | -------- | ----- | ----------- | --- | -------- | --------------- | --- |
| 30B/80B       | mid-tier         | cases:        | SHERLOC |         | lowers | local-   |       |             |     |          |                 |     |
| ization total | tokens           | substantially |         | (1598k  | to     | 1059k    |       |             |     |          |                 |     |
|               |                  |               |         |         |        |          | Patch | Production: |     | No-Patch | and Apply-Fail- |     |
withSWE-Agent;1145kto727kwithOpenHands) The no-patch and apply-failure rates
|                    |          |                          |         |          |           |          | ure Rates.      |           |                                |           |                |        |
| ------------------ | -------- | ------------------------ | ------- | -------- | --------- | -------- | --------------- | --------- | ------------------------------ | --------- | -------------- | ------ |
| and lifts resolve  | rate     | (45.2%                   | to      | 53.2%    | and 44.6% | to       |                 |           |                                |           |                |        |
|                    |          |                          |         |          |           |          | from the        | completed | runs                           | reinforce | the efficiency | inter- |
| 53.2%), while      | full-run | token                    | totals  | stay     | close     | to base- |                 |           |                                |           |                |        |
|                    |          |                          |         |          |           |          | pretationabove. |           | ForQwen3-Coder-Next/OpenHands, |           |                |        |
| line(−7.3%/+1.4%). |          | TheQwen3-Coder-480B-A35B |         |          |           |          |                 |           |                                |           |                |        |
|                    |          |                          |         |          |           |          | the baseline    |           | has 26.6%                      | no-patch  | and 27.0%      | apply- |
| row partially      | mirrors  | the                      | MiniMax | pattern: |           | SHER-    |                 |           |                                |           |                |        |
failurerates;withall-SHERLOCfindingsthesefallto
LOC lowers localization total tokens substantially in 16.2% and 16.6%, respectively, paralleling the resolve-
| bothframeworks(188.9kto64.6kwith |             |               |     |         | SWE-Agent;  |       |            |       |             |         |              |          |
| -------------------------------- | ----------- | ------------- | --- | ------- | ----------- | ----- | ---------- | ----- | ----------- | ------- | ------------ | -------- |
|                                  |             |               |     |         |             |       | rate lift. | For   | strong      | models, | no-patch and | apply-   |
| 472.8k to                        | 324.6k with | OpenHands)    |     | and     | lowers      | full- |            |       |             |         |              |          |
|                                  |             |               |     |         |             |       | failure    | rates | are already | low,    | so the main  | measured |
| run token                        | totals,     | while resolve |     | rate is | essentially | flat  |            |       |             |         |              |          |
effectremainssearchandtokencostratherthanpatch
| (0.0pp SWE-Agent, |     | +1.0pp | OpenHands). |     |     | At this |             |     |          |       |                  |      |
| ----------------- | --- | ------ | ----------- | --- | --- | ------- | ----------- | --- | -------- | ----- | ---------------- | ---- |
|                   |     |        |             |     |     |         | production. |     | Table 14 | shows | the same pattern | with |
modelscale,SHERLOCagainbehavesasacompute- the smaller Qwen3-30B localizer: localization-phase
23

SHERLOC:StructuredDiagnosticLocalizationforCodeRepairAgents
Table 13: Localization-phase and full-run costs with and without SHERLOC findings.
Per-instance means over 500 SWE-Bench Verified tasks; the localization phase is the trace prefix before
the first source-edit action. The “Total pipeline” row adds the standalone-localizer cost (top of table) to the
agent’s own interaction cost with the findings. Δ reports percentage change from baseline for cost columns
| and percentage-point        |                    | change      | for resolve | rate. |                |     |         |         |           |         |              |                |
| --------------------------- | ------------------ | ----------- | ----------- | ----- | -------------- | --- | ------- | ------- | --------- | ------- | ------------ | -------------- |
| Setting                     |                    |             |             |       |                |     | Loc.    | Loc.    | Loc.      | Loc.    | Full-run     | Resolved       |
|                             |                    |             |             |       |                |     | turns   | input   | output    | total   | total        |                |
| Standalone                  | localizer          |             |             |       |                |     |         |         |           |         |              |                |
| SHERLOC(Qwen3-235B)         |                    |             |             |       |                |     | 4.7     | 9.0k    | 19.5k     | 28.6k   |              | – –            |
| Qwen3-Coder-30B-A3B         |                    | / SWE-Agent |             |       |                |     |         |         |           |         |              |                |
| Baseline                    |                    |             |             |       |                |     | 12.3    | 100.5k  | 1.3k      | 101.8k  |              | 622.4k 44.7%   |
| Total pipeline              |                    |             |             |       |                |     | 10.5    | 45.4k   | 20.4k     | 65.8k   | 433.6k       | 54.0%          |
| Δvsbaseline                 |                    |             |             |       |                |     | -14.6%  | -54.8%  | +1474.9%  | -35.4%  |              | -30.3% +9.3pp  |
| Qwen3-Coder-30B-A3B         |                    | / OpenHands |             |       |                |     |         |         |           |         |              |                |
| Baseline                    |                    |             |             |       |                |     | 21.6    | 358.3k  | 2.8k      | 361.1k  | 1630.5k      | 49.4%          |
| Total pipeline              |                    |             |             |       |                |     | 17.7    | 212.7k  | 21.3k     | 234.1k  | 1299.4k      | 53.0%          |
| Δvsbaseline                 |                    |             |             |       |                |     | -18.1%  | -40.6%  | +658.7%   | -35.2%  |              | -20.3% +3.6pp  |
| Qwen3-Coder-Next            |                    | / SWE-Agent |             |       |                |     |         |         |           |         |              |                |
| Baseline                    |                    |             |             |       |                |     | 53.3    | 1592.5k | 5.6k      | 1598.1k | 3025.9k      | 45.2%          |
| Total pipeline              |                    |             |             |       |                |     | 45.7    | 1034.9k | 24.0k     | 1058.9k | 2805.6k      | 53.2%          |
| Δvsbaseline                 |                    |             |             |       |                |     | -14.3%  | -35.0%  | +324.5%   | -33.7%  |              | -7.3% +8.0pp   |
| Qwen3-Coder-Next            |                    | / OpenHands |             |       |                |     |         |         |           |         |              |                |
| Baseline                    |                    |             |             |       |                |     | 40.5    | 1140.8k | 4.6k      | 1145.4k | 3221.4k      | 44.6%          |
| Total pipeline              |                    |             |             |       |                |     | 33.0    | 703.9k  | 22.7k     | 726.6k  | 3267.8k      | 53.2%          |
| Δvsbaseline                 |                    |             |             |       |                |     | -18.5%  | -38.3%  | +394.5%   | -36.6%  |              | +1.4% +8.6pp   |
| Qwen3-Next-80B-A3B-Instruct |                    |             | / SWE-Agent |       |                |     |         |         |           |         |              |                |
| Baseline                    |                    |             |             |       |                |     | 9.2     | 160.0k  | 1.4k      | 161.4k  |              | 617.0k 38.8%   |
| Total pipeline              |                    |             |             |       |                |     | 8.6     | 41.4k   | 20.1k     | 61.5k   | 318.3k       | 49.4%          |
| Δvsbaseline                 |                    |             |             |       |                |     | -6.5%   | -74.1%  | +1373.0%  | -61.9%  |              | -48.4% +10.6pp |
| Qwen3-Next-80B-A3B-Instruct |                    |             | / OpenHands |       |                |     |         |         |           |         |              |                |
| Baseline                    |                    |             |             |       |                |     | 9.6     | 179.6k  | 2.0k      | 181.6k  |              | 626.8k 38.6%   |
| Total pipeline              |                    |             |             |       |                |     | 10.9    | 112.4k  | 21.4k     | 133.8k  | 420.1k       | 50.4%          |
| Δvsbaseline                 |                    |             |             |       |                |     | +13.5%  | -37.4%  | +965.4%   | -26.3%  |              | -33.0% +11.8pp |
| MiniMax-M2.5                |                    | / SWE-Agent |             |       |                |     |         |         |           |         |              |                |
| Baseline                    |                    |             |             |       |                |     | 11.3    | 114.3k  | 2.0k      | 116.3k  | 1556.3k      | 74.4%          |
| Total pipeline              |                    |             |             |       |                |     | 12.5    | 84.8k   | 20.8k     | 105.6k  | 1206.1k      | 70.4%          |
| Δvsbaseline                 |                    |             |             |       |                |     | +10.6%  | -25.8%  | +918.5%   | -9.2%   |              | -22.5% -4.0pp  |
| MiniMax-M2.5                |                    | / OpenHands |             |       |                |     |         |         |           |         |              |                |
| Baseline                    |                    |             |             |       |                |     | 22.1    | 423.7k  | 4.6k      | 428.3k  | 1591.3k      | 72.2%          |
| Total pipeline              |                    |             |             |       |                |     | 19.1    | 270.8k  | 22.6k     | 293.5k  | 1395.0k      | 67.2%          |
| Δvsbaseline                 |                    |             |             |       |                |     | -13.6%  | -36.1%  | +394.3%   | -31.5%  |              | -12.3% -5.0pp  |
| Qwen3-Coder-480B-A35B       |                    | / SWE-Agent |             |       |                |     |         |         |           |         |              |                |
| Baseline                    |                    |             |             |       |                |     | 15.2    | 187.6k  | 1.3k      | 188.9k  | 1157.0k      | 63.0%          |
| Total pipeline              |                    |             |             |       |                |     | 10.8    | 44.5k   | 20.0k     | 64.6k   | 596.5k       | 63.0%          |
| Δvsbaseline                 |                    |             |             |       |                |     | -28.9%  | -76.3%  | +1408.8%  | -65.8%  |              | -48.4% +0.0pp  |
| Qwen3-Coder-480B-A35B       |                    | / OpenHands |             |       |                |     |         |         |           |         |              |                |
| Baseline                    |                    |             |             |       |                |     | 24.5    | 470.0k  | 2.8k      | 472.8k  | 2067.5k      | 61.6%          |
| Total pipeline              |                    |             |             |       |                |     | 21.4    | 303.0k  | 21.6k     | 324.6k  | 1862.9k      | 62.6%          |
| Δvsbaseline                 |                    |             |             |       |                |     | -12.7%  | -35.5%  | +669.5%   | -31.3%  |              | -9.9% +1.0pp   |
| Table                       | 14:                |             |             |       |                |     |         |         | findings. |         | Per-instance | means          |
|                             | Localization-phase |             | efficiency  |       | with Qwen3-30B |     | SHERLOC |         |           |         |              |                |
over 500 SWE-Bench Verified tasks for repair runs that receive findings produced by
Qwen3-30B-A3B-Thinking. “Qwen3-30B total” columns add the standalone Qwen3-30B SHERLOC localizer
cost (7.2 turns; 10.9k input + 35.1k output = 46.0k total tokens) to the repair-agent run. Resolve rates are
| shown | as baseline | → with Qwen3-30B |          | SHERLOC   |          | findings. |          |           |          |      |          |     |
| ----- | ----------- | ---------------- | -------- | --------- | -------- | --------- | -------- | --------- | -------- | ---- | -------- | --- |
|       |             |                  | Baseline | Qwen3-30B |          | Δ         | Baseline | Qwen3-30B |          | Δ    |          |     |
| Model |             | Framework        |          |           |          |           |          |           |          |      | Resolved |     |
|       |             |                  | loc.     | tok       | loc. tok | loc.      | full tok |           | full tok | full |          |     |
Qwen3-Coder-30B-A3B SWE-Agent 101.8k 85.4k −16.1% 622.4k 574.4k −7.7% 44.7%→43.8%
OpenHands 361.1k 246.5k −31.7% 1630.5k 1351.8k −17.1% 49.4%→42.2%
SWE-Agent 1598.1k 1224.6k −23.4% 3025.9k 2888.2k −4.6% 45.2%→49.2%
Qwen3-Coder-Next OpenHands 1145.4k 840.5k −26.6% 3221.4k 3197.9k −0.7% 44.6%→45.4%
24

SHERLOC:StructuredDiagnosticLocalizationforCodeRepairAgents
tokens decrease in every measured cell.
M. Token Cost Under the Masked-
Description Control
Table 15 checks whether masking repository/file
hints in the problem statement makes repair agents
spend more tokens on localization. Across completed
baseline–masked pairs, the effect is mostly small and
mixed: with the exception of the Qwen3-Coder-480B-
A35B/SWE-Agent outlier (+23.0%), localization-
token deltas range from −12.0% to +10.9%. Thus,
masking problem-statement identifiers generally does
notforcesubstantiallymorelocalizationeffort;agents
largely follow similar exploration routines, or infer
structure from the remaining context.
N. File-Level Localization: Baseline
vs. SHERLOC
For each SWE-Bench Verified instance we extract
theimplicitlocalizationoutputofbaselineandmasked
agentruns,i.e.,thesetofexisting source files thatthe
agent actually modifies in its model patch, excluding
agent-created reproduction, debug, or test scripts
(any hunk introducing a new file is filtered out by
checking for new file mode or — /dev/null). We
compare these file sets to SHERLOC’s predicted
files and to the gold patch files. Table 16 reports the
full per-instance file-level localization breakdown that
complements the compute and resolve-rate view in
Table 13: Hit@1, macro precision/recall, and macro
F1overall500tasks. Instanceswheretheagentnever
touches an existing source file contribute zero, so the
metric jointly rewards correct file selection and the
willingness to commit to one.
Reading. Table 13 reports compute and resolve
rate; this table provides the matched file-level
localization-metric breakdown. SHERLOC dom-
inates baseline/masked agent localization for the
weakermodels, whileMiniMax-M2.5alreadylocalizes
near saturation. Masked (≈ baseline) values across
rows indicate that masking file/repo identifiers in the
problem statement is not a strong contamination con-
trol here: capable agents recover localization quality
withoutthosehints. Table17isolatestheQwen3-30B
localizer used for the smaller-finding runs: it is less
accurate than Qwen3-235B SHERLOC, but remains
stronger than the baseline localization traces for the
weaker repair-agent settings.
25

SHERLOC:StructuredDiagnosticLocalizationforCodeRepairAgents
Table 15: Baseline vs. masked-description token cost. “Loc.” is the localization phase (the prefix of the
trajectory before the first source-edit action). Per-instance means; deltas are masked relative to baseline.
Model Framework Loc. turns Loc. tokens Δloc. tok Full-runtokens Δfulltok Resolved
SWE-Agent 12.3→12.8 101.8k→111.4k +9.4% 622.4k→997.4k +60.2% 44.7%→45.4%
Qwen3-Coder-30B-A3B OpenHands 21.6→21.7 361.1k→368.2k +2.0% 1630.5k→1644.9k +0.9% 49.4%→46.0%
Qwen3-Coder-Next SWE-Agent 53.3→52.7 1598.1k→1599.8k +0.1% 3025.9k→2871.4k -5.1% 45.2%→41.2%
OpenHands 40.5→40.4 1145.4k→1131.1k -1.2% 3221.4k→3125.6k -3.0% 44.6%→44.6%
Qwen3-Next-80B-A3B-Instruct SWE-Agent 9.2→9.0 161.4k→142.1k -12.0% 617.0k→607.1k -1.6% 38.8%→41.6%
OpenHands 9.6→9.9 181.6k→190.9k +5.1% 626.8k→697.9k +11.3% 38.6%→38.2%
MiniMax-M2.5 SWE-Agent 11.3→12.3 116.3k→129.0k +10.9% 1556.3k→1642.7k +5.6% 74.4%→74.5%
OpenHands 22.1→22.5 428.3k→437.7k +2.2% 1591.3k→1586.6k -0.3% 72.2%→71.8%
SWE-Agent 15.2→16.1 188.9k→232.4k +23.0% 1157.0k→1269.0k +9.7% 63.0%→61.8%
Qwen3-Coder-480B-A35B
OpenHands 24.5→24.6 472.8k→470.5k -0.5% 2067.5k→2066.1k -0.1% 61.6%→62.8%
| Table | 16:                     |         |              |     | Verified. | SHERLOC’s | predicted | files vs. the |
| ----- | ----------------------- | ------- | ------------ | --- | --------- | --------- | --------- | ------------- |
|       | File-level localization | quality | on SWE-Bench |     |           |           |           |               |
existing-source files modified by baseline and masked agent runs; higher is better. Evaluable(n) is the
number of instances where the method emits at least one file (SHERLOC predicts files for almost all
instances; baseline/masked counts equal the rate at which the agent commits a real source edit). Hit@1,
Recall, Precision, and F1 are per-instance means over all 500 instances, with non-evaluable instances
| contributing | zero. |     |     |     |     |     |     |     |
| ------------ | ----- | --- | --- | --- | --- | --- | --- | --- |
Model Framework Method Hit@1 Recall Precision F1 Evaluable(n)
Qwen3-235B-A22B-Thinking SHERLOC 0.884 0.813 0.876 0.835 498 / 500
|     |     |     | Baseline | 0.772 | 0.730 | 0.763 | 0.734 | 437 / 500 |
| --- | --- | --- | -------- | ----- | ----- | ----- | ----- | --------- |
SWE-Agent
|     |     |     | Masked | 0.788 | 0.735 | 0.781 | 0.743 | 457 / 500 |
| --- | --- | --- | ------ | ----- | ----- | ----- | ----- | --------- |
Qwen3-Coder-30B-A3B
|     |     |     | Baseline | 0.752 | 0.759 | 0.748 | 0.730 | 461 / 500 |
| --- | --- | --- | -------- | ----- | ----- | ----- | ----- | --------- |
OpenHands
|     |     |           | Masked   | 0.734 | 0.738 | 0.725 | 0.708 | 456 / 500 |
| --- | --- | --------- | -------- | ----- | ----- | ----- | ----- | --------- |
|     |     |           | Baseline | 0.562 | 0.553 | 0.551 | 0.542 | 305 / 500 |
|     |     | SWE-Agent | Masked   | 0.494 | 0.483 | 0.485 | 0.474 | 271 / 500 |
Qwen3-Coder-Next
|     |     |     | Baseline | 0.562 | 0.584 | 0.543 | 0.547 | 357 / 500 |
| --- | --- | --- | -------- | ----- | ----- | ----- | ----- | --------- |
OpenHands
|     |     |     | Masked   | 0.562 | 0.573 | 0.540 | 0.538 | 350 / 500 |
| --- | --- | --- | -------- | ----- | ----- | ----- | ----- | --------- |
|     |     |     | Baseline | 0.760 | 0.721 | 0.761 | 0.728 | 441 / 500 |
SWE-Agent
|     |     |     | Masked | 0.766 | 0.726 | 0.766 | 0.731 | 447 / 500 |
| --- | --- | --- | ------ | ----- | ----- | ----- | ----- | --------- |
Qwen3-Next-80B-A3B-Instruct
|     |     |     | Baseline | 0.752 | 0.776 | 0.752 | 0.738 | 480 / 500 |
| --- | --- | --- | -------- | ----- | ----- | ----- | ----- | --------- |
OpenHands
|     |     |     | Masked   | 0.744 | 0.775 | 0.734 | 0.731 | 479 / 500 |
| --- | --- | --- | -------- | ----- | ----- | ----- | ----- | --------- |
|     |     |     | Baseline | 0.896 | 0.864 | 0.888 | 0.863 | 489 / 500 |
SWE-Agent
|     |     |     | Masked | 0.886 | 0.848 | 0.880 | 0.851 | 461 / 500 |
| --- | --- | --- | ------ | ----- | ----- | ----- | ----- | --------- |
MiniMax-M2.5
|     |     | OpenHands | Baseline | 0.824 | 0.846 | 0.818 | 0.809 | 493 / 500 |
| --- | --- | --------- | -------- | ----- | ----- | ----- | ----- | --------- |
|     |     |           | Masked   | 0.834 | 0.855 | 0.823 | 0.816 | 487 / 500 |
|     |     |           | Baseline | 0.868 | 0.834 | 0.844 | 0.821 | 491 / 500 |
SWE-Agent
|     |     |     | Masked | 0.862 | 0.833 | 0.839 | 0.818 | 488 / 500 |
| --- | --- | --- | ------ | ----- | ----- | ----- | ----- | --------- |
Qwen3-Coder-480B-A35B
|     |     |     | Baseline | 0.816 | 0.837 | 0.773 | 0.776 | 490 / 500 |
| --- | --- | --- | -------- | ----- | ----- | ----- | ----- | --------- |
OpenHands
|     |     |     | Masked | 0.812 | 0.837 | 0.785 | 0.785 | 490 / 500 |
| --- | --- | --- | ------ | ----- | ----- | ----- | ----- | --------- |
Table 17: Standalone Qwen3-30B SHERLOC localization vs. baseline repair-agent traces. The
injected-finding repair runs in Table 14 do not receive a separate localization score; their findings are supplied
| by the | standalone SHERLOC | row. |     |     |     |     |     |     |
| ------ | ------------------ | ---- | --- | --- | --- | --- | --- | --- |
Model Framework Method Hit@1 Recall Precision F1 Evaluable(n)
SHERLOC
| Qwen3-30B-A3B-Thinking |     |           |          | 0.786 | 0.751 | 0.785 | 0.750 | 497 / 500 |
| ---------------------- | --- | --------- | -------- | ----- | ----- | ----- | ----- | --------- |
|                        |     | SWE-Agent | Baseline | 0.772 | 0.730 | 0.763 | 0.734 | 437 / 500 |
Qwen3-Coder-30B-A3B
|     |     | OpenHands | Baseline | 0.752 | 0.759 | 0.748 | 0.730 | 461 / 500 |
| --- | --- | --------- | -------- | ----- | ----- | ----- | ----- | --------- |
|     |     | SWE-Agent | Baseline | 0.562 | 0.553 | 0.551 | 0.542 | 305 / 500 |
Qwen3-Coder-Next
|     |     | OpenHands | Baseline | 0.562 | 0.584 | 0.543 | 0.547 | 357 / 500 |
| --- | --- | --------- | -------- | ----- | ----- | ----- | ----- | --------- |
26
