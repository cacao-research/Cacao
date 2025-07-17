// Menu Component Renderer
(component) => {
  const props = component.props;
  const items = Array.isArray(props.items) ? props.items : [];
  const mode = ['horizontal', 'vertical', 'inline'].includes(props.mode) ? props.mode : 'horizontal';
  const theme = props.theme === 'dark' ? 'dark' : 'light';
  const collapsed = props.collapsed === true;
  let selectedKey = props.default_selected || null;

  // Helper to send selection events
  async function sendEvent(eventName, data = {}) {
    if (window.CacaoWS && window.CacaoWS.getStatus() === 1) {
      window.socket.send(JSON.stringify({ type: 'event', event: eventName, data }));
    } else {
      let params = `event=${encodeURIComponent(eventName)}&t=${Date.now()}`;
      for (let [k, v] of Object.entries(data)) {
        params += `&${encodeURIComponent(k)}=${encodeURIComponent(v)}`;
      }
      await fetch(`/api/action?${params}`, { method: 'GET' });
    }
  }

  // Create root <ul>
  const root = document.createElement('ul');
  root.className = `menu menu--${mode} menu--${theme}` + (collapsed ? ' menu--collapsed' : '');
  root.setAttribute('role', 'menu');
  root.setAttribute('tabindex', '0');
  root.setAttribute('aria-label', props.ariaLabel || 'Main menu');

  // Keyboard navigation support
  root.addEventListener('keydown', (e) => {
    const itemsEls = Array.from(root.querySelectorAll('.menu-item:not(.is-disabled)'));
    const current = root.querySelector('.menu-item.is-selected');
    let idx = itemsEls.indexOf(current);
    if (e.key === 'ArrowDown' || (e.key === 'ArrowRight' && mode === 'horizontal')) {
      idx = (idx + 1) % itemsEls.length;
      itemsEls[idx].querySelector('button, a').focus();
      e.preventDefault();
    } else if (e.key === 'ArrowUp' || (e.key === 'ArrowLeft' && mode === 'horizontal')) {
      idx = (idx - 1 + itemsEls.length) % itemsEls.length;
      itemsEls[idx].querySelector('button, a').focus();
      e.preventDefault();
    } else if (e.key === 'Home') {
      itemsEls[0].querySelector('button, a').focus();
      e.preventDefault();
    } else if (e.key === 'End') {
      itemsEls[itemsEls.length - 1].querySelector('button, a').focus();
      e.preventDefault();
    }
  });

  // Recursive renderer for each item (and submenu)
  function renderItem(item, container, parentKey = null) {
    const li = document.createElement('li');
    li.className = 'menu-item' + (item.disabled ? ' is-disabled' : '') + (item.key === selectedKey ? ' is-selected' : '');
    li.setAttribute('role', 'menuitem');
    li.setAttribute('tabindex', item.key === selectedKey ? '0' : '-1');
    if (item.key) li.dataset.key = item.key;
    if (item.disabled) li.setAttribute('aria-disabled', 'true');
    if (item.key === selectedKey) li.setAttribute('aria-current', 'true');

    // Icon if present
    if (item.icon) {
      const iconEl = document.createElement('span');
      iconEl.className = 'menu-item__icon';
      iconEl.innerHTML = `<img src="/cacao/core/static/icons/menu.svg" alt="" aria-hidden="true" />`;
      li.appendChild(iconEl);
    }

    // Label (link or button)
    let trigger;
    if (item.url && !item.disabled) {
      trigger = document.createElement('a');
      trigger.href = item.url;
      trigger.className = 'menu-item__link';
      trigger.textContent = item.label || '';
      trigger.setAttribute('tabindex', '-1');
    } else {
      trigger = document.createElement('button');
      trigger.type = 'button';
      trigger.className = 'menu-item__button';
      trigger.textContent = item.label || '';
      if (item.disabled) trigger.disabled = true;
      trigger.setAttribute('tabindex', '-1');
    }
    li.appendChild(trigger);

    // Click handler for selection
    if (!item.disabled) {
      trigger.addEventListener('click', e => {
        e.preventDefault();
        if (selectedKey !== item.key) {
          root.querySelectorAll('.menu-item.is-selected').forEach(el => {
            el.classList.remove('is-selected');
            el.removeAttribute('aria-current');
            el.setAttribute('tabindex', '-1');
          });
          li.classList.add('is-selected');
          li.setAttribute('aria-current', 'true');
          li.setAttribute('tabindex', '0');
          selectedKey = item.key;
          sendEvent(props.on_select || 'menu:select', { key: item.key });
          trigger.focus();
        }
      });
      // Keyboard: Enter/Space selects
      trigger.addEventListener('keydown', e => {
        if ((e.key === 'Enter' || e.key === ' ') && !item.disabled) {
          trigger.click();
        }
      });
    }

    container.appendChild(li);

    // Submenu (children) support
    if (Array.isArray(item.children) && item.children.length) {
      const subUl = document.createElement('ul');
      subUl.className = 'menu-submenu';
      subUl.setAttribute('role', 'menu');
      subUl.setAttribute('aria-label', item.label ? `${item.label} submenu` : 'Submenu');
      item.children.forEach(child => renderItem(child, subUl, item.key));
      li.appendChild(subUl);
      li.setAttribute('aria-haspopup', 'true');
      li.setAttribute('aria-expanded', 'false');
      // Expand/collapse logic could be added here if needed
    }
  }

  // Render all top‑level items
  items.forEach(item => renderItem(item, root));

  // Focus first selected or first item for accessibility
  setTimeout(() => {
    const selected = root.querySelector('.menu-item.is-selected button, .menu-item.is-selected a');
    if (selected) selected.focus();
    else {
      const first = root.querySelector('.menu-item button, .menu-item a');
      if (first) first.focus();
    }
  }, 0);

  return root;
}
