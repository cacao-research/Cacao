/*
WebSocket client for Cacao framework.
Handles real-time updates and UI synchronization.
*/

(function() {
    // WebSocket connection management
    const WS_URL = `ws://${window.location.hostname}:1633`;
    let socket = null;
    let reconnectAttempts = 0;
    const MAX_RECONNECT_ATTEMPTS = 5;
    let refreshInProgress = false;

    function connect() {
        socket = new WebSocket(WS_URL);

        socket.onopen = function() {
            console.log('[CacaoWS] Connected to WebSocket server');
            reconnectAttempts = 0;
        };

        socket.onmessage = function(event) {
            try {
                const data = JSON.parse(event.data);
                
                // Handle UI update events
                if (data.type === 'ui_update') {
                    console.log('[CacaoWS] Received UI update', data);
                    
                    // Prevent multiple simultaneous refreshes
                    if (refreshInProgress) {
                        console.log('[CacaoWS] Refresh already in progress, skipping');
                        return;
                    }
                    
                    refreshInProgress = true;
                    
                    // Show refresh overlay
                    const overlay = document.querySelector('.refresh-overlay');
                    if (overlay) overlay.classList.add('active');
                    
                    // Force UI refresh
                    fetch('/api/ui?force=true&t=' + Date.now(), {
                        headers: {
                            'Cache-Control': 'no-cache, no-store, must-revalidate',
                            'Pragma': 'no-cache',
                            'Expires': '0'
                        }
                    })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error(`Server returned ${response.status}`);
                        }
                        return response.json();
                    })
                    .then(uiData => {
                        console.log('[CacaoWS] Fetched new UI data', uiData);
                        window.CacaoCore.render(uiData);
                    })
                    .catch(error => {
                        console.error('[CacaoWS] Error fetching UI update:', error);
                        // Hide overlay on error
                        if (overlay) overlay.classList.remove('active');
                    })
                    .finally(() => {
                        refreshInProgress = false;
                    });
                }
            } catch (error) {
                console.error('[CacaoWS] Error processing message:', error);
            }
        };

        socket.onclose = function(event) {
            console.log('[CacaoWS] WebSocket connection closed', event);
            
            if (reconnectAttempts < MAX_RECONNECT_ATTEMPTS) {
                reconnectAttempts++;
                const timeout = Math.pow(2, reconnectAttempts) * 1000;
                console.log(`[CacaoWS] Attempting to reconnect in ${timeout/1000} seconds`);
                
                setTimeout(connect, timeout);
            } else {
                console.error('[CacaoWS] Max reconnect attempts reached');
            }
        };

        socket.onerror = function(error) {
            console.error('[CacaoWS] WebSocket error:', error);
        };
    }

    // Expose WebSocket functionality
    window.CacaoWS = {
        connect: connect,
        forceRefresh: function() {
            console.log('[CacaoWS] Forcing UI refresh');
            
            // Show refresh overlay
            const overlay = document.querySelector('.refresh-overlay');
            if (overlay) overlay.classList.add('active');
            
            fetch('/api/ui?force=true&t=' + Date.now(), {
                headers: {
                    'Cache-Control': 'no-cache, no-store, must-revalidate',
                    'Pragma': 'no-cache',
                    'Expires': '0'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Server returned ${response.status}`);
                }
                return response.json();
            })
            .then(uiData => {
                console.log('[CacaoWS] Fetched new UI data', uiData);
                window.CacaoCore.render(uiData);
            })
            .catch(error => {
                console.error('[CacaoWS] Error forcing refresh:', error);
                // Hide overlay on error
                if (overlay) overlay.classList.remove('active');
            });
        },
        requestServerRefresh: function() {
            if (socket && socket.readyState === WebSocket.OPEN) {
                socket.send(JSON.stringify({action: 'refresh'}));
                console.log('[CacaoWS] Requested server refresh');
            } else {
                console.error('[CacaoWS] WebSocket not connected, cannot request refresh');
                // Fallback to direct refresh
                this.forceRefresh();
            }
        }
    };

    // Automatically connect on script load
    connect();
})();
