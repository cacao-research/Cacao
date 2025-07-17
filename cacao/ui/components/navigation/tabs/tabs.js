(component) => {
  console.log("[CacaoCore] Rendering tabs component:", component);
  const props = component.props;
  const items = Array.isArray(props.items) ? props.items : [];
  let activeKey = props.active_key || (items[0] && items[0].key) || null;
  const orientation = props.orientation === 'vertical' ? 'vertical' : 'horizontal';
  const size = props.size || 'medium';
  const variant = props.variant || 'default';
  const animated = props.animated !== false;
  const closable = props.closable === true;
  const centered = props.centered === true;
  const showAdd = props.show_add_button === true;
  const maxWidth = props.max_width || null;

  // Helper for sending events (change, close, add)
  async function sendEvent(eventName, data = {}) {
    console.log("[Cacao] Tab event:", eventName, data);
    if (window.CacaoWS && window.CacaoWS.getStatus() === 1) {
      window.socket.send(JSON.stringify({ type: 'event', event: eventName, data }));
    } else {
      // HTTP fallback
      let params = `event=${eventName}&t=${Date.now()}`;
      for (const [k,v] of Object.entries(data)) {
        params += `&${encodeURIComponent(k)}=${encodeURIComponent(v)}`;
      }
      await fetch(`/api/action?${params}`, { method: 'GET' });
    }
  }

  // Create root container
  const root = document.createElement('div');
  root.className = `tabs-container tabs-${orientation} tabs-${size} tabs-${variant}`;
  if (centered) root.classList.add('tabs-centered');
  if (animated) root.classList.add('tabs-animated');
  if (closable) root.classList.add('tabs-closable');
  if (showAdd) root.classList.add('tabs-has-add-button');
  if (maxWidth) root.style.maxWidth = maxWidth;

  // Set ID if provided
  if (props.id) {
    root.id = props.id;
  }

  // Create the navigation wrapper
  const nav = document.createElement('div');
  nav.className = 'tabs-nav';

  // Create the tab list
  const list = document.createElement('ul');
  list.className = 'tabs-list';
  list.setAttribute('role', 'tablist');
  if (orientation === 'vertical') {
    list.setAttribute('aria-orientation', 'vertical');
  }

  // Create panels container
  const panels = document.createElement('div');
  panels.className = 'tabs-content';

  // Create indicator for active tab
  const indicator = document.createElement('div');
  indicator.className = 'tabs-indicator';
  nav.appendChild(indicator);

  // Track tab buttons for indicator positioning
  const tabButtons = [];

  // Render each tab + panel
  items.forEach((item, index) => {
    const key = item.key;
    const disabled = item.disabled === true;
    const isActive = key === activeKey;

    // --- Tab Button ---
    const li = document.createElement('li');
    li.className = 'tabs-item';
    
    const btn = document.createElement('button');
    btn.className = `tab-item${isActive ? ' tab-active' : ''}${disabled ? ' tab-disabled' : ''}`;
    btn.setAttribute('role', 'tab');
    btn.setAttribute('aria-selected', isActive);
    btn.setAttribute('aria-controls', `panel-${key}`);
    btn.setAttribute('data-key', key);
    btn.disabled = disabled;
    btn.tabIndex = isActive ? 0 : -1;

    // Tab content wrapper
    const tabContent = document.createElement('div');
    tabContent.className = 'tab-content';

    // Icon
    if (item.icon) {
      const icon = document.createElement('span');
      icon.className = `tab-icon icon-${item.icon}`;
      tabContent.appendChild(icon);
    }

    // Label
    const label = document.createElement('span');
    label.className = 'tab-label';
    label.textContent = item.label || '';
    tabContent.appendChild(label);

    // Badge
    if (item.badge != null) {
      const badge = document.createElement('span');
      badge.className = 'tab-badge';
      badge.textContent = item.badge;
      tabContent.appendChild(badge);
    }

    btn.appendChild(tabContent);

    // Close button
    if (closable && !disabled) {
      const close = document.createElement('button');
      close.className = 'tab-close';
      close.innerHTML = '×';
      close.title = 'Close tab';
      close.setAttribute('aria-label', 'Close tab');
      close.addEventListener('click', e => {
        e.stopPropagation();
        sendEvent(props.on_close || 'tabs:close', { key });
        // remove item & panel
        li.remove();
        panel.remove();
        if (activeKey === key && items.length > 1) {
          // activate first remaining
          const nextKey = root.querySelector('.tab-item:not(.tab-disabled)')?.dataset.key;
          if (nextKey) activateTab(nextKey);
        }
      });
      btn.appendChild(close);
    }

    btn.addEventListener('click', () => {
      if (disabled) return;
      if (key !== activeKey) {
        activateTab(key);
        sendEvent(props.on_change || 'tabs:change', { key });
      }
    });

    li.appendChild(btn);
    list.appendChild(li);
    tabButtons.push(btn);

    // --- Content Panel ---
    const panel = document.createElement('div');
    panel.className = `tab-panel${isActive ? ' tab-panel-active' : ''}`;
    panel.setAttribute('role', 'tabpanel');
    panel.setAttribute('id', `panel-${key}`);
    panel.setAttribute('aria-labelledby', `tab-${key}`);
    panel.setAttribute('data-key', key);
    if (!isActive) panel.hidden = true;
    
    // Handle content - it could be a string or a component
    if (typeof item.content === 'string') {
      panel.innerHTML = item.content;
    } else if (item.content && typeof item.content === 'object') {
      // Render as component
      panel.appendChild(window.CacaoCore.renderComponent(item.content));
    }
    
    panels.appendChild(panel);
  });

  // Optional "Add" button
  if (showAdd) {
    const addLi = document.createElement('li');
    addLi.className = 'tabs-item tabs-item--add';
    const addBtn = document.createElement('button');
    addBtn.className = 'tabs-add-button';
    addBtn.innerHTML = '<span class="tabs-add-icon">+</span>';
    addBtn.title = 'Add tab';
    addBtn.setAttribute('aria-label', 'Add new tab');
    addBtn.addEventListener('click', () => {
      sendEvent(props.on_add || 'tabs:add', {});
    });
    addLi.appendChild(addBtn);
    list.appendChild(addLi);
  }

  nav.appendChild(list);
  root.appendChild(nav);
  root.appendChild(panels);

  // Function to update indicator position
  function updateIndicator() {
    const activeBtn = root.querySelector('.tab-item.tab-active');
    if (activeBtn) {
      const rect = activeBtn.getBoundingClientRect();
      const listRect = list.getBoundingClientRect();
      
      if (orientation === 'horizontal') {
        indicator.style.left = `${activeBtn.offsetLeft}px`;
        indicator.style.width = `${activeBtn.offsetWidth}px`;
        indicator.style.height = '3px';
        indicator.style.top = 'auto';
        indicator.style.bottom = '0';
      } else {
        indicator.style.top = `${activeBtn.offsetTop}px`;
        indicator.style.height = `${activeBtn.offsetHeight}px`;
        indicator.style.width = '3px';
        indicator.style.left = 'auto';
        indicator.style.right = '0';
      }
    }
  }

  // Keyboard navigation
  root.addEventListener('keydown', e => {
    const triggers = Array.from(root.querySelectorAll('.tab-item:not(.tab-disabled)'));
    if (!triggers.length) return;
    
    let currentIndex = triggers.findIndex(t => t.dataset.key === activeKey);
    if (currentIndex === -1) return;
    
    let nextIndex = currentIndex;
    
    switch (e.key) {
      case 'ArrowRight':
        if (orientation === 'horizontal') {
          e.preventDefault();
          nextIndex = (currentIndex + 1) % triggers.length;
        }
        break;
      case 'ArrowLeft':
        if (orientation === 'horizontal') {
          e.preventDefault();
          nextIndex = (currentIndex - 1 + triggers.length) % triggers.length;
        }
        break;
      case 'ArrowDown':
        if (orientation === 'vertical') {
          e.preventDefault();
          nextIndex = (currentIndex + 1) % triggers.length;
        }
        break;
      case 'ArrowUp':
        if (orientation === 'vertical') {
          e.preventDefault();
          nextIndex = (currentIndex - 1 + triggers.length) % triggers.length;
        }
        break;
      case 'Home':
        e.preventDefault();
        nextIndex = 0;
        break;
      case 'End':
        e.preventDefault();
        nextIndex = triggers.length - 1;
        break;
    }
    
    if (nextIndex !== currentIndex) {
      const nextBtn = triggers[nextIndex];
      nextBtn.focus();
      activateTab(nextBtn.dataset.key);
      sendEvent(props.on_change || 'tabs:change', { key: nextBtn.dataset.key });
    }
  });

  // Activate a tab by key
  function activateTab(key) {
    activeKey = key;
    
    // Update tab buttons
    root.querySelectorAll('.tab-item').forEach(btn => {
      const isActive = btn.dataset.key === key;
      btn.classList.toggle('tab-active', isActive);
      btn.setAttribute('aria-selected', isActive);
      btn.tabIndex = isActive ? 0 : -1;
    });
    
    // Update panels
    root.querySelectorAll('.tab-panel').forEach(panel => {
      const isActive = panel.dataset.key === key;
      panel.classList.toggle('tab-panel-active', isActive);
      panel.hidden = !isActive;
    });
    
    // Update indicator position
    updateIndicator();
  }

  // Initial indicator positioning
  setTimeout(() => {
    updateIndicator();
  }, 0);

  // Update indicator on window resize
  window.addEventListener('resize', updateIndicator);

  return root;
}
