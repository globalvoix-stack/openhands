# Thinksoft Deployment Guide

This guide will help you deploy Thinksoft to production.

## Architecture Overview

Thinksoft consists of three main components:
1. **Frontend** (React) - Can be deployed to Vercel, Netlify, etc.
2. **Backend** (Python/FastAPI) - Needs Docker support (Railway, Render, DigitalOcean, etc.)
3. **Sandbox Runtime** (Docker containers) - Runs inside the backend

## Prerequisites

Before deploying, you need:
- [ ] LLM API key (Anthropic Claude or OpenAI GPT)
- [ ] Backend hosting with Docker support
- [ ] Frontend hosting (Vercel recommended)
- [ ] GitHub account (for repository access)

## Quick Start Deployment

### Step 1: Get Your LLM API Key

Choose ONE of the following:

**Option A: Anthropic Claude (Recommended)**
1. Go to https://console.anthropic.com/
2. Create an account and add credits
3. Generate an API key
4. Copy the key (starts with `sk-ant-`)

**Option B: OpenAI GPT**
1. Go to https://platform.openai.com/api-keys
2. Create an account and add credits
3. Generate an API key
4. Copy the key (starts with `sk-`)

### Step 2: Deploy Backend

**Option A: Railway (Easiest)**

1. Sign up at https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your `globalvoix-stack/openhands` repository
4. Configure environment variables:
   - Copy variables from `.env.backend.example`
   - **REQUIRED**: Set `LLM_API_KEY` to your actual API key
   - Set `LLM_MODEL` (e.g., `anthropic/claude-sonnet-4-20250514`)
   - Set `RUNTIME=docker`
   - Set `SANDBOX_RUNTIME_CONTAINER_IMAGE=ghcr.io/openhands/runtime:main-nikolaik`
5. Enable Docker socket access in Railway settings
6. Deploy!
7. Note your backend URL (e.g., `your-app.railway.app`)

**Option B: Render**

1. Sign up at https://render.com
2. Create a new "Web Service"
3. Connect your GitHub repository
4. Select "Docker" as environment
5. Add environment variables from `.env.backend.example`
6. Enable Docker socket in settings
7. Deploy and note the URL

**Option C: DigitalOcean/VPS**

```bash
# SSH into your server
ssh root@your-server-ip

# Clone repository
git clone https://github.com/globalvoix-stack/openhands.git
cd openhands

# Copy and configure environment file
cp .env.backend.example .env
nano .env  # Edit and add your LLM_API_KEY

# Run with Docker
docker run -it --rm \
  --env-file .env \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(pwd)/workspace:/workspace \
  -v $(pwd)/.thinksoft:/.thinksoft \
  -p 3000:3000 \
  ghcr.io/openhands/openhands:latest
```

### Step 3: Deploy Frontend to Vercel

1. Sign up at https://vercel.com
2. Click "Add New Project" → "Import Git Repository"
3. Select your `globalvoix-stack/openhands` repository
4. Configure:
   - **Root Directory**: `frontend`
   - **Framework Preset**: Vite (or React)
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
5. Add environment variables from `.env.frontend.example`:
   ```
   VITE_BACKEND_HOST=your-backend.railway.app
   VITE_BACKEND_BASE_URL=your-backend.railway.app
   VITE_USE_TLS=true
   VITE_INSECURE_SKIP_VERIFY=false
   VITE_MOCK_API=false
   ```
6. Deploy!

### Step 4: Test Your Deployment

1. Visit your Vercel URL (e.g., `your-app.vercel.app`)
2. You should see the Thinksoft interface
3. Try starting a conversation
4. The app should connect to your backend and use the LLM

## Environment Variables Reference

### Frontend Variables (Vercel)
See [`.env.frontend.example`](.env.frontend.example) for complete list.

**Required:**
- `VITE_BACKEND_HOST` - Your backend URL
- `VITE_USE_TLS` - Set to `true` for production

### Backend Variables (Railway/Render/VPS)
See [`.env.backend.example`](.env.backend.example) for complete list.

**Required:**
- `LLM_API_KEY` - Your Anthropic or OpenAI API key
- `LLM_MODEL` - Model to use (e.g., `anthropic/claude-sonnet-4-20250514`)
- `RUNTIME` - Set to `docker`
- `SANDBOX_RUNTIME_CONTAINER_IMAGE` - Docker image for sandbox

## Troubleshooting

### Frontend can't connect to backend
- Check `VITE_BACKEND_HOST` is correct
- Ensure backend is running and accessible
- Check CORS settings on backend

### Backend can't access LLM
- Verify `LLM_API_KEY` is set correctly
- Check you have credits in your LLM account
- Verify `LLM_MODEL` is a valid model name

### Sandbox/Runtime errors
- Ensure backend has Docker socket access
- Check `SANDBOX_RUNTIME_CONTAINER_IMAGE` is correct
- Verify Docker is running on backend server

### "Permission denied" errors
- Set `RUN_AS_OPENHANDS=true`
- Check file permissions on mounted volumes

## Cost Estimates

**LLM Costs** (variable, depends on usage):
- Claude Sonnet: ~$3 per million input tokens, ~$15 per million output tokens
- GPT-4o: ~$2.50 per million input tokens, ~$10 per million output tokens
- Typical conversation: $0.10 - $0.50

**Hosting Costs**:
- Frontend (Vercel): Free tier available
- Backend (Railway): ~$5/month minimum
- Backend (DigitalOcean): ~$6/month for basic droplet

## Security Notes

- Never commit `.env` files with actual API keys
- Use environment variables for all secrets
- Enable `CONFIRMATION_MODE` for production
- Keep `VITE_INSECURE_SKIP_VERIFY=false` in production
- Regularly rotate API keys
- Monitor LLM usage to prevent unexpected costs

## Support

For issues with:
- **Thinksoft**: Open an issue at https://github.com/globalvoix-stack/openhands/issues
- **OpenHands**: See https://github.com/OpenHands/OpenHands
- **Deployment platforms**: Check their respective documentation

## Advanced Configuration

For advanced configuration options, see:
- [`config.toml.example`](config.toml.example) - Full configuration reference
- [`THINKSOFT_SETUP.md`](THINKSOFT_SETUP.md) - Detailed setup guide
- OpenHands docs: https://docs.openhands.dev/
