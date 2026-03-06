/**
 * SubNav - Scrollable sidebar navigation with groups, search, and badges
 */

const { createElement: h, useState, useCallback, useMemo, useRef, useEffect } = React;

function SubNavItem({ props }) {
  const { label, badge, tag, tag_color, target, href } = props;

  const handleClick = useCallback((e) => {
    if (target) {
      e.preventDefault();
      const el = document.getElementById(target);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }
  }, [target]);

  const tagColorClass = tag_color ? ' c-subnav-tag--' + tag_color : '';

  return h('a', {
    className: 'c-subnav-item',
    href: href || '#',
    onClick: handleClick,
  }, [
    tag && h('span', {
      key: 'tag',
      className: 'c-subnav-tag' + tagColorClass,
    }, tag),
    h('span', { key: 'label', className: 'c-subnav-label' }, label),
    badge != null && h('span', { key: 'badge', className: 'c-subnav-badge' }, badge),
  ]);
}

function SubNavGroup({ props }) {
  const { label } = props;
  return h('div', { className: 'c-subnav-group' }, label);
}

export function SubNav({ props, children }) {
  const { searchable = false, placeholder = 'Search...' } = props;
  const [query, setQuery] = useState('');
  const inputRef = useRef(null);

  const filteredChildren = useMemo(() => {
    if (!query || !children) return children;
    const q = query.toLowerCase();

    const result = [];
    let lastGroup = null;
    let groupHasMatch = false;

    for (const child of children) {
      if (!child || !child.props) continue;

      // Cacao renderer wraps components: child.props.props has the original data
      // child.props.type tells us the component type string
      const childType = child.props.type || '';
      const innerProps = child.props.props || {};

      if (childType === 'SubNavGroup') {
        if (lastGroup && groupHasMatch) {
          result.push(lastGroup);
        }
        lastGroup = child;
        groupHasMatch = false;
      } else if (childType === 'SubNavItem') {
        const label = (innerProps.label || '').toLowerCase();
        const tag = (innerProps.tag || '').toLowerCase();
        if (label.includes(q) || tag.includes(q)) {
          if (lastGroup && !groupHasMatch) {
            result.push(lastGroup);
            groupHasMatch = true;
          }
          result.push(child);
        }
      } else {
        result.push(child);
      }
    }

    // Flush last group
    if (lastGroup && groupHasMatch) {
      // Already pushed
    }

    return result;
  }, [query, children]);

  // Count visible items (excluding groups)
  const itemCount = useMemo(() => {
    if (!children) return 0;
    return children.filter(c => c && c.props && c.props.type === 'SubNavItem').length;
  }, [children]);

  const matchCount = useMemo(() => {
    if (!query || !filteredChildren) return itemCount;
    return filteredChildren.filter(c => c && c.props && c.props.type === 'SubNavItem').length;
  }, [query, filteredChildren, itemCount]);

  return h('div', { className: 'c-subnav' }, [
    searchable && h('div', { key: 'search', className: 'c-subnav-search' },
      h('div', { className: 'c-subnav-search-wrap' }, [
        h('svg', {
          key: 'icon',
          className: 'c-subnav-search-icon',
          viewBox: '0 0 16 16',
          fill: 'none',
          stroke: 'currentColor',
          strokeWidth: '1.5',
          width: 14,
          height: 14,
        }, h('path', { d: 'M11.5 11.5L14 14M6.5 12A5.5 5.5 0 106.5 1a5.5 5.5 0 000 11z' })),
        h('input', {
          key: 'input',
          ref: inputRef,
          type: 'text',
          className: 'c-subnav-search-input',
          placeholder,
          value: query,
          onInput: (e) => setQuery(e.target.value),
        }),
        query && h('span', {
          key: 'count',
          className: 'c-subnav-search-count',
        }, matchCount + '/' + itemCount),
      ])
    ),
    h('div', { key: 'items', className: 'c-subnav-items' }, filteredChildren),
    query && matchCount === 0 && h('div', {
      key: 'empty',
      className: 'c-subnav-empty',
    }, 'No matches'),
  ]);
}

export { SubNavItem, SubNavGroup };
