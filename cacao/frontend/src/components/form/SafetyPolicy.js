/**
 * SafetyPolicy - Safety policy configuration UI for Tukuy
 *
 * Configure allowed imports, network access, and filesystem access
 * for skill execution per session.
 *
 * Props:
 *   title          - Widget title
 *   preset         - Initial preset
 *   show_presets   - Show preset buttons
 *   show_advanced  - Show advanced configuration
 *   compact        - Compact mode
 */

const { createElement: h, useState, useEffect, useCallback } = React;
import { cacaoWs } from '../core/websocket.js';

const PRESETS = [
  { id: 'permissive', label: 'Permissive', desc: 'All access allowed', icon: '🟢' },
  { id: 'network_only', label: 'Network Only', desc: 'Network yes, filesystem no', icon: '🌐' },
  { id: 'filesystem_only', label: 'Filesystem Only', desc: 'Filesystem yes, network no', icon: '📁' },
  { id: 'restrictive', label: 'Restrictive', desc: 'No imports, no network, no filesystem', icon: '🔒' },
  { id: 'custom', label: 'Custom', desc: 'Configure manually', icon: '⚙' },
];

export function SafetyPolicy({ props }) {
  const {
    title = 'Safety Policy',
    preset: initialPreset = null,
    show_presets = true,
    show_advanced = true,
    compact = false,
  } = props;

  const [activePreset, setActivePreset] = useState(initialPreset || 'permissive');
  const [policy, setPolicy] = useState(null);
  const [allowNetwork, setAllowNetwork] = useState(true);
  const [allowFilesystem, setAllowFilesystem] = useState(true);
  const [allowedImports, setAllowedImports] = useState('');
  const [blockedImports, setBlockedImports] = useState('');
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState(null);

  // Load current policy on mount
  useEffect(() => {
    const handler = (msg) => {
      if (msg.type === 'safety:get_result') {
        if (msg.policy) {
          setPolicy(msg.policy);
          setAllowNetwork(msg.policy.allow_network !== false);
          setAllowFilesystem(msg.policy.allow_filesystem !== false);
          if (msg.policy.allowed_imports) setAllowedImports(msg.policy.allowed_imports.join(', '));
          if (msg.policy.blocked_imports) setBlockedImports(msg.policy.blocked_imports.join(', '));
        }
        cacaoWs.removeListener(handler);
      }
    };
    cacaoWs.addListener(handler);
    cacaoWs.send({ type: 'safety:get' });

    return () => cacaoWs.removeListener(handler);
  }, []);

  // Apply preset on initial load
  useEffect(() => {
    if (initialPreset && initialPreset !== 'custom') {
      applyPreset(initialPreset);
    }
  }, [initialPreset]);

  const applyPreset = useCallback((presetId) => {
    setActivePreset(presetId);
    setSaved(false);

    switch (presetId) {
      case 'permissive':
        setAllowNetwork(true);
        setAllowFilesystem(true);
        setAllowedImports('');
        setBlockedImports('');
        break;
      case 'network_only':
        setAllowNetwork(true);
        setAllowFilesystem(false);
        setAllowedImports('');
        setBlockedImports('');
        break;
      case 'filesystem_only':
        setAllowNetwork(false);
        setAllowFilesystem(true);
        setAllowedImports('');
        setBlockedImports('');
        break;
      case 'restrictive':
        setAllowNetwork(false);
        setAllowFilesystem(false);
        setAllowedImports('');
        setBlockedImports('');
        break;
    }

    // Auto-save non-custom presets
    if (presetId !== 'custom') {
      savePolicy(presetId);
    }
  }, []);

  const savePolicy = useCallback((presetOverride) => {
    setSaving(true);
    setError(null);
    setSaved(false);

    const policyConfig = presetOverride && presetOverride !== 'custom'
      ? { preset: presetOverride }
      : {
          allow_network: allowNetwork,
          allow_filesystem: allowFilesystem,
          allowed_imports: allowedImports ? allowedImports.split(',').map(s => s.trim()).filter(Boolean) : [],
          blocked_imports: blockedImports ? blockedImports.split(',').map(s => s.trim()).filter(Boolean) : [],
        };

    const handler = (msg) => {
      if (msg.type === 'safety:set_result') {
        setSaving(false);
        setSaved(true);
        if (msg.policy) setPolicy(msg.policy);
        cacaoWs.removeListener(handler);
        setTimeout(() => setSaved(false), 2000);
      } else if (msg.type === 'safety:set_error') {
        setSaving(false);
        setError(msg.error);
        cacaoWs.removeListener(handler);
      }
    };
    cacaoWs.addListener(handler);
    cacaoWs.send({ type: 'safety:set', policy: policyConfig });
  }, [allowNetwork, allowFilesystem, allowedImports, blockedImports]);

  return h('div', { className: `cacao-safety-policy ${compact ? 'cacao-safety-policy-compact' : ''}` },
    // Header
    h('div', { className: 'cacao-safety-policy-header' },
      h('h3', { className: 'cacao-safety-policy-title' }, title),
      saved && h('span', { className: 'cacao-badge', style: { background: 'var(--success-color, #22c55e)' } }, 'Saved'),
    ),

    // Presets
    show_presets && h('div', { className: 'cacao-safety-policy-presets' },
      ...PRESETS.map(p =>
        h('button', {
          key: p.id,
          className: `cacao-safety-policy-preset ${activePreset === p.id ? 'cacao-safety-policy-preset-active' : ''}`,
          onClick: () => applyPreset(p.id),
        },
          h('span', { className: 'cacao-safety-policy-preset-icon' }, p.icon),
          h('span', { className: 'cacao-safety-policy-preset-label' }, p.label),
          !compact && h('span', { className: 'cacao-safety-policy-preset-desc' }, p.desc),
        ),
      ),
    ),

    // Advanced configuration
    show_advanced && h('div', { className: 'cacao-safety-policy-advanced' },
      // Toggles
      h('div', { className: 'cacao-safety-policy-toggles' },
        h('label', { className: 'cacao-safety-policy-toggle' },
          h('input', {
            type: 'checkbox',
            checked: allowNetwork,
            onChange: (e) => { setAllowNetwork(e.target.checked); setActivePreset('custom'); },
          }),
          h('span', null, 'Allow Network Access'),
        ),
        h('label', { className: 'cacao-safety-policy-toggle' },
          h('input', {
            type: 'checkbox',
            checked: allowFilesystem,
            onChange: (e) => { setAllowFilesystem(e.target.checked); setActivePreset('custom'); },
          }),
          h('span', null, 'Allow Filesystem Access'),
        ),
      ),

      // Import controls
      h('div', { className: 'cacao-safety-policy-imports' },
        h('div', { className: 'cacao-safety-policy-field' },
          h('label', null, 'Allowed Imports (comma-separated, empty = all)'),
          h('input', {
            className: 'cacao-input',
            value: allowedImports,
            placeholder: 'json, re, datetime, math',
            onChange: (e) => { setAllowedImports(e.target.value); setActivePreset('custom'); },
          }),
        ),
        h('div', { className: 'cacao-safety-policy-field' },
          h('label', null, 'Blocked Imports (comma-separated)'),
          h('input', {
            className: 'cacao-input',
            value: blockedImports,
            placeholder: 'os, subprocess, sys',
            onChange: (e) => { setBlockedImports(e.target.value); setActivePreset('custom'); },
          }),
        ),
      ),

      // Save button (for custom config)
      activePreset === 'custom' && h('button', {
        className: 'cacao-btn cacao-btn-primary',
        onClick: () => savePolicy(),
        disabled: saving,
      }, saving ? 'Saving...' : 'Apply Policy'),
    ),

    // Error
    error && h('div', { className: 'cacao-alert cacao-alert-error' }, error),

    // Current policy summary
    policy && h('div', { className: 'cacao-safety-policy-summary' },
      h('small', null, 'Active: '),
      h('span', { className: 'cacao-badge cacao-badge-sm' }, policy.allow_network ? 'Network ✓' : 'Network ✗'),
      h('span', { className: 'cacao-badge cacao-badge-sm' }, policy.allow_filesystem ? 'Filesystem ✓' : 'Filesystem ✗'),
      policy.allowed_imports && h('span', { className: 'cacao-badge cacao-badge-sm' },
        `${policy.allowed_imports.length} allowed imports`,
      ),
    ),
  );
}
