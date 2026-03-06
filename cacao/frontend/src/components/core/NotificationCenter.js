/**
 * NotificationCenter - Persistent notification panel with bell icon
 * Receives notifications via WebSocket and stores them in sessionStorage
 */

const { createElement: h, useState, useEffect, useCallback, useRef } = React;
import { getIcon } from './icons.js';

const STORAGE_KEY = 'cacao-notifications';

function loadNotifications() {
  try {
    return JSON.parse(sessionStorage.getItem(STORAGE_KEY) || '[]');
  } catch {
    return [];
  }
}

function saveNotifications(notifications) {
  sessionStorage.setItem(STORAGE_KEY, JSON.stringify(notifications));
}

let _addNotification = null;
let _notifId = 0;

/**
 * Add a notification from code.
 */
export function addNotification(notification) {
  if (_addNotification) {
    _addNotification(notification);
  }
}

// Expose globally
window.CacaoNotifications = { add: addNotification };

export function NotificationCenter() {
  const [notifications, setNotifications] = useState(loadNotifications);
  const [open, setOpen] = useState(false);
  const panelRef = useRef(null);

  const unreadCount = notifications.filter(n => !n.read).length;

  // Expose addNotification
  useEffect(() => {
    _addNotification = (notif) => {
      const newNotif = {
        id: ++_notifId,
        title: notif.title || '',
        message: notif.message || '',
        variant: notif.variant || 'info',
        timestamp: Date.now(),
        read: false,
      };
      setNotifications(prev => {
        const updated = [newNotif, ...prev].slice(0, 100); // Cap at 100
        saveNotifications(updated);
        return updated;
      });
    };
    return () => { _addNotification = null; };
  }, []);

  // Close panel on outside click
  useEffect(() => {
    if (!open) return;
    const handleClick = (e) => {
      if (panelRef.current && !panelRef.current.contains(e.target)) {
        setOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, [open]);

  const markAllRead = useCallback(() => {
    setNotifications(prev => {
      const updated = prev.map(n => ({ ...n, read: true }));
      saveNotifications(updated);
      return updated;
    });
  }, []);

  const dismiss = useCallback((id) => {
    setNotifications(prev => {
      const updated = prev.filter(n => n.id !== id);
      saveNotifications(updated);
      return updated;
    });
  }, []);

  const clearAll = useCallback(() => {
    setNotifications([]);
    saveNotifications([]);
  }, []);

  const variantColors = {
    info: 'var(--info)',
    success: 'var(--success)',
    warning: 'var(--warning)',
    error: 'var(--danger)',
  };

  const timeAgo = (ts) => {
    const diff = Date.now() - ts;
    if (diff < 60000) return 'just now';
    if (diff < 3600000) return Math.floor(diff / 60000) + 'm ago';
    if (diff < 86400000) return Math.floor(diff / 3600000) + 'h ago';
    return Math.floor(diff / 86400000) + 'd ago';
  };

  return h('div', { className: 'notification-center', ref: panelRef }, [
    // Bell button
    h('button', {
      key: 'bell',
      className: 'notification-bell',
      onClick: () => { setOpen(!open); if (!open) markAllRead(); },
      'aria-label': 'Notifications',
    }, [
      getIcon('bell'),
      unreadCount > 0 && h('span', { key: 'badge', className: 'notification-badge' },
        unreadCount > 99 ? '99+' : unreadCount
      ),
    ]),
    // Panel
    open && h('div', { key: 'panel', className: 'notification-panel' }, [
      h('div', { key: 'header', className: 'notification-panel-header' }, [
        h('span', { key: 'title' }, 'Notifications'),
        notifications.length > 0 && h('button', {
          key: 'clear',
          className: 'notification-clear',
          onClick: clearAll,
        }, 'Clear all'),
      ]),
      h('div', { key: 'list', className: 'notification-list' },
        notifications.length === 0
          ? h('div', { className: 'notification-empty' }, 'No notifications')
          : notifications.map(n =>
            h('div', {
              key: n.id,
              className: 'notification-item' + (n.read ? '' : ' unread'),
            }, [
              h('div', {
                key: 'dot',
                className: 'notification-dot',
                style: { background: variantColors[n.variant] || variantColors.info },
              }),
              h('div', { key: 'content', className: 'notification-content' }, [
                n.title && h('div', { key: 'title', className: 'notification-title' }, n.title),
                h('div', { key: 'msg', className: 'notification-message' }, n.message),
                h('div', { key: 'time', className: 'notification-time' }, timeAgo(n.timestamp)),
              ]),
              h('button', {
                key: 'dismiss',
                className: 'notification-dismiss',
                onClick: (e) => { e.stopPropagation(); dismiss(n.id); },
                'aria-label': 'Dismiss',
              }, '\u00d7'),
            ])
          )
      ),
    ]),
  ]);
}
