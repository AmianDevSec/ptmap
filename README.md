# ptmap

An asynchronous path traversal fuzzer for discovering and testing path traversal vulnerabilities in web applications.

## Overview

**ptmap** is a powerful command-line tool designed for security professionals and penetration testers to identify path traversal vulnerabilities through intelligent payload generation and fuzzing. Built with Python 3.10+, it leverages async/await patterns for high-performance concurrent testing across multiple targets.

## Features

- 🚀 **Asynchronous Fuzzing**: Concurrent worker threads for efficient vulnerability testing
- 🎯 **Multiple Input Methods**: Direct URLs, file-based target lists, or piped input
- 🧬 **Flexible Payload Generation**: Built-in and custom payload mutators
- 🔧 **Configurable Traversal**: Adjustable depth and payload size parameters
- 🛡️ **Multi-Platform Support**: Optimized payloads for Linux and Windows targets
- 📊 **Rich CLI Output**: Beautiful terminal output with real-time results

## Installation

```bash
pip install ptmap
```

**Requirements:**
- Python 3.10+
- aiohttp >= 3.9.0
- rich >= 13.0.0
- typer >= 0.12.0
- pyfiglet >= 1.0.0

## Quick Start

### Basic Usage

```bash
# Test a single URL
ptmap https://site.com/page?file=img.png

# Test multiple targets from a file
ptmap urls.txt

# Pipe targets from another tool
cat urls.txt | ptmap
katana https://example.com | ptmap
```

## Usage Guide

### Command Syntax

```
Usage: ptmap [OPTIONS] [TARGET]

Arguments:
  [TARGET]  Target URL or file containing newline-separated target URLs
            (e.g.: https://example.com:8080 or targets.txt)
```

### Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--custom-payloads` | `-cp` | TEXT | - | Path to a custom payload file. If omitted, built-in payload generation is used |
| `--size` | `-s` | INTEGER | - | Request payload size |
| `--threads` | `-t` | INTEGER | 10 | Number of concurrent worker threads |
| `--max-depth` | `-md` | INTEGER | 10 | Maximum traversal depth for payload generation |
| `--platform` | `-pf` | linux\|windows | linux | Target operating system |
| `--payloads` | `-p` | TEXT | traverse,urlencode | Comma-separated list of payload mutators |
| `--help` | - | - | - | Show help message |

### Available Payload Mutators

- `traverse`: Basic path traversal patterns
- `urlencode`: URL encoding mutations
- `double_urlencode`: Double URL encoding
- `overlong_utf8`: UTF-8 encoding variations
- `nested_slashes`: Nested slash patterns
- `encode_dots`: Dot encoding mutations
- `nullbyte`: Null byte injection
- `direct_path`: Direct path patterns
- `all`: Enable all available mutators

### Input Methods

| Method | Example | Description |
|--------|---------|-------------|
| **Direct URL** | `ptmap https://site.com/page?file=img.png` | Test a single target URL |
| **File Input** | `ptmap urls.txt` | Test targets from a newline-separated file |
| **Piped Input** | `cat urls.txt \| ptmap` | Receive targets from stdin |
| **Piped Tools** | `katana https://example.com \| ptmap` | Integrate with other security tools |

## Examples

### Basic Path Traversal Test
```bash
ptmap https://vulnerable-site.com/download?file=document.pdf
```

### Advanced Fuzzing with Custom Settings
```bash
ptmap targets.txt \
  --threads 20 \
  --max-depth 15 \
  --payloads all \
  --platform windows
```

### Using Custom Payloads
```bash
ptmap https://example.com \
  --custom-payloads custom_payloads.txt \
  --threads 15
```

### Integration with Reconnaissance Tools
```bash
# Find endpoints with katana, then fuzz with ptmap
katana -u https://example.com -d 3 | ptmap --threads 25

# Combine with URL filtering
cat urls.txt | grep "/download" | ptmap --payloads all
```

### Targeting Windows Systems
```bash
ptmap windows_targets.txt \
  --platform windows \
  --max-depth 12
```

## Configuration

### Custom Payload File Format

Create a custom payload file with newline-separated payloads:
```
../../../etc/passwd
..\\..\\..\\windows\\system32\\config\\sam
%2e%2e%2f%2e%2e%2fetc%2fpasswd
```

## Requirements

- **Python**: 3.10 or higher
- **aiohttp**: Asynchronous HTTP client library
- **rich**: Terminal output formatting
- **typer**: CLI framework
- **pyfiglet**: ASCII art generation

## License

This project is licensed under the GNU General Public License v3 (GPLv3) - see the LICENSE file for details.

## Author

**AmianDevSec**  
Email: amiandevsec@gmail.com

## Support & Community

If you find ptmap helpful in your security research, consider supporting the project:

- ⭐ **Star the repository** on GitHub to show appreciation
- 🐛 **Report bugs** and suggest features via GitHub Issues
- 🔀 **Contribute** improvements through pull requests
- 📝 **Share feedback** and use cases with the community
- 💬 **Engage** in discussions to help improve the tool

Your feedback and contributions help make ptmap better for everyone!

---

**Disclaimer**: This tool is intended for authorized security testing and educational purposes only. Unauthorized access to computer systems is illegal. Always obtain proper authorization before testing.
