# 🚀 Korewole Onire - Deployment Guide

## 📋 Prerequisites

1. **Google Gemini API Key**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Save it securely

2. **Google Cloud Service Account** (for Drive integration)
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project or select existing
   - Enable Google Drive API
   - Create Service Account:
     - IAM & Admin → Service Accounts → Create Service Account
     - Grant role: "Editor" or "Drive File Access"
     - Create JSON key and download it
   - Share your Google Drive folder with the service account email

## 📁 GitHub Repository Setup

1. **Create Repository Structure:**
```
korewole-onire/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .streamlit/
│   └── config.toml       # Streamlit configuration
├── .gitignore
└── README.md
```

2. **Create `.gitignore` file:**
```
*.pyc
__pycache__/
.env
*.json
.DS_Store
*.mp4
*.mov
*.avi
```

3. **Create `.streamlit/config.toml` file:**
```toml
[theme]
primaryColor = "#D4AF37"
backgroundColor = "#0A1929"
secondaryBackgroundColor = "#1A2942"
textColor = "#FFFFFF"
font = "sans serif"

[server]
maxUploadSize = 200
enableCORS = false
enableXsrfProtection = true
```

## 🌐 Deploy to Streamlit.io

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit: Korewole Onire app"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/korewole-onire.git
git push -u origin main
```

### Step 2: Connect to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository: `YOUR_USERNAME/korewole-onire`
5. Set main file path: `app.py`
6. Click "Advanced settings"

### Step 3: Configure Secrets

In the Advanced settings → Secrets section, add:

```toml
# Google Gemini API Key
GEMINI_API_KEY = "your_gemini_api_key_here"

# Google Drive Service Account Credentials (entire JSON as one line)
GOOGLE_DRIVE_CREDENTIALS = '''
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END PRIVATE KEY-----\n",
  "client_email": "your-service-account@project.iam.gserviceaccount.com",
  "client_id": "123456789",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "your-cert-url"
}
'''
```

### Step 4: Deploy

1. Click "Deploy!"
2. Wait 2-3 minutes for deployment
3. Your app will be live at: `https://YOUR_APP_NAME.streamlit.app`

## 🔧 System Dependencies

Streamlit Cloud includes FFmpeg by default, but if you need to specify it:

Create `packages.txt` in root:
```
ffmpeg
```

## ✅ Testing the Deployment

1. **Test YouTube URL processing:**
   - Use a short public YouTube video
   - Verify transcription and content generation

2. **Test file upload:**
   - Upload a small video file (<50MB for testing)
   - Check processing speed

3. **Test Google Drive export:**
   - Click "Deliver to my Google Drive"
   - Verify file appears in your Drive

## 🐛 Troubleshooting

### Issue: "FFmpeg not found"
**Solution:** Add `ffmpeg` to `packages.txt`

### Issue: "API key not configured"
**Solution:** Double-check secrets formatting in Streamlit Cloud settings

### Issue: "Google Drive permission denied"
**Solution:** 
- Verify service account email has access to Drive folder
- Check JSON credentials are correctly formatted in secrets

### Issue: "File size too large"
**Solution:** 
- Streamlit Cloud has memory limits
- Use shorter videos (<100MB recommended)
- Consider upgrading Streamlit Cloud plan

## 📊 Resource Limits (Streamlit Cloud Free Tier)

- **Memory:** 1GB RAM
- **CPU:** Shared
- **Storage:** Limited temporary storage
- **Bandwidth:** Fair use policy
- **Uptime:** Apps sleep after inactivity

For production use, consider:
- Streamlit Cloud Pro ($20/month)
- Self-hosting on AWS/GCP/Azure

## 🔐 Security Best Practices

1. **Never commit secrets to GitHub**
2. **Use environment variables for all API keys**
3. **Rotate API keys regularly**
4. **Limit Service Account permissions**
5. **Monitor API usage and costs**

## 📈 Monitoring

Check your app's performance:
- Streamlit Cloud Dashboard: Usage metrics
- Google Cloud Console: API usage
- Gemini API Console: Token consumption

## 🆘 Support

- Streamlit Docs: https://docs.streamlit.io
- Google Gemini Docs: https://ai.google.dev/docs
- Google Drive API: https://developers.google.com/drive

---

## 🎉 You're Ready!

Your premium content repurposing service is now live and ready to transform videos into viral content!
