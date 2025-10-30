## Quick Reference: Azure Portal Settings

When creating the Azure Static Web App, use these exact settings:

### Basics
```
Subscription: [Your Azure Subscription]
Resource Group: [Create new or select existing]
Name: gccb-tdps-archive
Hosting Plan: Free
Region: [Choose your preferred region, e.g., East US 2]
```

### GitHub Integration
```
Source: GitHub
Organization: Digital-Grinnell
Repository: GCCB-TDPS-Archive
Branch: main
```

### Build Configuration
```
Build Presets: Custom
App location: /
Api location: [leave empty]
Output location: _site
```

### After Creation
1. Azure URL will be: `https://<random-name>.azurestaticapps.net`
2. Secret added to GitHub: `AZURE_STATIC_WEB_APPS_API_TOKEN`
3. Check GitHub Actions for deployment status

### Custom Domain (Optional)
Once deployed, you can add a custom domain:
1. Azure Portal → Your Static Web App → Custom domains
2. Add CNAME record: `your-domain.com` → `<random-name>.azurestaticapps.net`
3. Validate and Azure handles SSL automatically
