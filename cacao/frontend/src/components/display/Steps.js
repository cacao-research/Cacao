/**
 * Steps / Stepper - Progress steps indicator
 */

const { createElement: h } = React;
import { getIcon } from '../core/icons.js';

export function Steps({ props, children }) {
  const { direction = 'horizontal' } = props;

  return h('div', {
    className: 'c-steps c-steps--' + direction,
  }, children);
}

export function Step({ props }) {
  const { title, description, status = 'pending', icon } = props;

  const statusIcon = {
    complete: '\u2713',
    active: '\u25CF',
    error: '\u2717',
    pending: '',
  };

  return h('div', { className: 'c-step c-step--' + status }, [
    h('div', { key: 'indicator', className: 'c-step-indicator' },
      icon ? getIcon(icon) : h('span', null, statusIcon[status] || '')
    ),
    h('div', { key: 'content', className: 'c-step-content' }, [
      h('div', { key: 'title', className: 'c-step-title' }, title),
      description && h('div', { key: 'desc', className: 'c-step-description' }, description),
    ]),
  ]);
}
