# Thinksoft Setup Guide

This guide will help you set up and run Thinksoft after the rebranding from OpenHands.

## Quick Start

### Prerequisites

- Docker (for sandboxed code execution)
- Node.js 22.x or higher
- Python 3.12 (for backend)
- Poetry (Python dependency manager)

### Required API Keys and Environment Variables

To run Thinksoft, you'll need to obtain and configure the following API keys:

## 1. LLM API Keys (REQUIRED - Pick One)

You need at least one LLM provider API key. Choose from:

### Option A: Anthropic Claude (Recommended)
- **API Key**: Get from https://console.anthropic.com/
- **Models**:
  - `claude-sonnet-4-20250514` (recommended)
  - `claude-3-5-haiku-20241022` (faster, cheaper)
- **Environment Variable**: `LLM_API_KEY`
- **In config.toml**: `api_key = "YOUR_ANTHROPIC_API_KEY"`

### Option B: OpenAI GPT
- **API Key**: Get from https://platform.openai.com/api-keys
- **Models**:
  - `gpt-4o` (recommended)
  - `gpt-4-turbo`
  - `gpt-3.5-turbo` (cheaper)
- **Environment Variable**: `LLM_API_KEY`
- **In config.toml**: `api_key = "YOUR_OPENAI_API_KEY"`

### Option C: Other LLM Providers
Thinksoft uses LiteLLM, so it supports 100+ LLM providers including:
- Azure OpenAI
- AWS Bedrock
- Google Vertex AI
- Cohere
- Mistral AI
- And many more

