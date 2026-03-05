/**
 * Accordion - Collapsible sections component
 */

const { createElement: h, useState } = React;
import { renderComponent } from '../renderer.js';
import { getIcon } from '../core/icons.js';

function AccordionItemInner({ title, defaultOpen, icon, children, mode, openIndex, index, setOpenIndex }) {
  const isControlled = mode === 'single';
  const [localOpen, setLocalOpen] = useState(defaultOpen || false);
  const isOpen = isControlled ? openIndex === index : localOpen;

  const toggle = () => {
    if (isControlled) {
      setOpenIndex(isOpen ? -1 : index);
    } else {
      setLocalOpen(!localOpen);
    }
  };

  return h('div', { className: 'c-accordion-item' + (isOpen ? ' c-accordion-item--open' : '') }, [
    h('button', {
      key: 'header',
      className: 'c-accordion-header',
      onClick: toggle,
      'aria-expanded': isOpen,
    }, [
      icon && h('span', { key: 'icon', className: 'c-accordion-icon' }, getIcon(icon)),
      h('span', { key: 'title', className: 'c-accordion-title' }, title),
      h('span', { key: 'chevron', className: 'c-accordion-chevron' + (isOpen ? ' c-accordion-chevron--open' : '') }, '\u25B6'),
    ]),
    isOpen && h('div', { key: 'content', className: 'c-accordion-content' }, children),
  ]);
}

export function Accordion({ props, children, setActiveTab, activeTab }) {
  const { items, mode = 'multiple' } = props;
  const [openIndex, setOpenIndex] = useState(-1);
  const renderers = window.Cacao?.renderers || {};

  // If items prop is provided, render simple text accordion
  if (items && items.length) {
    return h('div', { className: 'c-accordion' },
      items.map((item, i) =>
        h(AccordionItemInner, {
          key: i,
          title: item.title,
          defaultOpen: item.defaultOpen || false,
          icon: item.icon,
          children: [h('p', null, item.content)],
          mode,
          openIndex,
          index: i,
          setOpenIndex,
        })
      )
    );
  }

  // Context manager mode - render children (AccordionItem components)
  return h('div', { className: 'c-accordion' },
    children.map((child, i) => {
      if (!child) return null;
      // Pass mode context to AccordionItem children
      return React.cloneElement(child, { key: i, accordionMode: mode, accordionIndex: i, accordionOpenIndex: openIndex, setAccordionOpenIndex: setOpenIndex });
    })
  );
}

export function AccordionItem({ props, children, accordionMode, accordionIndex, accordionOpenIndex, setAccordionOpenIndex }) {
  const { title, defaultOpen, icon } = props;

  return h(AccordionItemInner, {
    title,
    defaultOpen,
    icon,
    children,
    mode: accordionMode || 'multiple',
    openIndex: accordionOpenIndex,
    index: accordionIndex || 0,
    setOpenIndex: setAccordionOpenIndex || (() => {}),
  });
}
