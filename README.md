# UiASK 🚀

Convert natural language to SQL queries using UiPath AI agents.

![UiASK Demo](https://via.placeholder.com/800x400/667eea/ffffff?text=UiASK+Demo)

## ✨ Features

- 🗣️ Natural language to SQL conversion
- 🎨 Beautiful, modern UI
- ⚡ Real-time SQL editing with syntax highlighting
- 🔄 Integration with UiPath AI agents
- 📊 Query result visualization

## 🚀 Quick Deploy

[![Deploy to Railway](https://railway.app/button.svg)](https://railway.app/template/your-template)

1. Click the deploy button above
2. Set your `UIPATH_TOKEN` environment variable
3. Your app is live! 🎉

## 🛠️ Local Development

```bash
export UIPATH_TOKEN="your_token_here"
python server.py
```

Open `http://localhost:8000` in your browser.

## 🔧 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `UIPATH_TOKEN` | UiPath authentication token | ✅ |

## 📋 Example Queries

- "Show me total additions and deletions by department"
- "List all pull requests from last month"
- "Find top contributors by commits"

## 🚀 Deploy

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## 📜 License

MIT License - feel free to use and modify! 