# `awesome-deep-research` 🤖🔍

[![Automated Updates](https://github.com/ww/awesome-deep-research/actions/workflows/update-stars.yml/badge.svg)](https://github.com/ww/awesome-deep-research/actions/workflows/update-stars.yml)
[![Code Quality](https://github.com/ww/awesome-deep-research/actions/workflows/quality.yml/badge.svg)](https://github.com/ww/awesome-deep-research/actions/workflows/quality.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13.2](https://img.shields.io/badge/python-3.13.2-blue.svg)](https://www.python.org/downloads/release/python-3132/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Test Coverage: 90%+](https://img.shields.io/badge/coverage-90%25%2B-brightgreen.svg)](https://pytest-cov.readthedocs.io/)

---

> A curated list of AI-powered research tools and platforms, with automated tracking of GitHub stars and feature comparisons.

---

## 📊 Data Table

| name | summary | interface | UI Available | Feature Highlights | dependencies | Setup Requirements | documentation_quality | maintenance_status | Key Differentiator | links | SERPAPI | JINA_AI | OPENROUTER | OPENAI | GEMINI | FIRECRAWL | BING | BRAVE | ANTHROPIC |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| OpenDeepResearcher | OpenDeepResearcher is an AI research assistant that iteratively refines search queries to extract, evaluate, and compile comprehensive research reports | Jupyter Notebooks and Gradio web interface | Yes | • Iterative research loop<br>• Asynchronous processing<br>• Duplicate filtering<br>• LLM decision making<br>• Gradio interface | Python 3, aiohttp, asyncio, nest_asyncio, gradio | Requires Python environment, API keys configuration | High | Active | Combines multiple APIs with asynchronous processing | [GitHub](https://github.com/mshumer/OpenDeepResearcher), [X Post](https://x.com/mattshumer_/status/1886558939434664404) | True | True | True | True | False | False | False | False | False |
| GPT-Researcher | Advanced research automation tool with citation management | Python CLI and Web UI | Yes | • Detailed research reports<br>• Citation management<br>• Multiple search modes | GPT-3.5/4, Python, BeautifulSoup | Python environment, OpenAI API key | High | Active | Advanced citation system | [GitHub](https://github.com/assafelovic/gpt-researcher) | False | False | False | True | False | False | True | False | False |
| Stanford STORM | Academic research platform with multi-agent discussions | Web Interface | Yes | • Multi-agent discussions<br>• Expert simulation<br>• Wikipedia-style reports | Custom LLM, Python | None - Web based | High | Research | Academic quality research simulation | [Website](https://storm-project.stanford.edu/) | False | False | False | False | False | False | False | False | False |
| Jina Node-DeepResearch | Node.js based deep research tool with iterative search capabilities | Node.js API | Yes | • Iterative search<br>• Token budget mgmt<br>• Web reasoning | Node.js | Node.js environment | Medium | Active | Fast Node.js implementation | [GitHub](https://github.com/jina-ai/node-DeepResearch) | False | True | False | False | False | False | False | False | False |
| DZHNG Deep Research | Flexible deep research tool with adjustable parameters | Python API | Yes | • Adjustable depth/breadth<br>• Auto-timing<br>• Custom behavior | GPT-4, Python | Python environment, API keys | Medium | Active | Flexible control and timing | [GitHub](https://github.com/dzhng/deep-research) | False | False | True | True | False | False | False | False | False |
| Open-Deep-Research | Research tool with Firecrawl integration | Python API | No | • Firecrawl extraction<br>• Data reasoning<br>• Custom search | GPT-3.5/4, Python, Firecrawl | Python and Firecrawl setup | Medium | Maintained | Fast web crawling integration | [GitHub](https://github.com/nickscamara/open-deep-research) | False | False | False | True | False | True | False | False | False |
| AI-Web-Researcher-Ollama | Local LLM-based research tool | CLI | No | • Local LLM support<br>• Focus detection<br>• Result saving | Ollama, Python | Local Ollama setup | Medium | Active | Local LLM processing | [GitHub](https://github.com/TheBlewish/Automated-AI-Web-Researcher-Ollama) | False | False | False | False | False | False | False | False | False |
| Tahir-ODR | Gemini alternative research tool | Python API | No | • Gemini alternative<br>• Search integration<br>• Report generation | GPT-4, Python | Python environment | Low | Early Stage | Simple modern implementation | [GitHub](https://github.com/btahir/open-deep-research) | False | False | False | True | False | False | False | True | False |
| Standalone-GPT-Researcher | Simplified GPT research implementation | Python API | Yes | • Standalone fork<br>• Simplified setup<br>• Core features | GPT-4, Python | Python environment | Medium | Maintained | Easy standalone setup | [GitHub](https://github.com/avrtt/gpt-researcher) | False | False | False | True | False | False | True | False | False |
| OpenAI Deep Research | Professional research platform with GPT-4 Turbo | API & Web | Yes | • Pro report gen<br>• Advanced reasoning<br>• Multi-source synthesis | GPT-4 Turbo, O3 | API subscription | High | Active | State-of-art processing | [Docs](https://platform.openai.com/docs/deep-research) | False | False | False | True | False | False | False | False | False |
| Gemini Deep Research | Google's research platform with Gemini 2.0 | API & Web | Yes | • Real-time analysis<br>• Multi-modal<br>• Google integration | Gemini 2.0 | API subscription | High | Active | Google ecosystem integration | [Blog](https://blog.google/products/gemini/google-gemini-deep-research/) | False | False | False | False | True | False | False | False | False |
| Claude Research | Advanced research assistant with system control | API & Web | Yes | • Computer control<br>• Advanced reasoning<br>• Tool use | Claude 3 | API subscription | High | Active | System control capabilities | [Website](https://www.anthropic.com/claude) | False | False | False | False | False | False | False | False | True |
| Perplexity Pro | Real-time research platform | Web | Yes | • Real-time research<br>• Chat interface<br>• Quick results | GPT-4, Claude | Subscription | High | Active | User-friendly research | [Website](https://www.perplexity.ai/) | False | False | False | True | False | False | False | False | True |
| DeepSeek | Multi-modal research platform | Web | Yes | • Multi-modal research<br>• Advanced synthesis<br>• Academic focus | Custom, Claude | Subscription | High | Active | Deep analysis capabilities | [Website](https://deepseek.com/) | False | False | False | False | False | False | False | False | True |
| You.com Research | AI-powered search and research | Web | Yes | • AI search<br>• App integration<br>• Web tools | Custom | None | Medium | Active | App ecosystem integration | [Website](https://you.com/) | False | False | False | False | False | False | False | True | False |
| Operator | Enterprise autonomous research platform | API & Web | Yes | • Autonomous research<br>• Task automation<br>• Advanced reasoning | GPT-4, Custom | Enterprise access | High | Active | Full research autonomy | [Website](https://operator.openai.com) | False | False | False | True | False | False | False | False | False |
| NotebookLM | Google's AI-powered research assistant for document analysis and note-taking | Web Interface | Yes | • Document synthesis<br>• Context-aware responses<br>• PDF processing<br>• Smart summarization<br>• Source tracking | Gemini | Google account | High | Active | Deep document understanding and contextual awareness | [Website](https://notebooklm.google/) | False | False | False | False | True | False | False | False | False |
| Consensus | AI-powered academic search engine with paper synthesis | Web & ChatGPT Plugin | Yes | • 200M+ paper database<br>• GPT-4 synthesis<br>• Literature review<br>• Citation extraction<br>• Topic insights | GPT-4 | None - Web based | High | Active | Direct academic paper synthesis | [Website](https://consensus.app) | False | False | False | True | False | False | False | False | False |
| SciSpace | AI research platform for paper discovery and analysis | Web & ChatGPT Plugin | Yes | • Paper recommendations<br>• PDF analysis<br>• Citation management<br>• Related work discovery<br>• Smart summaries | Custom AI | None - Web based | High | Active | Comprehensive paper analysis and discovery | [Website](https://typeset.io) | False | False | False | False | False | False | False | False | False |
| Scholar GPT | ChatGPT plugin for academic research assistance | ChatGPT Plugin | Yes | • Paper summarization<br>• Key information extraction<br>• Research synthesis<br>• Citation support | GPT-4 | ChatGPT Plus subscription | Medium | Active | Focused academic paper analysis | [ChatGPT Plugin](https://chat.openai.com) | False | False | False | True | False | False | False | False | False |
| AgentLaboratory | End-to-end autonomous research workflow assistant | Python Framework | Yes | • Literature review<br>• Experiment design<br>• Code execution<br>• Report writing<br>• LLM-driven agents | Python, LLMs | Python environment | High | Active | Complete research workflow automation | [GitHub](https://github.com/SamuelSchmidgall/AgentLaboratory) | False | False | False | True | False | False | False | False | False |
| Elicit | AI research assistant focused on literature review and analysis | Web | Yes | • Literature discovery<br>• Paper analysis<br>• Study comparison<br>• Methodology extraction<br>• Research synthesis | Custom AI | None - Web based | High | Active | Research methodology analysis | [Website](https://elicit.org) | False | False | False | False | False | False | False | False | False |
| Scite.ai | Citation analysis and research validation platform | Web & Browser Extension | Yes | • Citation context analysis<br>• Smart citations<br>• Paper validation<br>• Reference checking<br>• Browser integration | Custom AI | None - Web based | High | Active | Smart citation analysis | [Website](https://scite.ai) | False | False | False | False | False | False | False | False | False |
| ResearchRabbit | Literature discovery and citation mapping tool | Web | Yes | • Citation mapping<br>• Paper recommendations<br>• Network visualization<br>• Collection management<br>• Collaboration features | Custom | None - Web based | High | Active | Visual citation mapping | [Website](https://researchrabbit.ai) | False | False | False | False | False | False | False | False | False |

\* Free for local LLM usage, API costs may apply for some models

## 🎯 Project Goals

1. **Curation**: Maintain an up-to-date list of high-quality research tools
2. **Comparison**: Provide detailed feature comparisons for informed choices
3. **Integration**: Track API integrations across major AI providers
4. **Automation**: Ensure data accuracy through automated updates
5. **Community**: Foster an active community of contributors

## 🗂 Categories

### Academic Research Tools
- Paper analysis and synthesis
- Citation management
- Literature review assistance

### Enterprise Solutions
- Autonomous research platforms
- Multi-modal analysis
- Advanced reasoning systems

### Local & Open Source
- Self-hosted options
- Local LLM integrations
- Community-driven tools

## 🛠 Development

### System Requirements
- Python 3.13.2 (specified in `.python-version`)
- [uv](https://github.com/astral-sh/uv) package manager
- GitHub API token (for star updates)
- Unix-like environment (macOS/Linux preferred)

### Quick Start
```bash
# Clone repository
git clone https://github.com/yourusername/awesome-deep-research.git
cd awesome-deep-research

# Install uv (if needed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Setup environment
make setup

# Run all checks
make ci
```

### Development Workflow

1. **Environment Setup**
   ```bash
   cp .env.example .env  # Configure environment
   make setup           # Install dependencies
   ```

2. **Code Quality**
   ```bash
   make format         # Format code
   make lint          # Run linters
   make test          # Run tests
   ```

3. **Data Updates**
   ```bash
   make update-stars  # Update star counts
   make update-table  # Regenerate table
   ```

### Project Structure
- `scripts/`: Core automation scripts
- `tests/`: Comprehensive test suite
- `.github/`: CI/CD and template configurations
- `table.csv`: Source data for comparisons

## 👥 Contributing

We welcome contributions! Please follow these steps:

1. **Fork & Clone**
   ```bash
   git clone https://github.com/yourusername/awesome-deep-research.git
   cd awesome-deep-research
   ```

2. **Setup Development Environment**
   ```bash
   make setup
   ```

3. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Changes**
   - Update `table.csv` for new entries
   - Follow code style guidelines
   - Add tests for new features

5. **Quality Checks**
   ```bash
   make ci  # Runs format, lint, and test
   ```

6. **Submit PR**
   - Use the PR template
   - Include clear description
   - Link related issues

### Contribution Guidelines

- Follow Python best practices (PEP 8)
- Maintain test coverage (90%+)
- Update documentation
- Use clear commit messages
- Add tests for new features

## 🔍 Feature Comparison Criteria

### UI/Interface Types
- CLI: Command-line interface
- API: Programmatic access
- Web: Browser-based interface
- Plugin: Integration capabilities

### API Integrations
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- Google (Gemini)
- Custom/Other

### Setup Complexity
- None: Web-based, no setup
- Basic: Simple API key setup
- Complex: Multiple dependencies

### Documentation Quality
- High: Comprehensive docs
- Medium: Basic coverage
- Low: Minimal documentation

## 📈 Maintenance Status

- **Active**: Regular updates
- **Maintained**: Occasional updates
- **Research**: Academic focus
- **Early Stage**: Under development

## 🔒 Security

- Environment variables for sensitive data
- Secure API key management
- No hardcoded credentials
- Regular dependency updates

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

## 🙏 Acknowledgments

- Tool creators and maintainers
- Open source community
- All contributors

---

<div align="center">
  <sub>Built with ❤️ by the AI research community</sub>
</div>