See [LiteLLM docs](https://docs.litellm.ai/docs/providers) for configuration.

## 2. Optional API Keys

### GitHub Integration
- **Purpose**: For working with GitHub repositories, creating PRs, etc.
- **Get from**: https://github.com/settings/tokens
- **Scopes needed**: `repo`, `workflow`
- **Environment Variable**: `GITHUB_TOKEN`
- **In config.toml**: Not directly used, set as environment variable

### Tavily Search (for web search capabilities)
- **Purpose**: Enable agents to search the web
- **Get from**: https://tavily.com/
- **Environment Variable**: Not required, add to config.toml
- **In config.toml**: `tavily_api_key = "YOUR_TAVILY_API_KEY"`

### Remote Runtime (Thinksoft Cloud)
- **Purpose**: Use cloud-hosted sandbox instead of local Docker
- **Get from**: Contact Thinksoft team
- **Environment Variables**:
  - `ALLHANDS_API_KEY` or `RUNTIME_API_KEY`
  - `SANDBOX_REMOTE_RUNTIME_API_URL`

### E2B Sandbox (Alternative Runtime)
- **Purpose**: Alternative cloud sandbox provider
- **Get from**: https://e2b.dev/
- **Environment Variable**: `E2B_API_KEY`

### Daytona Workspace (Alternative Runtime)
- **Purpose**: Cloud development environments
- **Get from**: https://daytona.io/
- **Environment Variable**: `DAYTONA_API_KEY`

### Runloop Runtime (Alternative Runtime)
- **Purpose**: Another cloud sandbox option
- **Get from**: Contact Runloop
- **Environment Variable**: `RUNLOOP_API_KEY`

### PostHog Analytics (Enterprise/SaaS)
- **Purpose**: Product analytics
- **Get from**: https://posthog.com/
- **Environment Variables**:
  - `POSTHOG_API_KEY`
  - `POSTHOG_CLIENT_KEY`

### Stripe Billing (Enterprise/SaaS)
- **Purpose**: Payment processing
- **Get from**: https://stripe.com/
- **Environment Variables**:
  - `STRIPE_SECRET_KEY`
  - `STRIPE_PUBLISHABLE_KEY`
  - `STRIPE_WEBHOOK_SECRET`

## Configuration Files

### 1. Frontend Configuration (`frontend/.env`)

Create this file with:

```bash
# Backend Configuration
VITE_BACKEND_BASE_URL="localhost:3000"
VITE_BACKEND_HOST="127.0.0.1:3000"

# Development Settings
VITE_MOCK_API="false"
VITE_MOCK_SAAS="false"

# TLS Configuration
VITE_USE_TLS="false"
VITE_INSECURE_SKIP_VERIFY="false"

# Frontend Port
VITE_FRONTEND_PORT="3001"
```

### 2. Backend Configuration (`config.toml`)

The `config.toml` file has been created in the root directory. You need to:

1. Open `config.toml`
2. Replace `YOUR_LLM_API_KEY` with your actual API key
3. Choose your model (default: `anthropic/claude-sonnet-4-20250514`)
4. Configure other optional settings as needed

**Minimum required changes:**
```toml
[llm]
model = "anthropic/claude-sonnet-4-20250514"  # or your preferred model
api_key = "YOUR_ACTUAL_API_KEY_HERE"  # REPLACE THIS!
```

## Installation Steps

### 1. Build the entire project

```bash
make build
```

This will:
- Install backend Python dependencies
- Install frontend Node.js dependencies
- Build the frontend
- Set up Docker containers

### 2. Install pre-commit hooks

```bash
make install-pre-commit-hooks
```

### 3. Run Thinksoft

**Option A: Development Mode (Recommended for testing)**

```bash
# Terminal 1: Run backend
cd backend
poetry run python -m openhands.server.listen

# Terminal 2: Run frontend
cd frontend
npm run dev
```

Then visit: http://localhost:3001

**Option B: Production Mode**

```bash
make run
```

This runs both frontend and backend together.

**Option C: With Custom Port**

```bash
make run FRONTEND_PORT=12000 FRONTEND_HOST=0.0.0.0 BACKEND_HOST=0.0.0.0
```

## Environment Variables Reference

### Core Configuration

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `LLM_API_KEY` | API key for your LLM provider | ✅ Yes | None |
| `LLM_MODEL` | Model to use | No | From config.toml |
| `LLM_BASE_URL` | Custom API endpoint | No | Provider default |
| `WORKSPACE_BASE` | Where Thinksoft works on files | No | `./workspace` |
| `SANDBOX_RUNTIME_TYPE` | Runtime: `docker`, `local`, `remote` | No | `docker` |

### Runtime Configuration

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `RUNTIME` | Runtime type (`docker`/`local`/`remote`) | No | `docker` |
| `SANDBOX_VOLUMES` | Docker volume mounts | No | None |
| `SANDBOX_TIMEOUT` | Sandbox timeout (seconds) | No | 120 |

### Development

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DEBUG` | Enable debug logging | No | `false` |
| `LOG_ALL_EVENTS` | Log all events | No | `false` |

### Security

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `CONFIRMATION_MODE` | Require user confirmation | No | `enabled` |
| `SECURITY_ANALYZER` | Security check type | No | `llm` |

### Integration Keys (Optional)

| Variable | Description | Required |
|----------|-------------|----------|
| `GITHUB_TOKEN` | GitHub API token | No |
| `E2B_API_KEY` | E2B sandbox API key | No |
| `DAYTONA_API_KEY` | Daytona workspace API key | No |
| `RUNLOOP_API_KEY` | Runloop runtime API key | No |

## Testing Your Setup

### 1. Test Backend

```bash
cd backend
poetry run python -c "from openhands.core.config import load_app_config; print(load_app_config())"
```

This should print your configuration without errors.

### 2. Test Frontend

```bash
cd frontend
npm run dev
```

Visit http://localhost:3001 - you should see the Thinksoft interface.

### 3. Test Full Integration

1. Start both frontend and backend
2. Open Thinksoft in your browser
3. Try a simple command: "Create a hello world Python script"
4. Thinksoft should respond and create the file

## Troubleshooting

### "No LLM API key found"
- Make sure you've set `LLM_API_KEY` in config.toml or as environment variable
- Check that the key is not wrapped in quotes in environment variables

### "Docker not found" or sandbox errors
- Install Docker: https://docs.docker.com/get-docker/
- Make sure Docker daemon is running
- Alternatively, use `RUNTIME=local` for local execution (less secure)

### Frontend can't connect to backend
- Check that backend is running on port 3000
- Verify `VITE_BACKEND_HOST` in `frontend/.env`
- Check firewall settings

### Module not found errors
- Run `make build` again
- For frontend: `cd frontend && npm install`
- For backend: `poetry install`

## Next Steps

1. **Customize Branding**: Replace placeholder logos in `frontend/src/assets/branding/` with actual Thinksoft logos
2. **Configure Integrations**: Add any additional API keys you need
3. **Set Up Production**: Configure proper TLS, domain names, and production settings
4. **Enable Features**: Configure MCP servers, security analyzers, etc. in config.toml

## Support

For issues or questions:
- Check the main README.md
- Review AGENTS.md for development guidelines
- See Development.md for detailed development instructions

## Summary: Minimum Required to Run

**Absolute minimum to get started:**

1. **One LLM API Key** (Anthropic or OpenAI recommended)
2. **Docker installed** (or use `RUNTIME=local`)
3. **Update config.toml** with your API key
4. **Run**: `make build && make run`

That's it! Everything else is optional and can be configured later.
