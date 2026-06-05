# dotfiles: Reproducible Research Environment

**Infrastructure as Code for Reproducible Science**

This repository automates the provisioning of standardized research environments, ensuring that local development (macOS) and remote training (HPC) share strictly consistent dependencies. It integrates:

1. **Local NLP**: An offline RAG pipeline (Gemma 2) for private, semantic search over research literature.
2. **Writing Automation**: A continuous LaTeX build system for real-time manuscript validation.
3. **Rapid Reference**: Instant fuzzy retrieval for opening canonical textbooks, citations, and knowledge graphs (Obsidian).

Designed to minimize technical friction and guarantee experimental reproducibility.

## System Architecture

```text
├── manifests/          # Declarative lists of system packages (Brew, Python, Obsidian)
├── llm-config/         # Local LLM model weights and version-controlled configurations
├── configs/
│   └── nvim/           # Neovim config (symlinked to ~/.config/nvim)
├── scripts/
│   ├── installers/
│   │   └── install_file.sh  # Universal script installer
│   └── local_rag/      # Custom pipeline for offline literature retrieval
└── keyboard/           # Low-level input remapping
```

## Installation

### Installing scripts globally

Use `install_file.sh` to install any script to `~/bin`:

```bash
./scripts/installers/install_file.sh <script> [command-name]
```

Example — install the RAG pipeline:

```bash
./scripts/installers/install_file.sh scripts/local_rag/local_rag.py rag
```

### Symlinking nvim config

```bash
ln -s ~/gitCode/dotfiles/configs/nvim ~/.config/nvim
```

## Core Research Capabilities

### 1. Reproducibility & Environmental Consistency
**Objective:** Eliminate the "works on my machine" class of failures that plague collaborative research.  
By replacing imperative setup commands with declarative manifest files (`manifests/`), this system guarantees that the local development environment and remote training nodes are mathematically identical, preventing **environmental drift** across heterogeneous hardware.

### 2. Data Sovereignty & Zero-Egress Inference
**Objective:** Enable the analysis of sensitive, embargoed, or clinical data (e.g., MIMIC-IV) without compliance risks.  
The environment provisions a completely air-gapped **inference stack** (Gemma 2 via Ollama) and a local RAG pipeline, ensuring **zero data egress** for confidential datasets where cloud-based APIs are legally or ethically prohibited.

### 3. Resilient Remote Workflow
**Objective:** Mitigate the productivity loss caused by unstable connections to High-Performance Computing (HPC) clusters.  
Optimized for headless operation on HPC clusters (e.g., NYU Greene), employing **session persistence** via Tmux to decouple the user interface from execution state across network interruptions.

## Research Utilities

### Offline Retrieval-Augmented Generation (RAG)
**Utility:** Conversational interrogation of dense technical papers without internet dependency.  
**Implementation:** `scripts/local_rag/local_rag.py` — uses ChromaDB and SentenceTransformers for semantic search over local PDF collections, with recursive search across subdirectories.

```bash
./scripts/installers/install_file.sh scripts/local_rag/local_rag.py rag
rag ~/Documents/Textbooks "your query"
```

### Automated LaTeX Compilation Pipeline
**Utility:** Decouples paper writing from cloud editors, providing a live editor experience with instant feedback.  
**Implementation:** `scripts/compile_latex` — continuous build wrapper using filesystem monitoring for incremental compilation.

### High-Throughput PDF Search
**Utility:** Rapid screening of literature for formulas, citations, or keywords across gigabytes of PDFs.  
**Implementation:** `scripts/search_pdfs_no_llm` — multi-threaded keyword spotter generating structured HTML reports.

### Heuristic Resource Retrieval
**Utility:** Instantaneous access to reference materials without navigating file hierarchies.  
**Implementation:** `scripts/search_textbooks_by_name` — CLI fuzzy matcher resolving partial queries to immediate file access.