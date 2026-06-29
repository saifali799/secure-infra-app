# --- Stage 1: Build/Preparation Stage ---
FROM alpine:latest AS preparer

WORKDIR /var/www

# Explicitly copy BOTH the HTML dashboard and the JS logic file
COPY index.html app.js ./

# Set read privileges globally for safety so Nginx can read them
RUN chmod 644 index.html app.js


# --- Stage 2: Final Secure Production Image ---
FROM nginx:1.25-alpine AS runtime

# Remove default generic landing pages
RUN rm /etc/nginx/conf.d/default.conf && \
    rm -rf /usr/share/nginx/html/*

# Copy our custom nginx configuration gateway
COPY nginx.conf /etc/nginx/nginx.conf

# Copy BOTH index.html and app.js from the preparation layer
COPY --from=preparer /var/www/index.html /usr/share/nginx/html/index.html
COPY --from=preparer /var/www/app.js /usr/share/nginx/html/app.js

# Force explicit ownership of the web directory to the unprivileged runtime user
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
    touch /var/run/nginx.pid && \
    chown nginx:nginx /var/run/nginx.pid

# Expose our unprivileged web port
EXPOSE 8080

# Switch to the unprivileged built-in user context
USER nginx

# Start Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]