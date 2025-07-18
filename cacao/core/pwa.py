"""PWA support for Cacao applications."""

import json
import os
from pathlib import Path

class PWASupport:
    def __init__(self, app_name="Cacao App", app_description="A Cacao Progressive Web App",
                 theme_color="#6B4226", background_color="#F5F5F5", enable_offline=True,
                 icon_192="/static/icons/icon-192.png", icon_512="/static/icons/icon-512.png"):
        self.app_name = app_name
        self.app_description = app_description
        self.theme_color = theme_color
        self.background_color = background_color
        self.enable_offline = enable_offline
        self.icon_192 = icon_192
        self.icon_512 = icon_512
        
    def generate_manifest(self):
        """Generate the manifest.json file for PWA support."""
        manifest = {
            "name": self.app_name,
            "short_name": self.app_name,
            "description": self.app_description,
            "start_url": "/",
            "display": "standalone",
            "theme_color": self.theme_color,
            "background_color": self.background_color,
            "icons": [
                {
                    "src": self.icon_192,
                    "sizes": "192x192",
                    "type": "image/png"
                },
                {
                    "src": self.icon_512,
                    "sizes": "512x512",
                    "type": "image/png"
                }
            ]
        }
        return manifest
    
    def generate_service_worker(self):
        """Generate the service worker code for offline capability."""
        if not self.enable_offline:
            return None
            
        return """
        // Service Worker for Cacao PWA
        const CACHE_NAME = 'cacao-app-v1';
        
        // Assets to cache immediately
        const PRECACHE_ASSETS = [
            '/',
            '/static/js/client.js',
            '/static/css/styles.css',
            '/static/icons/icon-192.png',
            '/static/icons/icon-512.png',
            '/manifest.json'
        ];
        
        self.addEventListener('install', event => {
            event.waitUntil(
                caches.open(CACHE_NAME)
                    .then(cache => cache.addAll(PRECACHE_ASSETS))
                    .then(() => self.skipWaiting())
            );
        });
        
        self.addEventListener('fetch', event => {
            event.respondWith(
                caches.match(event.request)
                    .then(response => response || fetch(event.request))
                    .catch(() => {
                        // Return offline page if we can't fetch
                        if (event.request.mode === 'navigate') {
                            return caches.match('/offline.html');
                        }
                        return null;
                    })
            );
        });
        """
    
    def generate_offline_page(self):
        """Generate the offline fallback page for PWA support."""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Offline - """ + self.app_name + """</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 50px;
            background-color: """ + self.background_color + """;
            color: #333;
        }
        .offline-container {
            max-width: 400px;
            margin: 0 auto;
        }
        h1 {
            color: """ + self.theme_color + """;
            margin-bottom: 20px;
        }
        .icon {
            font-size: 4rem;
            margin: 20px 0;
        }
        .retry-btn {
            background-color: """ + self.theme_color + """;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 20px;
        }
        .retry-btn:hover {
            opacity: 0.8;
        }
    </style>
</head>
<body>
    <div class="offline-container">
        <div class="icon">📱</div>
        <h1>You're Offline</h1>
        <p>Sorry, you need an internet connection to use """ + self.app_name + """.</p>
        <p>Please check your connection and try again.</p>
        <button class="retry-btn" onclick="window.location.reload()">Retry</button>
    </div>
</body>
</html>
        """
    
    def apply(self, server):
        """Apply PWA configuration to the server."""
        # Enable PWA mode on the server
        server.enable_pwa = True
        server.pwa = self