<div align="center">

# 🚀 Frappe Manager

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/frappe-manager.svg)](https://badge.fury.io/py/frappe-manager)

### Simplify Your Frappe Development & Deployment Workflow

*A powerful CLI tool that streamlines the entire lifecycle of Frappe applications using Docker - from development to deployment.*

[Quick Start](#quick-start) • [Documentation](https://github.com/rtCamp/Frappe-Manager/wiki) • [Examples](#examples) • [Support](#support)

</div>

![Frappe-Manager-Create-Site.svg](https://user-images.githubusercontent.com/28294795/283108791-0237d05a-2562-48be-987b-037a200d71a3.svg)

## ✨ Features

<table border="0" cellspacing="0" cellpadding="0">
<tr>
<td>
<h3>🔥 Easy Setup</h3>
• Get a new Frappe environment running in minutes<br>
• Zero configuration needed
</td>
<td>
<h3>🐳 Docker-Based</h3>
• Consistent environments across all platforms<br>
• Isolated development environments
</td>
<td>
<h3>🌐 Multi-Bench Support</h3>
• Manage multiple Frappe benches from one server
</td>
</tr>

<tr>
<td>
<h3>👨‍💻 Development Tools</h3>
• VSCode integration with debugger support<br>
• Automatic environment switching between dev/prod
</td>
<td>
<h3>🔒 SSL Management</h3>
• Built-in Let's Encrypt integration<br>
• Automatic certificate renewal
</td>
<td>
<h3>🛠️ Admin Tools</h3>
• Mailpit for email testing<br>
• Redis Queue Dashboard<br>
• Database management interface
</td>
</tr>

<tr>
<td>
<h3>⚙️ Process Management</h3>
• Supervisor integration for process control<br>
• Easy service restarts and monitoring
</td>
<td>
<h3>🔌 Extensible</h3>
• Support for custom apps and configurations<br>
• Plugin architecture
</td>
<td></td>
</tr>
</table>

## 🛠️ Requirements

- Python 3.11 or higher
- Docker
- VSCode (optional, for development features)

## 🚀 Quick Start

```bash
# Install Frappe Manager
pip install frappe-manager

# Setup shell completion
fm --install-completion

# Create your first site
fm create mysite
```

## 📚 Examples

### Development Setup
```bash
# Create a dev environment with ERPNext
fm create devsite --apps erpnext:version-15 --environment dev

# Start coding
fm code devsite --debugger
```

### Production Deploy
```bash
# Create production site with SSL
fm create prodsite --environment prod --ssl le \
    --letsencrypt-email admin@example.com
```

### Daily Operations
```bash
# Common commands
fm start mysite      # Start site
fm stop mysite       # Stop site
fm logs mysite -f    # View logs
fm shell mysite      # Access shell
```

## 📖 Documentation

Visit our [Wiki](https://github.com/rtCamp/Frappe-Manager/wiki) for:
- 📋 Detailed guides
- ⚙️ Configuration options
- 💡 Best practices
- ❓ Troubleshooting

## 🤝 Support

- 🐛 [Report issues](https://github.com/rtCamp/Frappe-Manager/issues)
- 💬 [Discussions](https://github.com/rtCamp/Frappe-Manager/discussions)
- 🌟 Star us on GitHub!

## 👏 Credits

Based on official [Frappe Docker](https://github.com/frappe/frappe_docker) images.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details
