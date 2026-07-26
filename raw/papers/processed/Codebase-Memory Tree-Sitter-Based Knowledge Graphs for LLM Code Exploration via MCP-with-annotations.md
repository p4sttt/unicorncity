|     | Codebase-Memory: |     |     |     |      | Tree-Sitter-Based |             |     |     | Knowledge |     | Graphs |     |     |     |
| --- | ---------------- | --- | --- | --- | ---- | ----------------- | ----------- | --- | --- | --------- | --- | ------ | --- | --- | --- |
|     |                  |     | for | LLM | Code |                   | Exploration |     |     | via MCP   |     |        |     |     |     |
Martin Vogel 1, Falk Meyer-Eschenbach 2,3,4, Severin Kohler 5,6,
|     |     |     |     | Elias | Grünewald |     | 2,  | and Felix | Balzer | 2   |     |     |     |     |     |
| --- | --- | --- | --- | ----- | --------- | --- | --- | --------- | ------ | --- | --- | --- | --- | --- | --- |
1Independent
|     |     |     |     |     |     | Researcher, |     | Berlin, |     | Germany |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ----------- | --- | ------- | --- | ------- | --- | --- | --- | --- | --- |
2Institute of Medical Informatics, Charité – Universitätsmedizin Berlin, Berlin, Germany
3Clinical Study Center, Berlin Institute of Health, Berlin, Germany
|     |     | 4Institute |     | of Informatics, |     | Humboldt |     | University, |     | Berlin, | Germany |     |     |     |     |
| --- | --- | ---------- | --- | --------------- | --- | -------- | --- | ----------- | --- | ------- | ------- | --- | --- | --- | --- |
6202 raM 82  ]ES.sc[  1v77272.3062:viXra 5Institute
|     |     |     |     | of Informatics, |     | Freie | Universität |     | Berlin, | Berlin, | Germany |     |     |     |     |
| --- | --- | --- | --- | --------------- | --- | ----- | ----------- | --- | ------- | ------- | ------- | --- | --- | --- | --- |
6Health Data Science Unit, University Hospital Heidelberg, Heidelberg, Germany
Abstract pact analysis. Text-based search cannot capture transi-
tiverelationshipswithoutiterativelyfollowingreferences,
| Large | Language | Model | (LLM) | coding |     | agents | typi- |                |     |           |            |     |        |              |     |
| ----- | -------- | ----- | ----- | ------ | --- | ------ | ----- | -------------- | --- | --------- | ---------- | --- | ------ | ------------ | --- |
|       |          |       |       |        |     |        |       | each iteration |     | consuming | additional |     | tokens | and increas- |     |
cally explore codebases through repeated file-reading ingtheriskoflostcontext[5]. Recentempiricalanalyses
and grep-searching, consuming thousands of tokens per confirm that input tokens dominate the cost of agentic
| query | without | structural | understanding. |     |     | We present |     |        |        |           |         |      |     |     |     |
| ----- | ------- | ---------- | -------------- | --- | --- | ---------- | --- | ------ | ------ | --------- | ------- | ---- | --- | --- | --- |
|       |         |            |                |     |     |            |     | coding | tasks, | even with | caching | [6]. |     |     |     |
Codebase-Memory, an open-source system that con- Recent work on coding agents [7–9] has focused
| structs | a persistent, | Tree-Sitter-based |     |     | knowledge | graph |     |              |     |                   |     |        |            |     |     |
| ------- | ------------- | ----------------- | --- | --- | --------- | ----- | --- | ------------ | --- | ----------------- | --- | ------ | ---------- | --- | --- |
|         |               |                   |     |     |           |       |     | on improving |     | agent strategies, |     | better | prompting, |     | hi- |
via the Model Context Protocol (MCP), parsing 66 erarchical localization, or fault-localization heuristics,
languages through a multi-phase pipeline with parallel while leaving the underlying code retrieval mechanism
| worker | pools, | call-graph | traversal, | impact | analysis, |     | and |         |            |               |     |             |     |      |      |
| ------ | ------ | ---------- | ---------- | ------ | --------- | --- | --- | ------- | ---------- | ------------- | --- | ----------- | --- | ---- | ---- |
|        |        |            |            |        |           |     |     | largely | unchanged. | Concurrently, |     | graph-based |     | code | rep- |
community discovery [1]. Evaluated across 31 real-world resentations such as Code Property Graphs [10] and
| repositories, |     | Codebase-Memory |     | achieves |     | 83% answer |     |        |      |             |          |     |            |          |     |
| ------------- | --- | --------------- | --- | -------- | --- | ---------- | --- | ------ | ---- | ----------- | -------- | --- | ---------- | -------- | --- |
|               |     |                 |     |          |     |            |     | CodeQL | [11] | have proven | powerful |     | for static | analysis |     |
quality versus 92% for a file-exploration agent, at ten but remain heavyweight, requiring specialized databases
times fewer tokens and 2.1 times fewer tool calls. For and query languages not optimized for LLM consump-
| graph-native |     | queries such | as  | hub detection |     | and caller |     |       |          |      |                     |     |     |           |     |
| ------------ | --- | ------------ | --- | ------------- | --- | ---------- | --- | ----- | -------- | ---- | ------------------- | --- | --- | --------- | --- |
|              |     |              |     |               |     |            |     | tion. | Emerging | work | on repository-aware |     |     | knowledge |     |
ranking, it matches or exceeds the explorer on 19 of 31 graphs [12] and graph-enhanced retrieval agents [13]
languages. demonstrates the growing interest in structural code
|     |     |     |     |     |     |     |     | representations |         | for LLM | agents,         | though | these | systems |         |
| --- | --- | --- | --- | --- | --- | --- | --- | --------------- | ------- | ------- | --------------- | ------ | ----- | ------- | ------- |
|     |     |     |     |     |     |     |     | typically       | require | complex | infrastructure. |        |       | The     | cost of |
1 Introduction
|     |     |     |     |     |     |     |     | this inefficiency |     | is concrete: |     | production |     | agentic | work- |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------------- | --- | ------------ | --- | ---------- | --- | ------- | ----- |
The emergence of LLM-based coding agents, such as loads report per-task LLM API costs of several dollars
Claude Code [2], Cursor, and Aider [3], has transformed on non-trivial repositories [6, 7]. The recent emergence
software development by enabling natural-language- of the Model Context Protocol (MCP) [2] as an open
driven code exploration, bug fixing, and refactoring. standard for connecting LLM agents to external tools
| These | agents | interact with | codebases |     | through | tool | calls, |     |     |     |     |     |     |     |     |
| ----- | ------ | ------------- | --------- | --- | ------- | ---- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
presentsanopportunitytoexposestructuralcodequeries
reading files, searching for patterns, and listing direc- as lightweight, agent-native tools—yet no existing solu-
tory contents. While effective for small-scale tasks, this tion exploits this to combine structural query capability
text-based exploration strategy scales poorly. A typi- with zero-infrastructure deployment.
cal codebase exploration session requires dozens of tool Tobridgethisgap,weproposetreatingcodebasestruc-
| calls, consuming |     | hundreds | of  | thousands | of tokens | before |     |         |                |           |     |           |       |         |     |
| ---------------- | --- | -------- | --- | --------- | --------- | ------ | --- | ------- | -------------- | --------- | --- | --------- | ----- | ------- | --- |
|                  |     |          |     |           |           |        |     | ture as | a first-class, | queryable |     | knowledge | graph | exposed |     |
the agent develops sufficient understanding to answer a directly to LLM agents via lightweight structural tools
structuralquestionsuchas“WhatbreaksifIchangethis rather than raw file content. We instantiate this in
function?” [4]. our implementation Codebase-Memory, which parses
This inefficiency stems from a fundamental mismatch: codebases using Tree-Sitter [14], stores the resulting
| LLM | agents | operate | on unstructured |     | text, | yet | the |       |           |        |               |     |     |         |     |
| --- | ------ | ------- | --------------- | --- | ----- | --- | --- | ----- | --------- | ------ | ------------- | --- | --- | ------- | --- |
|     |        |         |                 |     |       |     |     | graph | in SQLite | across | 66 languages, |     | and | exposes | 14  |
questions developers ask are inherently structural—call structural query tools via MCP [2], maintained incre-
| graphs, | dependency | chains, | module | boundaries, |     | and | im- |     |     |     |     |     |     |     |     |
| ------- | ---------- | ------- | ------ | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
1

mentally through file-watching and content-hash-based survey [19] identifies structural retrieval as a key fron-
| re-indexing. | Thesystemshipsasasinglestaticallylinked |     |     |     |     |     | tier. |     |     |     |     |     |     |
| ------------ | --------------------------------------- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- |
C binary with zero runtime dependencies. SeveralrecentsystemsconstructcodegraphsforLLM-
Our contributions are: based retrieval. GraphCoder [20] built Code Context
• A knowledge-graph architecture for code that Graphsforrepository-levelcodecompletion(ASE2024).
combines Tree-Sitter parsing across 66 languages, a CodexGraph [21] exposed code graphs to LLM agents
multi-phase build pipeline with parallel extraction, via graph database interfaces (NAACL 2025). KGCom-
6-strategy call resolution, and Louvain community pass [12] linked issues and code entities in repository-
detection, stored in a single SQLite file with zero awareknowledgegraphs,achieving58.3%onSWE-bench
external dependencies. Lite. RepoGraph [22] constructed repository-level code
• AnMCP-based interfaceexposing14typed graphs that boost existing agents by 32.8% relative im-
tool
structural queries (call-path tracing, impact anal- provement on SWE-bench (ICLR 2025).
ysis, hub detection) to any MCP-compatible LLM A second line of work focuses on graph-guided agent
agent, with sub-millisecond query latency. navigation. LocAgent [23] parsed codebases into di-
• A head-to-head evaluation across 31 languages rected heterogeneous graphs for multi-hop code localiza-
showing ten times lower token cost and 2.1 times tion(ACL2025). GraphCodeAgent[24]constructeddual
fewer tool calls at competitive quality (83% vs. requirement-structural graphs for retrieval-augmented
92%), with a systematic analysis of where graph- codegeneration. RANGER[13]usedgraph-enhancedre-
based retrieval excels and where file-based explo- trievalforrepository-levelqueries. Prometheus[25]com-
ration remains necessary. bined Tree-Sitter-based knowledge graphs with unified
The remainder of this paper is structured as follows: memory for multilingual issue resolution. The Reposi-
Section 2 surveys related work in structural code anal- tory Intelligence Graph [26] provided a deterministic ar-
ysis, code retrieval for LLMs, and token efficiency. Sec- chitectural map for LLM code assistants.
tion 3 describes the system architecture, graph schema, More fundamentally, SemanticForge [27] employed
pipeline, and security hardening. Section 4 presents the dualstatic-dynamicknowledgegraphswithneuralgraph
benchmark evaluation, performance measurements, and query generation, and the Code Graph Model [28] inte-
adoption metrics. Section 5 discusses trade-offs, threats gratedgraphrepresentationsdirectlyintoLLMattention
| to validity, | and | future | work. | Section | 6 concludes. |     | mechanisms. |         |      |       |            |          |     |
| ------------ | --- | ------ | ----- | ------- | ------------ | --- | ----------- | ------- | ---- | ----- | ---------- | -------- | --- |
|              |     |        |       |         |              |     | Our work    | differs | from | prior | approaches | by using | MCP |
2 Related Work as a standardized interface compatible with any MCP-
|     |     |     |     |     |     |     | capable | agent, | SQLite | for zero-dependency |     | deployment, |     |
| --- | --- | --- | --- | --- | --- | --- | ------- | ------ | ------ | ------------------- | --- | ----------- | --- |
2.1 Structural Code Analysis incremental synchronization for live workflows, and sup-
Structural code representations have a long history in port for 66 languages via a single binary.
| software   | engineering. |         | Program       | Dependence | Graphs | [15]     |     |     |        |        |     |     |     |
| ---------- | ------------ | ------- | ------------- | ---------- | ------ | -------- | --- | --- | ------ | ------ | --- | --- | --- |
|            |              |         |               |            |        |          | 2.3 | LLM | Coding | Agents |     |     |     |
| unify data | and          | control | dependencies. |            | Code   | Property |     |     |        |        |     |     |     |
Graphs [10] merge Abstract Syntax Trees (ASTs), con- SWE-bench [29] established the gold-standard bench-
|     |     |     |     |     |     |     | mark for | coding | agents. | SWE-Agent |     | [7] introduced |     |
| --- | --- | --- | --- | --- | --- | --- | -------- | ------ | ------- | --------- | --- | -------------- | --- |
trolflowgraphs,andPDGsintoasinglequeryablestruc-
ture. CodeQL[11]providesadeclarativequerylanguage Agent-Computer Interfaces (ACIs) optimized for LLM
over relational code databases. While powerful, these interaction. AutoCodeRover [8] combines AST-aware
systemsareheavyweight,requiringspecializeddatabases codesearchwithfaultlocalization. Agentless[9]demon-
and domain-specific query languages, and are not de- stratedthatasimplethree-phaseapproachachievescom-
signed for LLM consumption. petitiveresultswithoutanagenticloop. OpenHands[30]
Tree-Sitter [14] provides fast, incremental, error- provides an extensible open-source platform.
tolerant parsing with grammars for more than 100 lan- Thesesystemsoptimizetheagentstrategywhileusing
|         |        |        |        |       |              |         | simple | text-based | retrieval. | Our | work | is orthogonal: | we  |
| ------- | ------ | ------ | ------ | ----- | ------------ | ------- | ------ | ---------- | ---------- | --- | ---- | -------------- | --- |
| guages. | It has | become | the de | facto | standard for | editor- |        |            |            |     |      |                |     |
integrated code analysis and has been adopted by tools optimize the retrieval layer, and our approach can be
like Aider [3] for repository mapping. Recent work on combined with any of these agent architectures.
| AST-based | chunking  |        | [16] demonstrates |           | that preserving |      |     |       |            |     |     |     |     |
| --------- | --------- | ------ | ----------------- | --------- | --------------- | ---- | --- | ----- | ---------- | --- | --- | --- | --- |
|           |           |        |                   |           |                 |      | 2.4 | Token | Efficiency |     |     |     |     |
| syntactic | structure | during | code              | retrieval | improves        | both |     |       |            |     |     |     |     |
LLMLingua[31]achievesupto20timespromptcompres-
| recall and | downstream |     | task | performance | compared |     | to  |     |     |     |     |     |     |
| ---------- | ---------- | --- | ---- | ----------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
naive text chunking. sion via perplexity-based token pruning (EMNLP 2023),
|          |           |     |     |          |     |     | extended     | by LLMLingua-2 |     | [32]   | with   | task-agnostic | data     |
| -------- | --------- | --- | --- | -------- | --- | --- | ------------ | -------------- | --- | ------ | ------ | ------------- | -------- |
| 2.2 Code | Retrieval |     |     | for LLMs |     |     |              |                |     |        |        |               |          |
|          |           |     |     |          |     |     | distillation | (Findings      |     | of ACL | 2024). | Liu et al.    | [5] show |
Repository-level code understanding remains challeng- thatLLMsunderutilizeinformationinthemiddleoflong
ing for LLMs. RepoCoder [17] employs iterative BM25 contexts. LoCoBench-Agent[4]revealsacomprehension-
retrieval for code completion. DocPrompting [18] re- efficiency tradeoff: thorough codebase exploration con-
trieves documentation as generation context. A recent flictswithtokenefficiency,andagentsclusteronaPareto
2

| frontier. | Our | approach | addresses |     | this | tradeoff | by pro- |     |     |             |     |        |     |     |
| --------- | --- | -------- | --------- | --- | ---- | -------- | ------- | --- | --- | ----------- | --- | ------ | --- | --- |
|           |     |          |           |     |      |          |         |     |     | SourceFiles |     | change |     |     |
viding structurally relevant information from the start, (66languages)
avoidingunnecessarytokenconsumptionwhilemaintain-
1 Parse
| ing comprehension |     | quality. |     |     |     |     |     |     |     |     |     |     |     |     |
| ----------------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Tree-Sitter
| 3 System         |     | Design |          |     |     |     |     |     |     |     |       |     |              |     |
| ---------------- | --- | ------ | -------- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | ------------ | --- |
|                  |     |        |          |     |     |     |     |     |     | 2   | Build |     | FileWatcher  |     |
| 3.1 Architecture |     |        | Overview |     |     |     |     |     |     |     |       |     | XXH3+polling |     |
KnowledgeGraph
| Thearchitecturefollowsathree-stagepipeline.        |             |             |             |          |        |          | First,the |             |         |             |       |     |     |     |
| -------------------------------------------------- | ----------- | ----------- | ----------- | -------- | ------ | -------- | --------- | ----------- | ------- | ----------- | ----- | --- | --- | --- |
|                                                    |             |             |             |          |        |          |           |             | Louvain | SQLite(WAL) |       |     |     |     |
|                                                    |             |             |             |          |        |          |           | communities |         | nodes&edges |       |     |     |     |
| Parse stage                                        | walks       | Tree-Sitter |             | ASTs     | across | 66       | languages |             |         |             |       |     |     |     |
| to extract                                         | definitions |             | (functions, | methods, |        | classes, | inter-    |             |         |             |       |     |     |     |
| faces,enums,andtypeswithsignatures,returntypes,re- |             |             |             |          |        |          |           |             |         | 3           | Serve |     |     |     |
MCPServer
| ceivers,       | decorators, |                      | complexity, | and      | export           | status), | call      |     |     |             |          |     |     |     |
| -------------- | ----------- | -------------------- | ----------- | -------- | ---------------- | -------- | --------- | --- | --- | ----------- | -------- | --- | --- | --- |
| sites, imports |             | (8 language-specific |             |          | parsers          | plus     | a generic |     |     |             |          |     |     |     |
|                |             |                      |             |          |                  |          |           |     |     | Indexing(4) | Query(4) |     |     |     |
| fallback),     | references, |                      | and         | trait    | implementations. |          | For       |     |     |             |          |     |     |     |
|                |             |                      |             |          |                  |          |           |     |     | Analysis(3) | Code(3)  |     |     |     |
| Go, C,         | and         | C++,                 | a hybrid    | approach |                  | augments | Tree-     |     |     |             |          |     |     |     |
14tools
| Sitter extraction |     | with | LSP-style |     | type | resolution | to im- |     |     |     |     |     |     |     |
| ----------------- | --- | ---- | --------- | --- | ---- | ---------- | ------ | --- | --- | --- | --- | --- | --- | --- |
LLMAgent
| prove call-graph |     | accuracy |     | in the | presence | of method | re- |     |     |     |     |     |     |     |
| ---------------- | --- | -------- | --- | ------ | -------- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
tool-callsemantics
ceivers,pointerindirection,andpackage-qualifiedidenti-
fiers. Second, the stage executes a multi-phase Figure 1: Codebase-Memory architecture. Source
Build
|                 |          |                                    |           |             |            |              |            | files are   | parsed  | via Tree-Sitter,   |              | stored   | as a           | knowledge   |
| --------------- | -------- | ---------------------------------- | --------- | ----------- | ---------- | ------------ | ---------- | ----------- | ------- | ------------------ | ------------ | -------- | -------------- | ----------- |
| pipeline        | (Section | 3.3)                               | with      | parallel    | worker     |              | pools that |             |         |                    |              |          |                |             |
|                 |          |                                    |           |             |            |              |            | graph in    | SQLite, | and exposed        |              | to LLM   | agents         | through     |
| write extracted |          | entities                           | to        | per-worker  | in-memory  |              | graph      |             |         |                    |              |          |                |             |
|                 |          |                                    |           |             |            |              |            | 14 typed    | MCP     | tools. A           | file watcher | triggers |                | incremental |
| buffers,        | merge    | them,                              | and       | flush to    | SQLite     | with         | deferred   |             |         |                    |              |          |                |             |
|                 |          |                                    |           |             |            |              |            | re-indexing | on      | changes.           |              |          |                |             |
| indexcreation.  |          | Third,theServestageexposesthegraph |           |             |            |              |            |             |         |                    |              |          |                |             |
| via an MCP      | server   | with                               | 14        | typed       | tools      | that LLM     | agents     |             |         |                    |              |          |                |             |
|                 |          |                                    |           |             |            |              |            | Table       | 2: Edge | types representing |              | code     | relationships. |             |
| invoke through  |          | standard                           | tool-call |             | semantics. |              |            |             |         |                    |              |          |                |             |
| Codebase-Memory |          |                                    | is        | implemented |            | as a single, | stat-      |             |         |                    |              |          |                |             |
ically linked C binary with zero runtime dependencies. Edge Type Semantics
Thesystemvendors66Tree-SittergrammarsasCsource
|              |     |                     |     |     |            |     |        | CALLS,HTTP_CALLS,ASYNC_CALLS |     |     |     | Invocation   |     |     |
| ------------ | --- | ------------------- | --- | --- | ---------- | --- | ------ | ---------------------------- | --- | --- | --- | ------------ | --- | --- |
| and compiles |     | to a self-contained |     |     | executable | for | macOS, |                              |     |     |     |              |     |     |
|              |     |                     |     |     |            |     |        | IMPORTS                      |     |     |     | Moduleimport |     |     |
Linux,andWindows. Pipelineorchestration,graphstor- CONTAINS_*,DEFINES,DEFINES_METHOD Structuralnesting
|          |           |     |        |       |         |     |           | IMPLEMENTS |     |     |     | Interfaceimpl. |     |     |
| -------- | --------- | --- | ------ | ----- | ------- | --- | --------- | ---------- | --- | --- | --- | -------------- | --- | --- |
| age, MCP | protocol, |     | Cypher | query | engine, |     | and back- |            |     |     |     |                |     |     |
|          |           |     |        |       |         |     |           | HANDLES    |     |     |     | Route→handler  |     |     |
ground synchronization are implemented entirely in C. INHERITS,DECORATES OOPhierarchy
All state lives in a single SQLite file. USES_TYPE,USAGE Symbolreference
A background file watcher monitors the repository for THROWS,READS,WRITES Sideeffects
|         |              |          |          |             |               |             |             | CONFIGURES              |     |     |     | Configlinkage       |     |     |
| ------- | ------------ | -------- | -------- | ----------- | ------------- | ----------- | ----------- | ----------------------- | --- | --- | --- | ------------------- | --- | --- |
| changes | using        | adaptive | polling. | When        | files         | are         | modified,   |                         |     |     |     |                     |     |     |
|         |              |          |          |             |               |             |             | TESTS,FILE_CHANGES_WITH |     |     |     | Semanticlinks       |     |     |
| an XXH3 | content      | hash     | triggers | incremental |               | re-indexing |             |                         |     |     |     |                     |     |     |
|         |              |          |          |             |               |             |             | MEMBER_OF               |     |     |     | Communitymembership |     |     |
| of only | the affected |          | files.   | Figure      | 1 illustrates |             | the overall |                         |     |     |     |                     |     |     |
architecture.
|           |     |        |     |     |     |     |     | and Laravel)   |     | with confidence | scoring | (0.0–1.0),     |     | enabling  |
| --------- | --- | ------ | --- | --- | --- | --- | --- | -------------- | --- | --------------- | ------- | -------------- | --- | --------- |
| 3.2 Graph |     | Schema |     |     |     |     |     |                |     |                 |         |                |     |           |
|           |     |        |     |     |     |     |     | REST endpoints |     | to be           | treated | as first-class |     | graph en- |
The knowledge graph uses a property-graph model with tities. This allows the system to represent distributed
| typed nodes | and | edges: |       |        |           |        |     |                |            |                 |     |                |     |        |
| ----------- | --- | ------ | ----- | ------ | --------- | ------ | --- | -------------- | ---------- | --------------- | --- | -------------- | --- | ------ |
|             |     |        |       |        |           |        |     | codebases,     | such       | as microservice |     | architectures, |     | across |
|             |     |        |       |        |           |        |     | multiple       | languages. |                 |     |                |     |        |
| Table       | 1:  | Node   | types | in the | knowledge | graph. |     |                |            |                 |     |                |     |        |
|             |     |        |       |        |           |        |     | 3.3 Multi-Pass |            | Pipeline        |     |                |     |        |
Node Type Extracted From ThepipelineexecutesinsixphaseswithinasingleSQLite
Project, Package, Folder Directory structure transaction. Phases 1–4 write to an in-memory graph
File, Module File system buffer(cbm_gbuf_t),aCstructholdingnodesandedges
Function, Method, Tree-Sitter AST in hash maps indexed by qualified name, label, and
Class
Interface, Enum, Type Tree-Sitter AST ID, avoiding SQLite overhead during bulk insertion.
Route Framework detection Extraction and resolution phases dispatch work to a
|     |     |     |     |     |     |     |     | pthreads-based |     | worker | pool with | atomic | work-stealing: |     |
| --- | --- | --- | --- | --- | --- | --- | --- | -------------- | --- | ------ | --------- | ------ | -------------- | --- |
The schema includes HTTP_CALLS and ASYNC_CALLS each worker writes to a per-worker buffer, which are
edges discovered via cross-service HTTP route/call- merged after completion. The buffer assigns temporary
site matching (6 framework-specific extractors cover- sequentialIDsthatareremappedtorealSQLiterowIDs
ing Python, Go, Java/Spring, Kotlin/Ktor, Express.js, during flush. Phase 6 operates directly on the database
3

| after index | creation. |     |     |     |     |     |     | Each | pass builds | a per-file |     |     |     | populated |
| ----------- | --------- | --- | --- | --- | --- | --- | --- | ---- | ----------- | ---------- | --- | --- | --- | --------- |
TypeRegistry
|     |     |     |     |     |     |     |     | with all | definitions | extracted | in  | the Build | stage | (both |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | ----------- | --------- | --- | --------- | ----- | ----- |
Table 3: Pipeline phases and their outputs. file-local and cross-file), augmented with auto-generated
|     |     |     |     |     |     |     |     | standard-library |     | type stubs. | A   | Scope | structure | tracks |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------------- | --- | ----------- | --- | ----- | --------- | ------ |
Phase Output variable bindings introduced by declarations, assign-
ments,short-variabledeclarations(Go),andfunctionpa-
| 1.Structure |     | File discovery; |     | Project, | Package, | Folder, | File |     |     |     |     |     |     |     |
| ----------- | --- | --------------- | --- | -------- | -------- | ------- | ---- | --- | --- | --- | --- | --- | --- | --- |
nodes+containmentedges rameters. Theresolverthenwalksallcall-siteASTnodes
2.Extraction Paralleldefinitionextractionviapthreadsworker and evaluates the receiver expression’s type bottom-
pool; Function, Method, Class, Interface, Enum, up: identifier lookup in the scope chain, field and
Typenodes;decoratortags;FunctionRegistry
3.Resolution Parallel call, usage, and semantic resolution; methodlookupwithbase-classorembedded-typetraver-
CALLS, IMPORTS, USAGES, USES_TYPE, sal, return-type propagation through call chains, and
|     |     | IMPLEMENTS, |     | INHERITS, |     | DECORATES |     |                                         |     |     |     |     |               |     |
| --- | --- | ----------- | --- | --------- | --- | --------- | --- | --------------------------------------- | --- | --- | --- | --- | ------------- | --- |
|     |     |             |     |           |     |           |     | typesimplification(referenceunwrapping, |     |     |     |     | pointerderef- |     |
edges
|              |     |                                          |     |     |     |     |     | erencing, | alias   | resolution). | For        | C++,   | the | pass addi-  |
| ------------ | --- | ---------------------------------------- | --- | --- | --- | --- | --- | --------- | ------- | ------------ | ---------- | ------ | --- | ----------- |
| 4.Enrichment |     | TESTSedges,HTTProutematching,configlink- |     |     |     |     |     |           |         |              |            |        |     |             |
|              |     |                                          |     |     |     |     |     | tionally  | handles | namespace    | resolution | (using |     | directives, |
ing,gitco-changeedges
5.Flush Bulk INSERT into SQLite with deferred index declarations, and aliases), template parameter defaults,
|              |       | creation                          |       |              |           |            |          | andpendingtemplatecallsthatareresolvedretroactively |             |              |              |                  |           |           |
| ------------ | ----- | --------------------------------- | ----- | ------------ | --------- | ---------- | -------- | --------------------------------------------------- | ----------- | ------------ | ------------ | ---------------- | --------- | --------- |
| 6.Post-index |       | Louvaincommunities,XXH3filehashes |       |              |           |            |          |                                                     |             |              |              |                  |           |           |
|              |       |                                   |       |              |           |            |          | when concrete                                       | argument    |              | types become |                  | available | at call   |
|              |       |                                   |       |              |           |            |          | sites. Resolved                                     | calls       | carry        | the fully    | qualified        | callee    | name      |
|              |       |                                   |       |              |           |            |          | and bypass                                          | the         | string-based | cascade      | entirely,        |           | producing |
| 3.4          | Call  | Resolution                        |       |              |           |            |          |                                                     |             |              |              |                  |           |           |
|              |       |                                   |       |              |           |            |          | higher-confidenceedgesinthegraph.                   |             |              |              | Thepassesoperate |           |           |
| Resolving    | raw   | callee                            | names | (e.g.,       | pkg.Func) |            | to qual- |                                                     |             |              |              |                  |           |           |
|              |       |                                   |       |              |           |            |          | in batch                                            | mode across | all          | files of the | respective       |           | language, |
| ified graph  | nodes | is                                | the   | core linking |           | challenge. | The      |                                                     |             |              |              |                  |           |           |
enablingcross-fileresolutionwithinasinglepipelinerun.
| FunctionRegistry |     |     | indexes | all definitions |     | by  | qualified |     |     |     |     |     |     |     |
| ---------------- | --- | --- | ------- | --------------- | --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
name(exactmap)andsimplename(reverseindex). Res- 3.5 MCP Tool Interface
olution uses a prioritized 6-strategy cascade with per- Thesystemexposes14toolsgroupedintofourcategories:
| strategy       | confidence |            | scoring:     |           |            |              |         |          |                  |               |     |                  |          |       |
| -------------- | ---------- | ---------- | ------------ | --------- | ---------- | ------------ | ------- | -------- | ---------------- | ------------- | --- | ---------------- | -------- | ----- |
|                |            |            |              |           |            |              |         | Table 4: | MCP              | tools exposed | by  | Codebase-Memory. |          |       |
| 1. Import      |            | map        | (confidence  | 0.95):    |            | Split callee | into    |          |                  |               |     |                  |          |       |
| prefix.suffix; |            | look       | up prefix    | in        | the file’s | import       | map     |          |                  |               |     |                  |          |       |
| to             | obtain     | the module |              | qualified | name;      | join with    | suf-    |          |                  |               |     |                  |          |       |
|                |            |            |              |           |            |              |         | Category | Tool             |               |     | Description      |          |       |
| fix;           | exact      | match      | in registry. |           |            |              |         |          |                  |               |     |                  |          |       |
|                |            |            |              |           |            |              |         |          | index_repository |               |     | Build/update     |          | graph |
| 2.             |            |            |              | (0.85):   | Fallback   | when         | the ex- |          |                  |               |     |                  |          |       |
| Import         |            | map suffix |              |           |            |              |         |          | index_status     |               |     | Poll indexing    | progress |       |
Indexing
act import-map match fails; attempt suffix-based list_projects List indexed repos
| matching |     | against | import-resolved |     | module | paths. |     |     |     |     |     | Remove | index |     |
| -------- | --- | ------- | --------------- | --- | ------ | ------ | --- | --- | --- | --- | --- | ------ | ----- | --- |
delete_project
| 3.  | module(0.90): |     |     | Prefixcalleewiththeenclos- |     |     |     |     |     |     |     |     |     |     |
| --- | ------------- | --- | --- | -------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Same
|        |        |        |           |       |       |        |      |          | search_graph    |     |     | Symbol      | search    |     |
| ------ | ------ | ------ | --------- | ----- | ----- | ------ | ---- | -------- | --------------- | --- | --- | ----------- | --------- | --- |
| ing    | file’s | module | qualified | name; | exact | match. |      |          |                 |     |     |             |           |     |
|        |        |        |           |       |       |        |      |          | trace_call_path |     |     | Call-chain  | traversal |     |
| 4.     |        |        | (0.75):   | Look  | up    | simple | name | in Query |                 |     |     |             |           |     |
| Unique |        | name   |           |       |       |        |      |          | query_graph     |     |     | Cypher-like | queries   |     |
the reverse index; accept if exactly one candidate ingest_traces Import runtime traces
| project-wide |        | (penalized |            | if not               | import-reachable). |             |          |          |                  |     |     |              |               |     |
| ------------ | ------ | ---------- | ---------- | -------------------- | ------------------ | ----------- | -------- | -------- | ---------------- | --- | --- | ------------ | ------------- | --- |
|              |        |            |            |                      |                    |             |          |          | detect_changes   |     |     | Git diff     | impact        |     |
| 5.           |        |            | (0.55):    | Among                | multiple           | candidates, |          |          |                  |     |     |              |               |     |
| Suffix       | match  |            |            |                      |                    |             |          |          |                  |     |     |              |               |     |
|              |        |            |            |                      |                    |             |          | Analysis | get_graph_schema |     |     | Schema       | introspection |     |
| select       | by     | suffix     | match      | with import-distance |                    |             | scoring; |          |                  |     |     |              |               |     |
|              |        |            |            |                      |                    |             |          |          | get_architecture |     |     | Architecture | summary       |     |
| nearest      | module |            | path wins. |                      |                    |             |          |          |                  |     |     |              |               |     |
6. (0.30–0.40): Last-resort matching using get_code_snippet Source retrieval
Fuzzy
|        |            |     |      |               |     |            |      | Code | search_code |     |     | Full-text    | search    |     |
| ------ | ---------- | --- | ---- | ------------- | --- | ---------- | ---- | ---- | ----------- | --- | --- | ------------ | --------- | --- |
| string | similarity |     | when | no structured |     | resolution | suc- |      |             |     |     |              |           |     |
|        |            |     |      |               |     |            |      |      | manage_adr  |     |     | Architecture | decisions |     |
ceeds.
| From     | our observations, |     | strategies |     | 1–3   | resolve    | ∼80% | of              |              |            |     |      |      |           |
| -------- | ----------------- | --- | ---------- | --- | ----- | ---------- | ---- | --------------- | ------------ | ---------- | --- | ---- | ---- | --------- |
|          |                   |     |            |     |       |            |      | Each            | tool returns | structured |     | JSON | that | the LLM   |
| calls in | well-structured   |     | codebases, |     | while | strategies | 4–6  |                 |              |            |     |      |      |           |
|          |                   |     |            |     |       |            |      | agent processes |              | directly.  | The |      |      | tool sup- |
handle cross-module references and dynamic dispatch. query_graph
|     |     |     |     |     |     |     |     | ports a     | Cypher-like | query | language | for      | arbitrary | graph       |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------- | ----------- | ----- | -------- | -------- | --------- | ----------- |
|     |     |     |     |     |     |     |     | traversals, | while       |       |          | provides |           | directional |
trace_call_path
| LSP-Style | Hybrid |     | Type | Resolution. |     | The | name- |     |     |     |     |     |     |     |
| --------- | ------ | --- | ---- | ----------- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
(inbound/outbound)call-chaintracingwithconfigurable
basedcascadeaboveoperatesonstring-levelcalleetokens
depth.
| and does | not | track | expression | types. | This | limits | accu- |     |     |     |     |     |     |     |
| -------- | --- | ----- | ---------- | ------ | ---- | ------ | ----- | --- | --- | --- | --- | --- | --- | --- |
racy for languages with method receivers (Go), pointer 3.6 Incremental Synchronization
indirection and implicit this (C/C++), or template- Oneachfile-systemevent,thesystemcomputesanXXH3
dependent calls (C++). To address this, the system in- hash of the modified file and compares it against the
cludes dedicated type-resolution passes for Go, C, and stored hash. If changed, the file’s nodes and edges
C++ that run after the initial Tree-Sitter extraction are deleted and re-parsed with Tree-Sitter; the hash is
| phase. |     |     |     |     |     |     |     | updated | and affected | Louvain | community |     | assignments |     |
| ------ | --- | --- | --- | --- | --- | --- | --- | ------- | ------------ | ------- | --------- | --- | ----------- | --- |
4

are re-computed. XXH3 is a non-cryptographic 64-bit ternaldomains,trackingscripts,andhiddeniframes;
hash achieving ∼30GB/s throughput, chosen over cryp- the HTTP server binds to 127.0.0.1 only with
tographic hashes for its speed in content-addressed in- locked CORS policy.
dexingwherecollisionresistanceisnotasecurityrequire- 7. MCP robustness testing: 23 adversarial JSON-
| ment. |     |     |     |     |     |     |     | RPC  | payloads | cover  | malformed |            | JSON, | SQL   | injec- |
| ----- | --- | --- | --- | --- | --- | --- | --- | ---- | -------- | ------ | --------- | ---------- | ----- | ----- | ------ |
|       |     |     |     |     |     |     |     | tion | (DROP    | TABLE, |           | DATABASE), |       | shell | injec- |
ATTACH
| 3.7 Community |     |     | Detection |     |     |     |     |      |             |     |                  |     |      |            |     |
| ------------- | --- | --- | --------- | --- | --- | --- | --- | ---- | ----------- | --- | ---------------- | --- | ---- | ---------- | --- |
|               |     |     |           |     |     |     |     | tion | ($(whoami), |     | pipe sequences), |     | path | traversal, |     |
The system applies Louvain modularity optimization [1] ReDoS patterns, and oversized inputs; no payload
to partition the call graph into functional communities. may cause a crash or hang.
| Thealgorithmiteratestwophases: |     |     |     |     | (a)localmoving,each |     |     |                                 |     |     |     |     |                  |     |     |
| ------------------------------ | --- | --- | --- | --- | ------------------- | --- | --- | ------------------------------- | --- | --- | --- | --- | ---------------- | --- | --- |
|                                |     |     |     |     |                     |     |     | 8. Vendoreddependencyintegrity: |     |     |     |     | SHA-256checksums |     |     |
node greedily joins the neighboring community maxi- for all 72 vendored library files (including 66 Tree-
| mizing | modularity | gain |     |     |     |     | /(2m), |     |     |     |     |     |     |     |     |
| ------ | ---------- | ---- | --- | --- | --- | --- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
∆Q = w in −γ ·k i ·Σ tot Sitter grammars) detect supply-chain tampering;
whereγ=1.0istheresolutionparameter,k isthenode’s vendoredcodeisadditionallyscannedfordangerous
i
| weighted | degree, | Σ   | is the | community’s |     | total | degree, | calls. |     |     |     |     |     |     |     |
| -------- | ------- | --- | ------ | ----------- | --- | ----- | ------- | ------ | --- | --- | --- | --- | --- | --- | --- |
tot
| and | is total | edge | weight; | (b) | refinement, |     | commu- |     |     |     |     |     |     |     |     |
| --- | -------- | ---- | ------- | --- | ----------- | --- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
m
| nities with | internal |     | density | <1% | are | split | by eject- |     |     |     |     |       |           |     |           |
| ----------- | -------- | --- | ------- | --- | --- | ----- | --------- | --- | --- | --- | --- | ----- | --------- | --- | --------- |
|             |          |     |         |     |     |       |           |     |     |     |     | Shell | arguments |     | are vali- |
ing weakly-connected members. Convergence typically Code-Level Protections.
|               |             |             |                 |               |     |          |         | dated via        | cbm_validate_shell_arg() |                 |          |     | before     | all | popen    |
| ------------- | ----------- | ----------- | --------------- | ------------- | --- | -------- | ------- | ---------------- | ------------------------ | --------------- | -------- | --- | ---------- | --- | -------- |
| occurs        | in 3–5      | iterations. |                 | The algorithm |     | operates | on      |                  |                          |                 |          |     |            |     |          |
|               |             |             |                 |               |     |          |         | calls, rejecting |                          | metacharacters, |          |     | backticks, | and | sub-     |
| CALLS,        | HTTP_CALLS, |             | and ASYNC_CALLS |               |     | edges,   | produc- |                  |                          |                 |          |     |            |     |          |
|               |             |             |                 |               |     |          |         | stitution        | patterns.                |                 | A SQLite |     | authorizer |     | callback |
| ing Community |             | nodes       | and             |               |     | edges    | used by |                  |                          |                 |          |     |            |     |          |
MEMBER_OF
|     |     |     |     |     |     |     |     | blocks ATTACH/DETACH |     |     | statements |     | at the | engine | level, |
| --- | --- | --- | --- | --- | --- | --- | --- | -------------------- | --- | --- | ---------- | --- | ------ | ------ | ------ |
get_architecture.
|     |     |     |     |     |     |     |     | preventing | SQL-injection-based |     |     | file | creation. |     | The |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | ------------------- | --- | --- | ---- | --------- | --- | --- |
3.8 Security Hardening get_code_snippet tool applies realpath() contain-
|             |      |          |               |      |              |            |           | ment checks | to        | prevent | path-traversal |     | reads | outside      | the |
| ----------- | ---- | -------- | ------------- | ---- | ------------ | ---------- | --------- | ----------- | --------- | ------- | -------------- | --- | ----- | ------------ | --- |
| MCP servers |      | present  | a distinctive |      | trust        | challenge: | they      |             |           |         |                |     |       |              |     |
|             |      |          |               |      |              |            |           | project     | root. All | tests   | are compiled   |     | with  | AddressSani- |     |
| execute     | with | the host | agent’s       | full | permissions, |            | yet users |             |           |         |                |     |       |              |     |
install them as opaque binaries from third-party reposi- tizer and UndefinedBehaviorSanitizer; a 15-minute soak
|         |        |        |              |     |         |      |       | test under | ASan | stress-tests |     | sustained |     | workloads | for |
| ------- | ------ | ------ | ------------ | --- | ------- | ---- | ----- | ---------- | ---- | ------------ | --- | --------- | --- | --------- | --- |
| tories. | As LLM | agents | increasingly |     | operate | with | broad |            |      |              |     |           |     |           |     |
file-systemandnetworkaccess,theintegrityofeverytool memory safety regressions.
| in the agent’s |               | toolchain | becomes | a          | supply-chain |           | security |             |                      |     |           |       |          |            |          |
| -------------- | ------------- | --------- | ------- | ---------- | ------------ | --------- | -------- | ----------- | -------------------- | --- | --------- | ----- | -------- | ---------- | -------- |
| concern.       | A compromised |           | or      | malicious  | MCP          | server    | could    |             |                      |     |           |       |          |            |          |
|                |               |           |         |            |              |           |          | Release     | Verification         |     | Pipeline. |       | Releases |            | follow a |
| exfiltrate     | source        | code,     | inject  | backdoors, |              | or tamper | with     |             |                      |     |           |       |          |            |          |
|                |               |           |         |            |              |           |          | three-stage | draft–verify–publish |     |           | model | that     | integrates |          |
developer environments, all while appearing to function established industry security tooling. In the stage,
draft
| normally.      | This | threat    | model  | motivates |     | the defense-in- |     |                   |            |          |      |          |             |            |        |
| -------------- | ---- | --------- | ------ | --------- | --- | --------------- | --- | ----------------- | ---------- | -------- | ---- | -------- | ----------- | ---------- | ------ |
|                |      |           |        |           |     |                 |     | binaries          | are built, | signed   | via  | Sigstore |             | cosign     | (Linux |
| depth approach |      | described | below. |           |     |                 |     |                   |            |          |      |          |             |            |        |
|                |      |           |        |           |     |                 |     | Foundation),      | and        | attested | with | SLSA     | build       | provenance |        |
|                |      |           |        |           |     |                 |     | (Google/OpenSSF). |            | GitHub   |      | CodeQL   | (Microsoft) |            | runs   |
8-Layer CI Audit Suite. An automated audit suite staticapplicationsecuritytestingoneverypush,blocking
runs on every commit before merge: the release on any open alert. In the stage, every
verify
1. Static allow-list audit: Every call to dangerous libc binary is submitted to VirusTotal (Google/Chronicle)
functions (system, popen, fork, execvp) must ap- via the ghaction-virustotal GitHub Action, where
pear in an audited allow-list with explicit justifica- morethan70 antivirusenginesscan for malware; azero-
tion; new calls fail CI. tolerance policy blocks publication if any engine flags a
2. Post-build scanning of the detection. The CI pipeline polls each scan until all en-
| Binary | string | audit: |     |     |     |     |     |     |     |     |     |     |     |     |     |
| ------ | ------ | ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
compiled binary for hardcoded URLs (only GitHub gines have completed (up to 20 minutes), requiring a
API and localhost permitted), embedded creden- minimumof60enginestoreport. Additionally,platform-
tials, and suspicious base64-encoded payloads. native antivirus scans run during CI smoke tests on ev-
3. Networkegressmonitoring: OnLinux,theMCPses- ery build: Windows Defender (MpCmdRun.exe with ML
sion runs under to capture all heuristics and up-to-date signatures) on Windows, and
|     |     |     | strace |     |     | connect() |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | ------ | --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
syscalls; only localhost, DNS, and the GitHub re- ClamAV (Cisco/Talos, with freshclam signature up-
lease API are permitted. dates)onLinuxandmacOS.AnOpenSSFScorecardgate
4. A sandboxed dry- (Google/OSSF) enforces a minimum repository health
| Install | output | path | validation: |     |     |     |     |     |     |     |     |     |     |     |     |
| ------- | ------ | ---- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
run verifies that the installer writes only to ex- score. Only after all gates pass does the release be-
pected directories and blocks writes to sensitive come public. Each release includes SHA-256 checksums,
paths (~/.ssh, ~/.gnupg, ~/.aws). a CycloneDX software bill of materials (SBOM) listing
5. Smoke-test hardening: End-to-end functional tests allsevenvendoreddependencies, andinstructionsforin-
verify indexing, querying, and clean shutdown with dependentuserverificationviagh
|     |     |     |     |     |     |     |     |     |     |     |     | attestation |     |     | verify |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----------- | --- | --- | ------ |
no residual processes. and cosign verify-blob. To our knowledge, this level
6. Graph-UI audit: Frontendassetscanningblocksex- ofautomatedbinaryverification,combiningmulti-engine
5

antivirus scanning from Google, Microsoft, and Cisco Table 6: Head-to-head comparison: MCP Agent vs. Ex-
with cryptographic build provenance and zero-tolerance plorer Agent.
release gating, is not commonly implemented by open-
source MCP servers or developer tools distributed via Metric MCP Explorer Difference
GitHub.
Qualityscore 0.83 0.92 90%ofExplorer
Toolcalls/question 2.3 4.8 2.1timesfewer
4 Evaluation Tokens/question ∼1,000 ∼10,000 10timesfewer
Querylatency <1ms 10–30s >100timesfaster
WeevaluateCodebase-Memoryalongfourdimensions:
(1) a head-to-head comparison of an MCP-augmented
agent against a file-exploration agent, (2) a qualitative (10/31)—queriesrequiringline-levelcodethatthegraph
analysis of where each approach excels, (3) a measure- intentionally does not store. The weakest MCP result
ment of system performance, and (4) early community is macro-heavy C (0.58 vs. 1.00), where macros are not
adoption as a proxy for practical relevance. represented in the AST.
ThespeeddifferencearisesbecausetheMCPAgentre-
4.1 Head-to-Head Benchmark
solvesstructuralqueriesviapre-computedgraphlookups
We designed a benchmark consisting of 12 standard-
(breadth-first search via SQL recursive Common Table
ized question categories covering hub detection, caller
Expression: ∼0.3ms). TheExplorerAgentmustdiscover
ranking, dependency manifests, and full call-chain trac-
structure at query time: grep for function names, read
ing (Table 5). Each of 31 programming languages was
matchingfiles,parsecontext,repeat. Thismultipliestool
testedagainstarealopen-sourcerepositoryrangingfrom
calls and tokens linearly with codebase size. The graph
78 nodes (HCL/Terraform) to 49,398 nodes (Python/D-
approachpaystheindexingcostonce(6sfor49Knodes)
jango). Two agents were compared: an MCP Agent
and amortizes it across all subsequent queries.
with access to Codebase-Memory’s 14 tools, and an
ExplorerAgentusingconventionalfile-readingandgrep- 4.2 Comparison with Alternative Ap-
basedexploration. BothagentsusedClaudeOpus4.6as proaches
the LLM backend and received identical questions. Re-
Table7positionsCodebase-Memory againstthethree
sponsesweregradedbythefirstauthoragainstreference
dominant paradigms for LLM code retrieval.
answers derived from manual code inspection. Scores
≥0.80 were classified as PASS, 0.40–0.79 as PARTIAL, Table 7: Comparison of code retrieval approaches for
and <0.40 as FAIL. LLM agents.
Table 5: Benchmark question categories and primary
MCP tools. Feature Emb./RAG Repo- Graph+LLM Ours
Map
Languages 10–30 ∼100 8–14 66
Q# Category Primary Tool Struct.queries No No Yes Yes
Infra. Vector None Neo4j SQLite
1 Indexing get_graph_schema DB
2–3 Discovery search_graph Persistence Yes No Yes Yes
Embed.model Yes No Some No
4 Pattern matching search_graph Tok./query ∼2–5K ∼1K ∼5K ∼1K
5 Code retrieval get_code_snippet Auto-sync Varies N/A Manual Yes
License Comm. Apache Mixed MIT
6 Code search search_code
7–8 Call tracing trace_call_path
9–10 Graph query query_graph
4.3 System Performance
11 OOP analysis query_graph
12 File operations get_architecture Table 8 reports performance measurements on an Apple
M3 Pro (macOS).
Table6summarizesthehead-to-headcomparison. The
Table 8: System performance benchmarks.
MCP Agent achieves 90% of the Explorer Agent’s qual-
ity score while consuming an order of magnitude fewer
tokens and requiring 2.1 times fewer tool calls. Operation Time
The MCP Agent shows advantages in hub detec-
Fresh index (49K nodes, 196K edges) ∼6s
tion and caller ranking for 19 of 31 languages—queries Fresh index (Linux kernel, 2.1M nodes, 4.9M ∼3min
that require following pre-materialized graph edges. edges)
The strongest results appear for functional languages Incremental re-index ∼1.2s
(Haskell, OCaml, Elixir), where the quality gap narrows Cypher query (relationship traversal) <1ms
to ∼1%. BFS call-path tracing (depth=5) ∼0.3ms
The Explorer retains an advantage for full source Name search (regex) <10ms
Dead code detection ∼150ms
context (16/31 languages) and exhaustive call-site grep
6

The Django repository (49,398 nodes, 196,022 edges) 5.3 Trust and Supply-Chain Security in
serves as the primary benchmark. At the upper end of MCP Ecosystems
| scale, indexingtheLinuxkernel(28Mlines |     |      |       |     |            | ofcode, | 75K      |                |     |          |            |         |                |                |       |
| -------------------------------------- | --- | ---- | ----- | --- | ---------- | ------- | -------- | -------------- | --- | -------- | ---------- | ------- | -------------- | -------------- | ----- |
|                                        |     |      |       |     |            |         |          | The growing    |     | adoption | of MCP     | servers | as             | tool providers |       |
| files) produces                        |     | 2.1M | nodes | and | 4.9M edges | in      | approxi- |                |     |          |            |         |                |                |       |
|                                        |     |      |       |     |            |         |          | for autonomous |     | agents   | introduces |         | a supply-chain |                | trust |
mately3minutes,demonstratingthatthepipelinescales
|            |              |            |            |              |          |               |     | problem         | that,           | to date,      | has              | received     | little        | attention  | in    |
| ---------- | ------------ | ---------- | ---------- | ------------ | -------- | ------------- | --- | --------------- | --------------- | ------------- | ---------------- | ------------ | ------------- | ---------- | ----- |
| to very    | large        | codebases. |            | Incremental  |          | re-indexing   | via |                 |                 |               |                  |              |               |            |       |
|            |              |            |            |              |          |               |     | the literature. |                 | Unlike        | library          | dependencies |               | managed    |       |
| XXH3       | content-hash |            | comparison |              | achieves | approximately |     |                 |                 |               |                  |              |               |            |       |
|            |              |            |            |              |          |               |     | by package      | registries      |               | with established |              | review        | processes, |       |
| four times | speedup      |            | over full  | re-indexing. |          |               |     |                 |                 |               |                  |              |               |            |       |
|            |              |            |            |              |          |               |     | MCP servers     |                 | are typically | distributed      |              | as standalone |            | bi-   |
|            |              |            |            |              |          |               |     | naries          | from individual |               | repositories.    |              | Users         | grant      | these |
4.4 Community Adoption binariesbroadhostpermissions—file-systemaccess,pro-
|            |     |           |            |     |           |       |       | cess spawning, |     | network | communication—yet |     |     | have | lim- |
| ---------- | --- | --------- | ---------- | --- | --------- | ----- | ----- | -------------- | --- | ------- | ----------------- | --- | --- | ---- | ---- |
| As a proxy | for | practical | relevance, |     | we report | early | adop- |                |     |         |                   |     |     |      |      |
tion metrics from the public GitHub repository. Within itedmeanstoverifywhatthebinarydoesbeyondreading
|            |     |             |         |           |     |     |            | its source | code. |     |     |     |     |     |     |
| ---------- | --- | ----------- | ------- | --------- | --- | --- | ---------- | ---------- | ----- | --- | --- | --- | --- | --- | --- |
| four weeks | of  | the initial | release | (February |     | 25, | 2026), the |            |       |     |     |     |     |     |     |
project accumulated more than 900 stars and approxi- Thisproblemisamplifiedinagenticsettingswherethe
|             |            |           |         |          |            |     |           | LLM autonomously |               |     | invokes | tools  | without | per-call | user |
| ----------- | ---------- | --------- | ------- | -------- | ---------- | --- | --------- | ---------------- | ------------- | --- | ------- | ------ | ------- | -------- | ---- |
| mately      | 100 forks. | Referring |         | traffic  | originated |     | primarily |                  |               |     |         |        |         |          |      |
|             |            |           |         |          |            |     |           | approval.        | A compromised |     | MCP     | server | could   | silently | ex-  |
| from Reddit |            | (1,288    | views), | LinkedIn | (441),     | and | direct    |                  |               |     |         |        |         |          |      |
GitHub discovery (869). The tool is automatically de- filtrate code, inject malicious changes, or establish per-
|     |     |     |     |     |     |     |     | sistent | backdoors | across | developer |     | environments. |     | The |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | --------- | ------ | --------- | --- | ------------- | --- | --- |
tectedby10codingagentsincludingClaudeCode,Codex
CLI, Gemini CLI, Zed, and VS Code. These figures sug- attack surface extends beyond the server binary itself
gest that structural code retrieval addresses a concrete to vendored dependencies, build pipelines, and installer
scripts.
| need among | LLM | agent | practitioners. |     |     |     |     |                   |          |          |                |              |                    |        |      |
| ---------- | --- | ----- | -------------- | --- | --- | --- | --- | ----------------- | -------- | -------- | -------------- | ------------ | ------------------ | ------ | ---- |
|            |     |       |                |     |     |     |     | Our               | approach | to       | this challenge |              | (Section           | 3.8)   | com- |
|            |     |       |                |     |     |     |     | bines established |          | industry | security       |              | tooling—VirusTotal |        |      |
|            |     |       |                |     |     |     |     | (Google),         | Windows  |          | Defender       | (Microsoft), |                    | ClamAV |      |
5 Discussion
|     |       |       |       |      |     |      |        | (Cisco),       | CodeQL, |         | SLSA provenance, |                | and         | OpenSSF |         |
| --- | ----- | ----- | ----- | ---- | --- | ---- | ------ | -------------- | ------- | ------- | ---------------- | -------------- | ----------- | ------- | ------- |
|     |       |       |       |      |     |      |        | Scorecard—into |         | an      | automated,       | zero-tolerance |             |         | release |
| 5.1 | Graph | vs.   | Text: | When |     | Does | Struc- |                |         |         |                  |                |             |         |         |
|     |       |       |       |      |     |      |        | pipeline.      | We      | believe | this represents  |                | a necessary |         | base-   |
|     | ture  | Help? |       |      |     |      |        |                |         |         |                  |                |             |         |         |
|     |       |       |       |      |     |      |        | line for       | any MCP | server  | that             | requests       | elevated    | host    | per-    |
Our head-to-head evaluation reveals a clear division of missions, and advocate for the MCP ecosystem to adopt
| labor. | The | MCP Agent |     | excels | at cross-file |     | structural |         |              |            |     |     |         |         |       |
| ------ | --- | --------- | --- | ------ | ------------- | --- | ---------- | ------- | ------------ | ---------- | --- | --- | ------- | ------- | ----- |
|        |     |           |     |        |               |     |            | similar | verification | standards. |     | The | absence | of such | stan- |
queries, hub detection, caller ranking, and dependency dards today means that users must either trust individ-
chaintraversal,wherepre-materializedgraphedgesavoid
|              |             |           |              |               |                   |             |            | ual maintainers |           | or audit | each      | tool      | manually—neither |     | of    |
| ------------ | ----------- | --------- | ------------ | ------------- | ----------------- | ----------- | ---------- | --------------- | --------- | -------- | --------- | --------- | ---------------- | --- | ----- |
| the linear   | token       | cost      | of iterative |               | file exploration. |             | The        |                 |           |          |           |           |                  |     |       |
|              |             |           |              |               |                   |             |            | which scales    | as        | the MCP  | tool      | ecosystem | grows.           |     |       |
| ten times    | token       | reduction |              | and 2.1       | times             | fewer       | tool calls |                 |           |          |           |           |                  |     |       |
| translate    | directly    | into      | lower        | latency       | and               | cost.       | However,   |                 |           |          |           |           |                  |     |       |
|              |             |           |              |               |                   |             |            | 5.4             | Threats   | to       | Validity  |           |                  |     |       |
| the Explorer |             | Agent     | retains      | an advantage  |                   | for queries | re-        |                 |           |          |           |           |                  |     |       |
|              |             |           |              |               |                   |             |            |                 |           | The      | benchmark |           | compares         | two | agent |
| quiring      | full source | context   |              | or exhaustive |                   | pattern     | match-     | Internal        | validity. |          |           |           |                  |     |       |
ing, where the graph’s intentional abstraction (storing configurations (MCP vs. Explorer) on a single LLM
|               |     |          |         |              |         |               |           | backend       | (Claude | Opus         | 4.6);   | results     | may       | not generalize |      |
| ------------- | --- | -------- | ------- | ------------ | ------- | ------------- | --------- | ------------- | ------- | ------------ | ------- | ----------- | --------- | -------------- | ---- |
| relationships |     | but not  | source  | lines)       | becomes | a limitation. |           |               |         |              |         |             |           |                |      |
|               |     |          |         |              |         |               |           | across models |         | or prompting |         | strategies. | Responses |                | were |
| This suggests |     | that the | optimal | architecture |         | is            | a hybrid: |               |         |              |         |             |           |                |      |
|               |     |          |         |              |         |               |           | graded        | by the  | first author | against |             | manually  | verified       | ref- |
graph-basedretrievalforstructuralqueries,withfallback
|                     |     |     |              |     |        |     |     | erenceanswersonacontinuous0–1scale. |     |     |     |     |     | Theclassifica- |     |
| ------------------- | --- | --- | ------------ | --- | ------ | --- | --- | ----------------------------------- | --- | --- | --- | --- | --- | -------------- | --- |
| to file exploration |     | for | source-level |     | tasks. |     |     |                                     |     |     |     |     |     |                |     |
tionthresholds(PASS≥0.80,PARTIAL0.40–0.79,FAIL
<0.40)werechosenpragmatically;alternativethresholds
5.2 Structural Retrieval as a Paradigm could shift category distributions.
Current RAG approaches for code primarily use External validity. While 31 languages are bench-
embedding-basedretrieval,treatingcodeastext[17,33]. marked, each is represented by a single repository.
Our work supports the emerging paradigm of structural Macro-heavy languages (C: 0.58 quality) remain chal-
retrieval, graph traversal along typed relationships, as lengingbecausemacrosarenotrepresentedinTree-Sitter
a complement. While embedding-based retrieval excels ASTs. A systematic comparison against embedding-
at semantic similarity, structural retrieval excels at rela- basedRAG,ctags/LSP,andothergraphsystemsremains
| tional queries. |     | The | RACG | survey | [19] | identifies | this | as future work. |     |     |     |     |     |     |     |
| --------------- | --- | --- | ---- | ------ | ---- | ---------- | ---- | --------------- | --- | --- | --- | --- | --- | --- | --- |
a key frontier. Recent work on AST-based chunking [16] Construct validity. The knowledge graph captures
similarly shows that preserving syntactic structure im- static structure only; runtime behavior, reflection, and
proves retrieval quality, supporting the hypothesis that dynamicdispatcharenotrepresented. Thequery_graph
structure-awareapproachesoutperformflattextretrieval tool applies a default ceiling of 100,000 rows, which may
for code. undercount in very large codebases. All performance
7

benchmarks were measured on a single hardware con- Data Availability Statement
figuration (Apple M3 Pro); results may differ on other
The Codebase-Memory source code, bench-
platforms.
mark scripts, and evaluation data are pub-
licly available at https://github.com/DeusData/
5.5 Future Work
codebase-memory-mcp under the MIT license. The
Future work priorities include a controlled empir- version evaluated in this paper corresponds to release
ical study comparing graph-based, text-based, and v0.5.5.
embedding-based exploration across SWE-bench [29]
with ablation studies, hybrid retrieval combining struc- References
tural and semantic search, and system extensions
[1] Vincent D. Blondel, Jean-Loup Guillaume, Renaud
for multi-repository dependency tracking and LLM-
Lambiotte, and Etienne Lefebvre. Fast unfolding
generated graph summaries at the function and module
of communities in large networks. Journal of Sta-
level.
tistical Mechanics: Theory and Experiment, 2008
A particularly promising application domain is health
(10):P10008, 2008. doi: 10.1088/1742-5468/2008/
informatics, where domain-specific languages (DSLs) for
10/P10008.
clinical data transformation remain difficult for LLMs
to explore and generate. For example, FHIRcon- [2] Anthropic. Model context protocol specification,
nect [34] defines a DSL for bidirectional mappings be- 2024. URL https://modelcontextprotocol.io/.
tweenopenEHRandHL7FHIR,ataskrequiringprecise Open standard, donated to Linux Foundation
navigation of archetype hierarchies, profile constraints, (AAIF) in December 2025.
andcross-standardtypecorrespondences. CurrentLLMs
[3] PaulGauthier. Aider: AIpairprogramminginyour
struggletogeneratecorrectmappingcodewithoutstruc-
tural context about the DSL’s type system and trans-
terminal,2023. URLhttps://aider.chat/. Open-
source tool. Uses Tree-Sitter-based RepoMap with
formation rules. Extending Codebase-Memory with
PageRank for context selection.
grammarsforsuchDSLscouldexposemappingrelation-
ships, archetype dependencies, and profile constraints as [4] JielinQiu,ZuxinLiu,ZhiweiLiu,etal. LoCoBench-
graph-queryableentities, enablingLLMagentstoreason Agent: An interactive benchmark for LLM
about data integration tasks with the same structural agents in long-context software engineering, 2025.
precision demonstrated for general-purpose languages in URL https://arxiv.org/abs/2511.13998. arXiv
this work. preprint.
[5] Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin
6 Conclusion Paranjape, Michele Bevilacqua, Fabio Petroni, and
Percy Liang. Lost in the middle: How language
Codebase-Memory demonstrates that treating code
modelsuselongcontexts. Transactions of the Asso-
structure as a first-class, queryable graph, rather than
ciation for Computational Linguistics (TACL), 12:
text to be searched, delivers order-of-magnitude effi-
157–173, 2024. doi: 10.1162/tacl_a_00638.
ciency gains with competitive accuracy. A multi-phase
Tree-Sitterpipelinewithparallelworkerpools,6-strategy [6] Nicolas Hrubec. Reducing token usage of
call resolution, and Louvain community detection pro- software engineering agents, 2025. URL
duce a rich knowledge graph queryable in under a mil- https://repositum.tuwien.at/handle/20.
lisecond,exposedtoanyMCP-compatibleagentwithout 500.12708/224666. Diploma thesis, TU Wien.
infrastructure overhead. Implemented as a single stat-
[7] John Yang, Carlos E. Jimenez, Alexander Wettig,
ically linked C binary with zero dependencies, the sys-
Kilian Lieret, Shunyu Yao, Karthik Narasimhan,
temscalesfromsmallprojectstotheLinuxkernel(2.1M
and Ofir Press. SWE-agent: Agent-computer in-
nodesin∼3minutes). Attentimeslowertokencostand
terfaces enable automated software engineering. In
2.1 times fewer tool calls across 31 languages, structural
AdvancesinNeuralInformationProcessingSystems
retrieval provides a viable foundation for LLM-based
(NeurIPS),volume37,2024. URLhttps://arxiv.
codeintelligence. Beyondefficiency,thesystemaddresses
org/abs/2405.15793.
the emerging supply-chain trust challenge of MCP tool
ecosystemsthroughanautomated,zero-tolerancerelease [8] Yuntong Zhang, Haifeng Ruan, Zhiyu Fan, and Ab-
verification pipeline integrating industry-standard an- hik Roychoudhury. AutoCodeRover: Autonomous
tivirus scanning, build provenance, and dependency in- program improvement. In Proceedings of the 33rd
tegrity checks—a level of binary verification not com- ACM SIGSOFT International Symposium on Soft-
monly found in open-source developer tools. Early com- ware Testing and Analysis (ISSTA), 2024. doi:
munityadoption(Section4.4)confirmspracticaldemand 10.1145/3650212.3680384. URL https://arxiv.
for this approach. org/abs/2404.05427.
8

[9] ChunqiuStevenXia,YinlinDeng,SorenDunn,and (EMNLP), 2023. URL
https://arxiv.org/abs/
| Lingming                        |                 | Zhang. | Agentless: |               | Demystifying    |           | LLM-   | 2303.12570. |       |        |           |     |            |            |
| ------------------------------- | --------------- | ------ | ---------- | ------------- | --------------- | --------- | ------ | ----------- | ----- | ------ | --------- | --- | ---------- | ---------- |
| basedsoftwareengineeringagents. |                 |        |            |               | InProceedingsof |           |        |             |       |        |           |     |            |            |
|                                 |                 |        |            |               |                 |           | [18]   | Shuyan      | Zhou, |        | Uri Alon, |     | Frank F.   | Xu, Zheng- |
| the                             | 33rd            | ACM    | SIGSOFT    | International |                 | Symposium |        |             |       |        |           |     |            |            |
|                                 |                 |        |            |               |                 |           |        | bao         | Wang, | Zhiruo | Jiang,    |     | and Graham | Neubig.    |
| on                              | the Foundations |        | of         | Software      | Engineering     |           | (FSE), |             |       |        |           |     |            |            |
2025. doi: 10.1145/3715754. URL DocPrompting: Generating code by retrieving the
https://arxiv.
|     |     |     |     |     |     |     |     | docs. | In Proceedings |     | of  | the 11th | International | Con- |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | -------------- | --- | --- | -------- | ------------- | ---- |
org/abs/2407.01489.
|     |     |     |     |     |     |     |     |         |     |          |                 |     | (ICLR), | 2023. |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | -------- | --------------- | --- | ------- | ----- |
|     |     |     |     |     |     |     |     | ference | on  | Learning | Representations |     |         |       |
[10] Fabian Yamaguchi, Nico Golde, Daniel Arp, and URL https://arxiv.org/abs/2207.05987.
| Konrad   |          | Rieck. | Modeling  | and     | discovering | vulnera-    |      |           |      |      |             |     |             |            |
| -------- | -------- | ------ | --------- | ------- | ----------- | ----------- | ---- | --------- | ---- | ---- | ----------- | --- | ----------- | ---------- |
|          |          |        |           |         |             |             | [19] | Yicheng   | Tao, | Yao  | Qin,        | and | Yepang Liu. | Retrieval- |
| bilities | with     | code   | property  | graphs. | In          | Proceedings |      |           |      |      |             |     |             |            |
|          |          |        |           |         |             |             |      | augmented |      | code | generation: |     | A survey    | with focus |
| of       | the 2014 | IEEE   | Symposium | on      | Security    | and         | Pri- |           |      |      |             |     |             |            |
(S&P), pages 590–604, 2014. doi: 10.1109/SP. on repository-level approaches, 2025. URL https:
vacy
|     |     |     |     |     |     |     |     | //arxiv.org/abs/2510.04905. |     |     |     |     | arXiv | preprint. |
| --- | --- | --- | --- | --- | --- | --- | --- | --------------------------- | --- | --- | --- | --- | ----- | --------- |
2014.44.
|            |             |     |      |          |         |     | [20] | Wei | Liu, Ailun |     | Yu, et | al. | GraphCoder: | Enhanc- |
| ---------- | ----------- | --- | ---- | -------- | ------- | --- | ---- | --- | ---------- | --- | ------ | --- | ----------- | ------- |
| [11] Pavel | Avgustinov, |     | Oege | de Moor, | Michael |     | Pey- |     |            |     |        |     |             |         |
ton Jones, and Max Sherr. QL: Object-oriented ing repository-level code completion via coarse-to-
|               |          |            |            |                    |                 |     |        | fine     | retrieval | based                    | on       | code     | context graph. | In     |
| ------------- | -------- | ---------- | ---------- | ------------------ | --------------- | --- | ------ | -------- | --------- | ------------------------ | -------- | -------- | -------------- | ------ |
| queries       | on       | relational | data.      | In                 | Proceedings     |     | of the |          |           |                          |          |          |                | Pro-   |
|               |          |            |            |                    |                 |     |        | ceedings | of        | the 39th                 | IEEE/ACM |          | International  | Con-   |
| 30th          | European |            | Conference | on Object-Oriented |                 |     | Pro-   |          |           |                          |          |          |                |        |
|               |          |            |            |                    |                 |     |        | ference  | on        | Automated                |          | Software | Engineering    | (ASE), |
| gramming      |          | (ECOOP),   |            | 2016. doi:         | 10.4230/LIPIcs. |     |        |          |           |                          |          |          |                |        |
|               |          |            |            |                    |                 |     |        | 2024.    | doi:      | 10.1145/3691620.3695054. |          |          |                | URL    |
| ECOOP.2016.2. |          |            |            |                    |                 |     |        |          |           |                          |          |          |                | https: |
//arxiv.org/abs/2406.07003.
| [12] Boyang | Yang, |     | Jiadong | Ren, Shunfu | Jin, | Yang | Liu, |     |     |     |     |     |     |     |
| ----------- | ----- | --- | ------- | ----------- | ---- | ---- | ---- | --- | --- | --- | --- | --- | --- | --- |
Feng Liu, Bach Le, and Haoye Tian. Enhancing [21] Xiangyan Liu, Bo Peng, et al. CodexGraph: Bridg-
|     |     |     |     |     |     |     |     | ing large | language |     | models | and | code repositories | via |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | -------- | --- | ------ | --- | ----------------- | --- |
repository-levelsoftwarerepairviarepository-aware
knowledgegraphs,2025.URLhttps://arxiv.org/ code graph databases. In Proceedings of the 2025
|                 |     |     |       |           |     |     |     | Annual | Conference |     | of  | the North | American | Chap- |
| --------------- | --- | --- | ----- | --------- | --- | --- | --- | ------ | ---------- | --- | --- | --------- | -------- | ----- |
| abs/2503.21710. |     |     | arXiv | preprint. |     |     |     |        |            |     |     |           |          |       |
teroftheAssociationforComputationalLinguistics
[13] Pratik Shah, Rajat Ghosh, Aryan Singhal, and De- (NAACL), 2025. URL https://arxiv.org/abs/
| bojyoti                     | Dutta.         |     | RANGER:    | Repository-level |       |           | agent | 2408.03910.                              |       |      |       |      |           |        |
| --------------------------- | -------------- | --- | ---------- | ---------------- | ----- | --------- | ----- | ---------------------------------------- | ----- | ---- | ----- | ---- | --------- | ------ |
| for                         | graph-enhanced |     | retrieval, | 2025.            | URL   | https:    |       |                                          |       |      |       |      |           |        |
|                             |                |     |            |                  |       |           | [22]  | SichaoOuyang,DongWang,RongxinWeng,Xiaobo |       |      |       |      |           |        |
| //arxiv.org/abs/2509.25257. |                |     |            |                  | arXiv | preprint. |       |                                          |       |      |       |      |           |        |
|                             |                |     |            |                  |       |           |       | Long,                                    | Yukun | Xue, | Haina | Gao, | Shaoguang | Zhong, |
[14] MaxBrunsfeld. Tree-sitter: Anincrementalparsing Wenjie Liu, Chengcheng Li, and Gang Cui. Re-
system for programming tools, 2018. URL https: poGraph: Enhancing AI software engineering with
//tree-sitter.github.io/tree-sitter/. Open- repository-level code graph. In Proceedings of the
| source      | project.  |     | Presented | at Strange     | Loop | 2018. |        |            |               |         |            |     |                    |        |
| ----------- | --------- | --- | --------- | -------------- | ---- | ----- | ------ | ---------- | ------------- | ------- | ---------- | --- | ------------------ | ------ |
|             |           |     |           |                |      |       |        | 13th       | International |         | Conference |     | on Learning        | Repre- |
|             |           |     |           |                |      |       |        | sentations |               | (ICLR), | 2025.      |     | URL https://arxiv. |        |
| [15] Jeanne | Ferrante, |     | Karl      | J. Ottenstein, |      | and   | Joe D. |            |               |         |            |     |                    |        |
org/abs/2410.14684.
| Warren. |     | The | program | dependence | graph | and | its |     |     |     |     |     |     |     |
| ------- | --- | --- | ------- | ---------- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
use in optimization. [23] Zhaoling Chen, Robert Tang, Gangda Deng, Fang
|     |     |     |     | ACM Transactions |     | on  | Pro- |     |     |     |     |     |     |     |
| --- | --- | --- | --- | ---------------- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
grammingLanguagesandSystems(TOPLAS),9(3): Wu, Jialong Wu, Zhiwei Jiang, Viktor Prasanna,
319–349, 1987. doi: 10.1145/24039.24041. Arman Cohan, and Xingyao Wang. LocAgent:
|            |           |            |          |                     |              |     |        | Graph-guided   |     | LLM                            | agents        |      | for code       | localization. |
| ---------- | --------- | ---------- | -------- | ------------------- | ------------ | --- | ------ | -------------- | --- | ------------------------------ | ------------- | ---- | -------------- | ------------- |
| [16] Yilin | Zhang,    |            | Xinran   | Zhao, Zora          | Zhiruo       |     | Wang,  |                |     |                                |               |      |                |               |
|            |           |            |          |                     |              |     |        | In Proceedings |     | of                             | the           | 63rd | Annual Meeting | of the        |
| Chenyang   |           | Yang,      | Jiayi    | Wei, and            | Tongshuang   |     | Wu.    |                |     |                                |               |      |                | (ACL),        |
|            |           |            |          |                     |              |     |        | Association    |     | for                            | Computational |      | Linguistics    |               |
| cAST:      | Enhancing |            | code     | retrieval-augmented |              |     | gener- |                |     |                                |               |      |                |               |
|            |           |            |          |                     |              |     |        | 2025.          | URL | https://aclanthology.org/2025. |               |      |                |               |
| ation      | with      | structural | chunking |                     | via abstract |     | syntax |                |     |                                |               |      |                |               |
acl-long.426/.
| tree. | In  | Findings | of the | Association | for | Computa- |     |     |     |     |     |     |     |     |
| ----- | --- | -------- | ------ | ----------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
2025, 2025. doi: 10. [24] Jia Li et al. GraphCodeAgent: Dual graph-guided
| tional | Linguistics: |     | EMNLP |     |     |     |     |     |     |     |     |     |     |     |
| ------ | ------------ | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
18653/v1/2025.findings-emnlp.430. URL https:// LLM agent for retrieval-augmented repo-level code
aclanthology.org/2025.findings-emnlp.430/. generation, 2025. URL https://arxiv.org/abs/
|             |        |     |           |            |       |        |     | 2504.10046. |     | arXiv | preprint. |     |     |     |
| ----------- | ------ | --- | --------- | ---------- | ----- | ------ | --- | ----------- | --- | ----- | --------- | --- | --- | --- |
| [17] Fengji | Zhang, |     | Bei Chen, | Yue Zhang, | Jacky | Keung, |     |             |     |       |           |     |     |     |
Jin Liu, Daoguang Zan, Yi Mao, Jian-Guang Lou, [25] Yue Pan, Zhaoling Chen, Arman Cohan, and
and Weizhu Chen. RepoCoder: Repository-level Xingyao Wang. Prometheus: Towards long-horizon
codecompletionthroughiterativeretrievalandgen- codebase navigation via unified knowledge graphs
eration. In Proceedings of the 2023 Conference on formultilingualissueresolution, 2025. URLhttps:
Empirical Methods in Natural Language Processing //arxiv.org/abs/2507.19942. arXiv preprint.
9

[26] Tsvi Cherny-Shahar and Amiram Yehudai. Reposi- and Shujie Liu. ReACC: A retrieval-augmented
tory intelligence graph: Deterministic architectural code completion framework. In Proceedings of the
| map | for LLM | code | assistants, | 2026. | URL |        |             |         |                    |     |          |
| --- | ------- | ---- | ----------- | ----- | --- | ------ | ----------- | ------- | ------------------ | --- | -------- |
|     |         |      |             |       |     | https: | 60th Annual | Meeting | of the Association |     | for Com- |
//arxiv.org/abs/2601.10112. arXiv preprint. putational Linguistics (ACL), 2022. URL https:
//arxiv.org/abs/2203.07722.
| [27] Wuyang | Zhang, | Chenkai |     | Zhang, | Zhen | Luo, Jian- |     |     |     |     |     |
| ----------- | ------ | ------- | --- | ------ | ---- | ---------- | --- | --- | --- | --- | --- |
mingMa,WangmingYuan,ChuqiaoGu,andChen- [34] Severin Kohler, Raphael Bild, Alexander Kiel,
wei Feng. SemanticForge: Repository-level code Stefan Stengel, and Dominik Heider. FHIRcon-
generation through semantic knowledge graphs and nect: A bidirectional transformation engine be-
constraintsatisfaction,2025. URLhttps://arxiv. tween openEHR and HL7 FHIR. arXiv preprint
|                     |     |     |       |           |     |     | arXiv:2511.14618, | 2025. | URL |                |     |
| ------------------- | --- | --- | ----- | --------- | --- | --- | ----------------- | ----- | --- | -------------- | --- |
| org/abs/2511.07584. |     |     | arXiv | preprint. |     |     |                   |       |     | https://arxiv. |     |
org/abs/2511.14618.
[28] HongyuanTao,YingZhang,ZhenhaoTang,Hongen
Peng,XukunZhu,BingchangLiu,YingguangYang,
| Ziyin | Zhang,   | Zhaogui | Xu, | Haipeng    | Zhang,     | Linchao |     |     |     |     |     |
| ----- | -------- | ------- | --- | ---------- | ---------- | ------- | --- | --- | --- | --- | --- |
| Zhu,  | RuiWang, | HangYu, |     | JianguoLi, | andPengDi. |         |     |     |     |     |     |
Codegraphmodel(CGM):Agraph-integratedlarge
| language                 |        | model for | repository-level |                     | software | engi-   |     |     |     |     |     |
| ------------------------ | ------ | --------- | ---------------- | ------------------- | -------- | ------- | --- | --- | --- | --- | --- |
| neering                  | tasks, | 2025.     | URL              | https://openreview. |          |         |     |     |     |     |     |
| net/forum?id=b98ODdeYq5. |        |           |                  | OpenReview          |          | submis- |     |     |     |     |     |
sion.
| [29] Carlos  | E.                 | Jimenez,   | John       | Yang,                | Alexander      | Wettig, |     |     |     |     |     |
| ------------ | ------------------ | ---------- | ---------- | -------------------- | -------------- | ------- | --- | --- | --- | --- | --- |
| Shunyu       | Yao,               | Kexin      | Pei,       | Ofir Press,          | and            | Karthik |     |     |     |     |     |
| Narasimhan.  |                    | SWE-bench: |            | Canlanguagemodelsre- |                |         |     |     |     |     |     |
| solve        | real-world         | GitHub     | issues?    |                      | In Proceedings | of      |     |     |     |     |     |
| the          | 12th International |            | Conference |                      | on Learning    | Rep-    |     |     |     |     |     |
| resentations |                    | (ICLR),    | 2024.      | URL                  | https://arxiv. |         |     |     |     |     |     |
org/abs/2310.06770.
| [30] Xingyao | Wang,         | Yangyi  | Chen,      | Lifan  | Yuan,          | Yizhe     |     |     |     |     |     |
| ------------ | ------------- | ------- | ---------- | ------ | -------------- | --------- | --- | --- | --- | --- | --- |
| Zhang,       | Yunzhu        | Li,     | Hao Peng,  | and    | Heng           | Ji. Open- |     |     |     |     |     |
| Hands:       | An            | open    | platform   | for AI | software       | devel-    |     |     |     |     |     |
| opers        | as generalist |         | agents.    | In     |                |           |     |     |     |     |     |
|              |               |         |            |        | Proceedings    | of the    |     |     |     |     |     |
| 13th         | International |         | Conference | on     | Learning       | Repre-    |     |     |     |     |     |
|              |               | (ICLR), | 2025.      | URL    |                |           |     |     |     |     |     |
| sentations   |               |         |            |        | https://arxiv. |           |     |     |     |     |     |
org/abs/2407.16741.
[31] HuiqiangJiang,QianhuiWu,Chin-YewLin,Yuqing
| Yang,     | and | Lili Qiu.   | LLMLingua:                 |          | Compressing |            |     |     |     |     |     |
| --------- | --- | ----------- | -------------------------- | -------- | ----------- | ---------- | --- | --- | --- | --- | --- |
| prompts   | for | accelerated | inference                  |          | of large    | language   |     |     |     |     |     |
| models.   | In  | Proceedings | of                         | the 2023 | Conference  | on         |     |     |     |     |     |
| Empirical |     | Methods     | in Natural                 | Language |             | Processing |     |     |     |     |     |
| (EMNLP),  |     | 2023.       | URL https://arxiv.org/abs/ |          |             |            |     |     |     |     |     |
2310.05736.
| [32] Zhuoshi                            | Pan,          | Qianhui     | Wu,          | Huiqiang | Jiang,        | et al.      |     |     |     |     |     |
| --------------------------------------- | ------------- | ----------- | ------------ | -------- | ------------- | ----------- | --- | --- | --- | --- | --- |
| LLMLingua-2:                            |               | Data        | distillation |          | for efficient | and         |     |     |     |     |     |
| faithfultask-agnosticpromptcompression. |               |             |              |          |               | InFind-     |     |     |     |     |     |
| ings                                    | of the        | 62nd Annual | Meeting      |          | of the        | Association |     |     |     |     |     |
| for                                     | Computational |             | Linguistics  | (ACL),   |               | 2024. URL   |     |     |     |     |     |
https://arxiv.org/abs/2403.12968.
| [33] Shuai | Lu,           | Daya        | Guo, Shuo | Ren,   | Junjie  | Huang, |     |     |     |     |     |
| ---------- | ------------- | ----------- | --------- | ------ | ------- | ------ | --- | --- | --- | --- | --- |
| Alexey     | Svyatkovskiy, |             | Ambrosio  |        | Blanco, | Colin  |     |     |     |     |     |
| Clement,   |               | Dawn Drain, | Daxin     | Jiang, | Duyu    | Tang,  |     |     |     |     |     |
| Ge         | Li, Lidong    | Zhou,       | Linjun    | Shou,  | Long    | Zhou,  |     |     |     |     |     |
MicheleTufano,MingGong,MingZhou,NanDuan,
| Neel | Sundaresan, |     | Shao Kun | Deng, | Shengyu | Fu, |     |     |     |     |     |
| ---- | ----------- | --- | -------- | ----- | ------- | --- | --- | --- | --- | --- | --- |
10
