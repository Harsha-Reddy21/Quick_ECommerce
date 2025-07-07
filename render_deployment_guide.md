# Deploying Quick ECommerce to Render

This guide explains how to deploy the Quick ECommerce application to Render with a PostgreSQL database.

## Prerequisites

1. A [Render account](https://render.com/)
2. Your code pushed to a Git repository (GitHub, GitLab, etc.)

## Deployment Steps

### Option 1: Deploy using the Render Dashboard

1. **Create a PostgreSQL Database**
   - Go to the Render Dashboard
   - Click on "New +" and select "PostgreSQL"
   - Fill in the following details:
     - Name: `quick-ecommerce-db`
     - Database: `quickcommerce`
     - User: `quickcommerce_user`
     - Region: Choose the closest to your users
     - PostgreSQL Version: 14 or higher
   - Click "Create Database"
   - Once created, note the "Internal Database URL" for the next step

2. **Deploy the Web Service**
   - Go to the Render Dashboard
   - Click on "New +" and select "Web Service"
   - Connect your Git repository
   - Fill in the following details:
     - Name: `quick-ecommerce-api`
     - Runtime: Python 3
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Add the following environment variables:
     - `DATABASE_URL`: Paste the Internal Database URL from the previous step
     - `SECRET_KEY`: Generate a secure random string (you can use `openssl rand -hex 32`)
     - `ALGORITHM`: `HS256`
     - `ACCESS_TOKEN_EXPIRE_MINUTES`: `1440`
   - Click "Create Web Service"

### Option 2: Deploy using render.yaml (Blueprint)

1. **Push your code to a Git repository**
   - Make sure your repository includes the `render.yaml` file we created

2. **Deploy using Blueprint**
   - Go to the Render Dashboard
   - Click on "New +" and select "Blueprint"
   - Connect your Git repository
   - Render will automatically detect the `render.yaml` file
   - Review the configuration and click "Apply"
   - Render will create both the PostgreSQL database and the web service

## After Deployment

1. **Initialize the Database**
   - Once your service is deployed, go to the "Shell" tab in your web service
   - Run: `python create_tables.py`

2. **Verify the API**
   - Visit your API at `https://quick-ecommerce-api.onrender.com`
   - You should see the welcome message
   - Check the API documentation at `https://quick-ecommerce-api.onrender.com/docs`

## Deploying Frontend (React)

If you want to deploy the React frontend as well:

1. **Build the Frontend**
   ```bash
   cd frontend
   npm install
   npm run build
   ```

2. **Create a new Static Site on Render**
   - Go to the Render Dashboard
   - Click on "New +" and select "Static Site"
   - Connect your Git repository
   - Fill in the following details:
     - Name: `quick-ecommerce-frontend`
     - Build Command: `cd frontend && npm install && npm run build`
     - Publish Directory: `frontend/build`
   - Add the environment variable:
     - `REACT_APP_API_URL`: `https://quick-ecommerce-api.onrender.com`
   - Click "Create Static Site"

## Troubleshooting

1. **Database Connection Issues**
   - Check if the `DATABASE_URL` environment variable is correctly set
   - Make sure the database is running and accessible

2. **Application Errors**
   - Check the logs in the Render Dashboard
   - You can also SSH into your service for debugging

3. **CORS Issues**
   - Update your CORS configuration in `main.py` to include your frontend URL

## Maintenance

- **Scaling**: You can adjust the instance type in the Render Dashboard
- **Monitoring**: Render provides basic monitoring tools in the Dashboard
- **Logs**: Access logs from the "Logs" tab in your web service 