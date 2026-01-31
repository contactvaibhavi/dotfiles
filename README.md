# dotfiles: Reproducible Research Environment

**Infrastructure as Code for Reproducible Science**

This repository automates the provisioning of standardized research environments, ensuring that local development (macOS) and remote training (HPC) share strictly consistent dependencies. It integrates:

1. **Local NLP**: An offline RAG pipeline (Gemma 2) for private, semantic search over research literature.

2. **Writing Automation**: A continuous LaTeX build system for real-time manuscript validation.

3. **Rapid Reference**: Instant fuzzy retrieval for opening canonical textbooks, citations, and knowledge graphs (Obsidian).

Designed to minimize technical friction and guarantee experimental reproducibility.

## System Architecture

The repository is structured to separate package declaration from installation logic, ensuring modularity and easier auditing of system dependencies.

```text
├── manifests/          # Declarative lists of system packages (Brew, Python, Obsidian)
├── llm-config/         # Local LLM model weights and version-controlled configurations
├── scripts/            # Idempotent automation logic
│   ├── install_file.sh # Module-level installer
│   ├── install_folder.sh # Batch provisioning utility
│   └── local_rag/      # Custom pipeline for offline literature retrieval
├── configs/            # Application-specific configurations (Tmux, Alacritty)
└── keyboard/           # Low-level input remapping
```

## Core Research Capabilities

### 1. Reproducibility & Environmental Consistency
**Objective:** Eliminate the "works on my machine" class of failures that plague collaborative research.
By replacing imperative setup commands with declarative manifest files (`manifests/`), this system guarantees that the local development environment and remote training nodes are mathematically identical. This prevents **environmental drift**—bugs caused by subtle version mismatches in CUDA, compilers, or Python libraries—ensuring that experimental results are strictly reproducible across heterogeneous hardware.

### 2. Data Sovereignty & Zero-Egress Inference
**Objective:** Enable the analysis of sensitive, embargoed, or clinical data (e.g., MIMIC-IV) without compliance risks.
The environment provisions a completely air-gapped **inference stack** (Gemma 2 via Ollama) and a local RAG pipeline. This architecture ensures **zero data egress**, allowing for the use of powerful LLM assistants on confidential datasets where cloud-based APIs (OpenAI/Anthropic) are legally or ethically prohibited.

### 3. Resilient Remote Workflow
**Objective:** Mitigate the productivity loss caused by unstable connections to High-Performance Computing (HPC) clusters.
Optimized for headless operation on supercomputers (e.g., NYU Greene), this workflow employs **session persistence** (via Tmux) to decouple the user interface from the execution state. This ensures that long-running training jobs and unsaved code changes survive network interruptions or VPN disconnects without process termination.

## Research Utilities

### Offline Retrieval-Augmented Generation (RAG)
**Utility:** Accelerates literature review by enabling conversational interrogation of dense technical papers without internet dependency.
**Impact:** Reduces the time required to synthesize findings from large collections of PDFs.
**Implementation:** A custom pipeline (`scripts/local_rag`) leverages **ChromaDB** and **SentenceTransformers** to provide low-latency, semantic search over local knowledge bases.

### Automated LaTeX Compilation Pipeline
**Utility:** Decouples paper writing from cloud-based editors (Overleaf), removing reliance on internet connectivity and third-party servers.
**Impact:** Provides a "live editor" experience with instant feedback, while enforcing version control on the source text.
**Implementation:** A continuous build wrapper (`scripts/compile_latex`) uses filesystem monitoring to trigger **incremental compilation** and manages artifact hygiene to keep repositories clean.

### High-Throughput PDF Search
**Utility:** Drastically reduces the time spent screening literature for specific formulas, citations, or keywords.
**Impact:** Enables rapid verification of prior art across gigabytes of unindexed PDFs where standard system tools are too slow or imprecise.
**Implementation:** A multi-threaded keyword spotter (`scripts/search_pdfs_no_llm`) that outperforms grep by parallelizing text extraction and generating structured HTML reports for review.

### Heuristic Resource Retrieval
**Utility:** Minimizes the friction of accessing standard reference materials during deep work sessions.
**Impact:** Eliminates the cognitive load of navigating file hierarchies, allowing for instantaneous context switching to textbooks.
**Implementation:** A CLI wrapper (`scripts/search_textbooks_by_name`) that uses **fuzzy string matching** to resolve partial mental queries (e.g., "deep learn") into immediate file access.
