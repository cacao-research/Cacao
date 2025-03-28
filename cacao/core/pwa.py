"""PWA support for Cacao applications."""

import json
import os
from pathlib import Path

class PWASupport:
    def __init__(self, app_name="Cacao App", app_description="A Cacao Progressive Web App", 
                 theme_color="#6B4226", background_color="#F5F5F5", enable_offline=True):
        self.app_name = app_name
        self.app_description = app_description
        self.theme_color = theme_color
        self.background_color = background_color
        self.enable_offline = enable_offline
        
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
                    "src": "/static/icons/icon-192.png",
                    "sizes": "192x192",
                    "type": "image/png"
                },
                {
                    "src": "/static/icons/icon-512.png",
                    "sizes": "512x512",
                    "type": "image/png"
                }
            ]
        }
        return json.dumps(manifest, indent=2)
    
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