# Deploy UiASK to Railway.app

## 🚀 Quick Deploy (2 minutes)

1. **Push your code to GitHub** (if not already done):
   ```bash
   git add .
   git commit -m "Deploy UiASK"
   git push origin main
   ```

2. **Go to [Railway.app](https://railway.app)** and sign up with GitHub

3. **Deploy your repository**:
   - Click "Deploy from GitHub repo"
   - Select your repository
   - Click "Deploy Now"

4. **Add your UiPath token**:
   - Go to Variables tab
   - Add: `UIPATH_TOKEN` = `your_token_here`
   - Click "Add"

5. **✅ Done!** Your app is live at `https://your-app-name.up.railway.app`

## 🔐 Get Your UiPath Token

Your UiPath token is the long string that looks like:
```
eyJhbGciOiJSUzI1NiIsImtpZCI6IjM5QjNCRjU3...
```

## 🌐 Custom Domain (Optional)

In Railway.app:
- Go to Settings → Domains
- Add your custom domain
- Follow DNS setup instructions

## ❓ Troubleshooting

- **"UIPATH_TOKEN not configured"** → Set the environment variable in Railway
- **App not loading** → Check the deployment logs in Railway dashboard

That's it! Your UiASK app is now live and anyone can use it! 🎉 