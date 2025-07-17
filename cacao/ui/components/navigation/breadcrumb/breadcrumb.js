// Breadcrumb Component Renderer
(component) => {
  const props = component.props;
  const items = Array.isArray(props.items) ? props.items : [];
  const separator = props.separator || 'arrow';
  const separatorIcon = props.separator_icon;
  const showHome = props.show_home !== false;
  const homeUrl = props.home_url || '/';
  const homeIcon = props.home_icon;
  const maxItems = typeof props.max_items === 'number' ? props.max_items : null;
  const responsive = props.responsive !== false;
  const size = props.size || 'medium';
  const variant = props.variant || 'default';

  // Helper to build separator elements
  function createSeparator() {
    const sep = document.createElement('li');
    sep.className = 'breadcrumb-separator';
    if (separatorIcon) {
      const i = document.createElement('i');
      i.className = `icon-${separatorIcon}`;
      sep.appendChild(i);
    } else if (separator === 'slash') {
      sep.textContent = '/';
    } else if (separator === 'dot') {
      sep.textContent = '•';
    } else {
      // default arrow
      sep.textContent = '>';
    }
    return sep;
  }

  // Build the <nav> wrapper
  const nav = document.createElement('nav');
  nav.className = `breadcrumb breadcrumb--${size} breadcrumb--${variant}` + (responsive ? ' breadcrumb--responsive' : '');
  nav.setAttribute('aria-label', 'breadcrumb');

  // Build the <ol> list
  const ol = document.createElement('ol');
  ol.className = 'breadcrumb-list';

  // Prepare full items array (with home)
  let allItems = [];
  if (showHome) {
    allItems.push({ label: '', url: homeUrl, icon: homeIcon });
  }
  allItems = allItems.concat(items);

  // Handle collapsing if too many items
  let displayItems = allItems;
  if (maxItems && allItems.length > maxItems) {
    const keepStart = Math.ceil(maxItems / 2);
    const keepEnd = Math.floor(maxItems / 2);
    const startSlice = allItems.slice(0, keepStart);
    const endSlice = allItems.slice(allItems.length - keepEnd);
    const overflowSlice = allItems.slice(keepStart, allItems.length - keepEnd);

    displayItems = [
      ...startSlice,
      { label: '…', isOverflow: true, overflowItems: overflowSlice },
      ...endSlice
    ];
  }

  // Render each item (and separators)
  displayItems.forEach((item, idx) => {
    const isLast = idx === displayItems.length - 1;
    const li = document.createElement('li');
    li.className = 'breadcrumb-item';

    if (item.isOverflow) {
      // overflow dropdown
      const drop = document.createElement('span');
      drop.className = 'breadcrumb-overflow';
      drop.textContent = item.label;
      drop.tabIndex = 0;

      const submenu = document.createElement('ul');
      submenu.className = 'breadcrumb-overflow-menu';
      item.overflowItems.forEach(sub => {
        const subLi = document.createElement('li');
        subLi.className = 'breadcrumb-overflow-item';
        if (sub.url) {
          const a = document.createElement('a');
          a.href = sub.url;
          a.textContent = sub.label;
          subLi.appendChild(a);
        } else {
          subLi.textContent = sub.label;
        }
        submenu.appendChild(subLi);
      });

      drop.appendChild(submenu);
      li.appendChild(drop);
    } else {
      // normal item
      if (item.icon && idx === 0 && showHome) {
        const a = document.createElement('a');
        a.href = item.url;
        const i = document.createElement('i');
        i.className = `icon-${item.icon}`;
        a.appendChild(i);
        li.appendChild(a);
      } else if (item.url && !isLast) {
        const a = document.createElement('a');
        a.href = item.url;
        a.textContent = item.label;
        li.appendChild(a);
      } else {
        const span = document.createElement('span');
        span.textContent = item.label;
        li.appendChild(span);
      }
    }

    ol.appendChild(li);

    if (!isLast) {
      ol.appendChild(createSeparator());
    }
  });

  nav.appendChild(ol);
  return nav;
}
