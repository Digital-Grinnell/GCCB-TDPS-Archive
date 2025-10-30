# Azure Static Web Apps Deployment Setup

## NEW Deployment for TDPS-Archive

This guide will help you create a **new, dedicated** Azure Static Web App for the TDPS-Archive project.

## Configuration Details

### Workflow File
- **Location:** `.github/workflows/azure-static-web-apps-deploy.yml`
- **Trigger:** Automatic on push to `main` branch
- **Build:** Jekyll with Ruby 3.1

### Build Configuration
```yaml
- Jekyll builds the site in GitHub Actions
- Pre-built _site directory is deployed to Azure
- skip_app_build: true (Azure uses pre-built content)
```

### Deployment Process
1. **Push to main branch** → Triggers GitHub Action
2. **GitHub Action** installs Ruby & Jekyll dependencies
3. **Jekyll builds** the site → `_site` directory
4. **Azure** deploys pre-built `_site` directory
5. **Live URL** will be provided by Azure

## Step-by-Step Setup Instructions

### Step 1: Create New Azure Static Web App

1. **Login to Azure Portal:** https://portal.azure.com
2. **Create Resource** → Search for "Static Web Apps"
3. **Click "Create"**

### Step 2: Configure the Static Web App

Fill in these settings:

#### Basics Tab:
- **Subscription:** Select your Azure subscription
- **Resource Group:** Create new or use existing
- **Name:** `gccb-tdps-archive` (or your preferred name)
- **Plan type:** **Free**
- **Region:** Choose closest to your location (e.g., East US 2, West US 2)

#### Deployment Details:
- **Source:** GitHub
- **Organization:** Digital-Grinnell
- **Repository:** GCCB-TDPS-Archive
- **Branch:** main

#### Build Details:
- **Build Presets:** Custom
- **App location:** `/`
- **Api location:** (leave empty)
- **Output location:** `_site`

### Step 3: Azure Automatically Configures GitHub

Azure will:
1. Add the deployment token to your GitHub repository secrets as `AZURE_STATIC_WEB_APPS_API_TOKEN`
2. Create a workflow file (we already have a better one, so Azure's can be deleted)

### Step 4: Update the Workflow to Use the Token

After Azure creates the secret, the workflow is already configured to use:
- **Secret Name:** `AZURE_STATIC_WEB_APPS_API_TOKEN`

If Azure created a different secret name, you'll need to update `.github/workflows/azure-static-web-apps-deploy.yml`

### Step 5: Verify GitHub Secret

After Azure setup completes:
1. Go to: https://github.com/Digital-Grinnell/GCCB-TDPS-Archive/settings/secrets/actions
2. Verify `AZURE_STATIC_WEB_APPS_API_TOKEN` exists
3. If Azure created a workflow file, you can delete it (we have a better one)

### Step 6: Commit and Push

```bash
# Check status
git status

# Add the new workflow and documentation
git add .github/workflows/azure-static-web-apps-deploy.yml
git add AZURE_DEPLOYMENT_SETUP.md

# Commit
git commit -m "Add new Azure Static Web App deployment workflow"

# Push to trigger deployment
git push origin main
```

### Step 7: Monitor Deployment

After pushing, check:
1. **GitHub Actions:** https://github.com/Digital-Grinnell/GCCB-TDPS-Archive/actions
   - You should see the workflow running
   - First build takes 2-5 minutes
2. **Azure Portal:** https://portal.azure.com
   - Navigate to your Static Web App
   - Check "Overview" for the live URL
   - View deployment history

## Troubleshooting

### If the workflow fails:

1. **Check the GitHub Actions log** for specific errors
2. **Common issues:**
   - Secret not configured: Verify `AZURE_STATIC_WEB_APPS_API_TOKEN` exists
   - Jekyll build fails: Test locally with `bundle exec jekyll build`
   - Ruby version issues: Workflow uses Ruby 3.1

### If Azure creates its own workflow:

Azure might create `.github/workflows/azure-static-web-apps-<random-name>.yml`
- You can safely delete this file
- Use our custom workflow instead (better Jekyll support)

## What's Different from the Old Setup?

✅ **New Azure Static Web App** - Dedicated to this project  
✅ **Ruby/Jekyll build in GitHub Actions** - More control over the build process  
✅ **Pre-built deployment** - Faster, more reliable deployments  
✅ **Clean secret name** - Uses `AZURE_STATIC_WEB_APPS_API_TOKEN`

## Testing the Deployment

To test locally before pushing:
```bash
bundle install
bundle exec jekyll build
bundle exec jekyll serve
# Visit http://localhost:4000
```



## Free Tier Benefits
- **100 GB bandwidth/month**
- **0.5 GB storage**
- **Custom domains** supported
- **Automatic SSL/TLS** certificates
- **Global CDN** distribution

## Current Site Configuration
- **Metadata:** `TDPS_CBMetadata_transformed.csv`
- **Collection:** Theatre, Dance, and Performance Studies Archive
- **Build Tool:** Jekyll (CollectionBuilder-CSV)

---

**Note:** If the deployment fails, check the GitHub Actions log for errors and ensure the Azure API token secret is properly configured.
