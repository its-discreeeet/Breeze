# breeze
Your personal CLI Agent

'**breeze**' is an extensible command-line and Python tool for automating code understanding and transformation tasks across multiple programming languages. It leverages the advanced capabilities of Google's Gemini large language models (LLMs) to generate documentation, summaries, type annotations, tests, bug detection, refactoring, and more—all from your terminal or scripts.

## 🏗️ Architecture Overview
Below is the detailed architecture diagram of breeze, showing the flow from user input through the CLI, flow orchestration, agent nodes, utility layers, and the Google AI Cloud (zoom in to see everything to detail, its too big to view without any magnification) :

<img width="3840" height="1165" alt="breeze flowchart" src="https://github.com/user-attachments/assets/a31bff49-2f17-4d22-a937-1cd84d74ad51" />

## 🚀 Features
Core Capabilities
- 🔍 Multi-Language Support: Works with 20+ programming languages and file types
- 📝 Documentation Generation: Generate language-appropriate documentation (docstrings, JSDoc, Javadoc, etc.)
- 📊 Code Summarization: Get concise, intelligent summaries of your code files
- 🧪 Test Generation: Generate comprehensive unit tests using appropriate frameworks
- 🐛 Bug Detection: Analyze code for potential bugs, security issues, and performance problems
- ⚡ Code Refactoring: Suggest and apply code improvements following best practices
- 🏷️ Type Annotation: Add or update type annotations/declarations
- 🔄 Code Migration: Migrate code between versions, languages, and frameworks
- 💬 Interactive Chat Mode: Natural language interface for complex code tasks
- 🎯 Context Awareness: Intelligent understanding of code structure and relationships
- 📈 Progress Tracking: Verbose mode with detailed operation insights

## 🌐 Supported Languages & Technologies

### **💻 Programming Languages**

| Language | Extension | Documentation | Testing | Features |
|----------|-----------|---------------|---------|----------|
| **Python** | `.py` | Google-style docstrings | pytest | Type hints, PEP compliance |
| **JavaScript** | `.js` | JSDoc comments | Jest | ES6+, async/await patterns |
| **TypeScript** | `.ts` | TSDoc comments | Jest + TypeScript | Interface, generics, strict typing |
| **Java** | `.java` | Javadoc comments | JUnit | OOP patterns, streams, lambdas |
| **C++** | `.cpp`, `.cc` | Doxygen comments | Google Test | Modern C++, RAII, templates |
| **C** | `.c` | Doxygen comments | Unity Test | ANSI/C99/C11 standards |
| **C#** | `.cs` | XML documentation | NUnit/MSTest | Nullable references, LINQ |
| **PHP** | `.php` | PHPDoc comments | PHPUnit | PSR standards, type declarations |
| **Ruby** | `.rb` | YARD documentation | RSpec | Idiomatic patterns, metaprogramming |
| **Go** | `.go` | Go doc comments | Go testing | Interfaces, goroutines, idioms |
| **Rust** | `.rs` | Rust doc comments | Built-in tests | Ownership, lifetimes, traits |
| **Swift** | `.swift` | Swift documentation | XCTest | iOS/macOS development |
| **Kotlin** | `.kt` | KDoc comments | JUnit | Android development, coroutines |

### **🌐 Web & Data Technologies**

| Type | Extensions | Capabilities |
|------|------------|--------------|
| **Web** | `.html`, `.css`, `.scss` | Semantic markup, responsive design, accessibility |
| **Database** | `.sql` | Query optimization, security analysis, performance |
| **Data** | `.json`, `.xml`, `.yaml` | Structure validation, schema compliance |
| **Config** | `.toml`, `.ini`, `.conf` | Configuration analysis and validation |

### **🔧 Scripts & Tools**

| Type | Extensions | Platform |
|------|------------|----------|
| **Shell Scripts** | `.sh`, `.bash`, `.zsh` | Linux/macOS |
| **Batch Files** | `.bat`, `.cmd` | Windows |
| **PowerShell** | `.ps1` | Cross-platform |
| **Documentation** | `.md`, `.txt` | Universal |

### 🤖 Powered by Google's Gemini AI

- **Model**: Use appropriate Gemini API key of your choice - Optimized for code understanding and generation
- **Provider**: [Google AI for Developers](https://ai.google.dev/)
- **Why Gemini?**: Cuz its free duh

## 📦 Installation

### **Prerequisites**
- Python
- Google AI API key ([Get yours here](https://ai.google.dev/))

### **Install from Source**

### Clone the repository
```
git clone https://github.com/its-discreeeet/breeze.git
cd breeze
```
### Install dependencies
```
pip install -r requirements.txt
```

### Install in development mode
```
python -m pip install -e .
```
Setup API Key
For windows :
```
set GEMINI_API_KEY "your_api_key_here"
```

For linux/macOS :
export GEMINI_API_KEY="your_api_key_here"

### Verify Installation
```
breeze --help
breeze chat
```
## 🛠️ Usage Guide
Quick Start

#### **Available Commands**

NOTE: Kindly ensure that you provide the correct file paths when using the below cmds. I have provided a few test files in the **test** directory for you to use initially.

| Command | Description | Example |
|---------|-------------|---------|
| `doc` | Generate documentation | `breeze doc binarysearchtree.c` |
| `summarize` | Create code summary | `breeze summarize f1.py` |
| `test` | Generate unit tests | `breeze test api.java --output new-file` |
| `inspect` | Detect bugs and issues | `breeze inspect security.php` |
| `refactor` | Improve code structure | `breeze refactor legacy.cpp --secure` |
| `annotate` | Add type annotations | `breeze annotate api.ts` |
| `migrate` | Migrate code versions | `breeze migrate old.py --target "Python 3.12"` |
| `chat` | Interactive assistant | `breeze chat` |

#### **Global Options**

| Option | Description | Example |
|--------|-------------|---------|
| `--output MODE` | Set output mode: `console`, `in-place`, `new-file` | `--output in-place` |
| `--secure` | Require user approval for changes | `--secure` |
| `-v, --verbose` | Enable detailed logging | `--verbose` |
| `--help` | Show help information | `--help` |

#### **Command-Specific Options**

| Command | Option | Description | Example |
|---------|--------|-------------|---------|
| `migrate` | `--target` | Migration target | `--target "TypeScript"` |
