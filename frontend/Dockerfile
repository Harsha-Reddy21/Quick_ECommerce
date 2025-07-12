# Build stage
FROM node:16-alpine as build

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY . .

# Create env file
RUN echo "REACT_APP_API_URL=$REACT_APP_API_URL" > .env

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built files from build stage
COPY --from=build /app/build /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Create a shell script to handle environment variables at runtime
RUN echo $'\n\
#!/bin/sh\n\
\n\
# Replace environment variables in the built files\n\
find /usr/share/nginx/html -type f -exec sed -i "s|REACT_APP_API_URL_PLACEHOLDER|$REACT_APP_API_URL|g" {} +\n\
\n\
# Start nginx\n\
nginx -g "daemon off;"\n\
' > /docker-entrypoint.sh \
&& chmod +x /docker-entrypoint.sh

# Expose port
EXPOSE 80

# Start nginx using our entrypoint script
CMD ["/docker-entrypoint.sh"] 