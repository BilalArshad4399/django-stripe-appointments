# Koyeb Deployment Instructions

## Prerequisites
1. Create a free account at https://app.koyeb.com/
2. Push your code to GitHub

## Step-by-Step Deployment

### 1. Push Code to GitHub
```bash
git add .
git commit -m "Prepare for Koyeb deployment"
git push origin dev
```

### 2. Create Koyeb App

1. Go to https://app.koyeb.com/
2. Click "Create App"
3. Select "GitHub" as deployment method
4. Connect your GitHub account and select your repository
5. Select the branch (dev)

### 3. Configure Build Settings

In the Build and deployment settings:

**Build command:**
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

**Run command:**
```bash
gunicorn sofia_health.wsgi --bind 0.0.0.0:$PORT
```

### 4. Set Environment Variables

Click on "Environment variables" and add:

```
SECRET_KEY=your-django-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.koyeb.app
STRIPE_PUBLISHABLE_KEY=pk_test_your_key
STRIPE_SECRET_KEY=sk_test_your_key
DATABASE_URL=(Koyeb will provide this if you add a database)
```

### 5. Configure Port

- Set the port to 8000 (or use $PORT environment variable)
- Koyeb automatically provides the PORT variable

### 6. Add Database (Optional but Recommended)

For production, add a PostgreSQL database:
1. In Koyeb dashboard, go to "Databases"
2. Create a new PostgreSQL database
3. Copy the DATABASE_URL
4. Add it to your app's environment variables

### 7. Deploy

1. Click "Deploy"
2. Wait for the build to complete (5-10 minutes)
3. Your app will be available at: `https://your-app-name.koyeb.app`

## Alternative: Using Koyeb CLI

Install Koyeb CLI:
```bash
curl https://get.koyeb.com | bash
```

Deploy:
```bash
koyeb app create sofia-health \
  --github https://github.com/yourusername/your-repo \
  --branch dev \
  --builder buildpack \
  --env SECRET_KEY=your-secret-key \
  --env DEBUG=False \
  --env STRIPE_PUBLISHABLE_KEY=pk_test_xxx \
  --env STRIPE_SECRET_KEY=sk_test_xxx \
  --ports 8000:http \
  --routes /:8000
```

## Important Notes

1. **Database**: SQLite won't work on Koyeb (ephemeral filesystem). Use PostgreSQL.
2. **Static Files**: WhiteNoise is configured to serve static files
3. **Environment Variables**: Never commit real keys. Use Koyeb's environment variables
4. **Migrations**: Run automatically in the build command
5. **Logs**: Check Koyeb dashboard for deployment logs if issues occur

## Troubleshooting

If deployment fails:
1. Check build logs in Koyeb dashboard
2. Ensure all environment variables are set
3. Verify DATABASE_URL is configured for PostgreSQL
4. Make sure ALLOWED_HOSTS includes your Koyeb domain

## Free Tier Limits
- 1 app
- 512 MB RAM
- 1 vCPU
- Sleeps after inactivity (wakes on request)