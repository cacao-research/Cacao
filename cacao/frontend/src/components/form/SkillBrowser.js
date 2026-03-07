/**
 * SkillBrowser - Discovery widget for Tukuy skills
 *
 * Shows all registered skills grouped by plugin/category with search.
 * Click a skill to see details and run it.
 *
 * Props:
 *   title           - Widget title
 *   show_search     - Show search input
 *   show_categories - Group by category
 *   compact         - Compact display mode
 *   on_select       - Event name to fire on skill selection
 *   height          - Container height
 */

const { createElement: h, useState, useEffect, useCallback, useRef } = React;
import { cacaoWs } from '../core/websocket.js';

export function SkillBrowser({ props }) {
  const {
    title = 'Skill Browser',
    show_search = true,
    show_categories = true,
    compact = false,
    on_select,
    height = '500px',
  } = props;

  const [index, setIndex] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState('');
  const [searchResults, setSearchResults] = useState(null);
  const [selectedSkill, setSelectedSkill] = useState(null);
  const [skillDetails, setSkillDetails] = useState(null);
  const [detailsLoading, setDetailsLoading] = useState(false);
  const searchTimeout = useRef(null);

  // Load initial browse data
  useEffect(() => {
    const handler = (msg) => {
      if (msg.type === 'skill:browse_result') {
        setIndex(msg.index);
        setLoading(false);
        cacaoWs.removeListener(handler);
      } else if (msg.type === 'skill:browse_error') {
        setError(msg.error);
        setLoading(false);
        cacaoWs.removeListener(handler);
      }
    };
    cacaoWs.addListener(handler);
    cacaoWs.send({ type: 'skill:browse' });

    return () => cacaoWs.removeListener(handler);
  }, []);

  // Search handler with debounce
  const handleSearch = useCallback((query) => {
    setSearch(query);
    if (searchTimeout.current) clearTimeout(searchTimeout.current);

    if (!query.trim()) {
      setSearchResults(null);
      return;
    }

    searchTimeout.current = setTimeout(() => {
      const handler = (msg) => {
        if (msg.type === 'skill:search_result') {
          setSearchResults(msg.results);
          cacaoWs.removeListener(handler);
        } else if (msg.type === 'skill:search_error') {
          setSearchResults(null);
          cacaoWs.removeListener(handler);
        }
      };
      cacaoWs.addListener(handler);
      cacaoWs.send({ type: 'skill:search', query, limit: 30 });
    }, 300);
  }, []);

  // Load skill details
  const handleSelectSkill = useCallback((name) => {
    setSelectedSkill(name);
    setDetailsLoading(true);
    setSkillDetails(null);

    const handler = (msg) => {
      if (msg.type === 'skill:details_result') {
        setSkillDetails(msg.details && msg.details.length > 0 ? msg.details[0] : null);
        setDetailsLoading(false);
        cacaoWs.removeListener(handler);
      } else if (msg.type === 'skill:details_error') {
        setDetailsLoading(false);
        cacaoWs.removeListener(handler);
      }
    };
    cacaoWs.addListener(handler);
    cacaoWs.send({ type: 'skill:details', names: [name] });

    if (on_select) {
      cacaoWs.sendEvent(on_select, { skill: name });
    }
  }, [on_select]);

  const renderSkillList = () => {
    if (loading) return h('div', { className: 'cacao-skill-browser-loading' }, 'Loading skills...');
    if (error) return h('div', { className: 'cacao-alert cacao-alert-error' }, error);
    if (!index) return h('div', { className: 'cacao-skill-browser-empty' }, 'No skills found');

    // If searching, show flat search results
    if (searchResults) {
      return h('div', { className: 'cacao-skill-browser-results' },
        searchResults.length === 0
          ? h('div', { className: 'cacao-skill-browser-empty' }, 'No matching skills')
          : searchResults.map(r => renderSkillItem(
              typeof r === 'string' ? r : (r.name || r),
              typeof r === 'object' ? r.description : '',
            )),
      );
    }

    // Show by category
    const plugins = index.plugins || {};
    if (show_categories) {
      return h('div', { className: 'cacao-skill-browser-categories' },
        ...Object.entries(plugins).map(([pluginName, info]) =>
          h('div', { key: pluginName, className: 'cacao-skill-browser-category' },
            h('div', { className: 'cacao-skill-browser-category-header' },
              h('span', { className: 'cacao-skill-browser-category-name' }, pluginName),
              h('span', { className: 'cacao-badge cacao-badge-sm' }, String(info.tool_count || Object.keys(info.tools || {}).length)),
            ),
            h('div', { className: 'cacao-skill-browser-category-tools' },
              ...Object.entries(info.tools || {}).map(([name, desc]) =>
                renderSkillItem(name, desc)
              ),
            ),
          ),
        ),
      );
    }

    // Flat list
    const allTools = [];
    Object.values(plugins).forEach(info => {
      Object.entries(info.tools || {}).forEach(([name, desc]) => {
        allTools.push({ name, description: desc });
      });
    });
    return h('div', { className: 'cacao-skill-browser-results' },
      ...allTools.map(t => renderSkillItem(t.name, t.description)),
    );
  };

  const renderSkillItem = (name, description) => {
    const isSelected = selectedSkill === name;
    return h('div', {
      key: name,
      className: `cacao-skill-browser-item ${isSelected ? 'cacao-skill-browser-item-selected' : ''}`,
      onClick: () => handleSelectSkill(name),
    },
      h('div', { className: 'cacao-skill-browser-item-name' }, name),
      !compact && description && h('div', { className: 'cacao-skill-browser-item-desc' }, description),
    );
  };

  const renderDetails = () => {
    if (!selectedSkill) return h('div', { className: 'cacao-skill-browser-detail-empty' }, 'Select a skill to see details');
    if (detailsLoading) return h('div', { className: 'cacao-skill-browser-loading' }, 'Loading details...');
    if (!skillDetails) return h('div', { className: 'cacao-skill-browser-detail-empty' }, 'No details available');

    const d = skillDetails;
    return h('div', { className: 'cacao-skill-browser-detail' },
      h('h4', { className: 'cacao-skill-browser-detail-name' }, d.name || selectedSkill),
      d.description && h('p', { className: 'cacao-skill-browser-detail-desc' }, d.description),

      // Parameters
      d.parameters && h('div', { className: 'cacao-skill-browser-detail-section' },
        h('h5', null, 'Parameters'),
        h('pre', { className: 'cacao-skill-browser-detail-schema' }, JSON.stringify(d.parameters, null, 2)),
      ),

      // Examples
      d.examples && d.examples.length > 0 && h('div', { className: 'cacao-skill-browser-detail-section' },
        h('h5', null, 'Examples'),
        ...d.examples.map((ex, i) =>
          h('pre', { key: i, className: 'cacao-skill-browser-detail-example' },
            typeof ex === 'string' ? ex : JSON.stringify(ex, null, 2),
          ),
        ),
      ),

      // Tags
      d.tags && d.tags.length > 0 && h('div', { className: 'cacao-skill-browser-detail-tags' },
        ...d.tags.map(tag => h('span', { key: tag, className: 'cacao-badge cacao-badge-outline cacao-badge-sm' }, tag)),
      ),
    );
  };

  return h('div', { className: `cacao-skill-browser ${compact ? 'cacao-skill-browser-compact' : ''}`, style: { height } },
    // Header
    h('div', { className: 'cacao-skill-browser-header' },
      h('h3', { className: 'cacao-skill-browser-title' }, title),
      index && h('span', { className: 'cacao-badge' }, `${index.total_count || 0} skills`),
    ),

    // Search
    show_search && h('div', { className: 'cacao-skill-browser-search' },
      h('input', {
        className: 'cacao-input',
        type: 'text',
        placeholder: 'Search skills...',
        value: search,
        onChange: (e) => handleSearch(e.target.value),
      }),
    ),

    // Content: list + details
    h('div', { className: 'cacao-skill-browser-content' },
      h('div', { className: 'cacao-skill-browser-list' }, renderSkillList()),
      !compact && h('div', { className: 'cacao-skill-browser-details' }, renderDetails()),
    ),
  );
}
