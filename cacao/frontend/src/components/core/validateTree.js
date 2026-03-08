/**
 * Dev-mode JSON tree validator.
 *
 * Walks the component tree from the server and checks it against
 * the contract registry. Runs only when __CACAO_DEBUG__ is true.
 * Reports all issues at once so you see the full picture.
 */

import { contracts } from './contracts.js';

/**
 * Validate a component tree (array of root components).
 * Logs grouped warnings to the console — never throws.
 */
export function validateTree(components) {
  if (!window.__CACAO_DEBUG__) return;

  const issues = [];
  walkTree(components, null, issues);

  if (issues.length === 0) return;

  console.groupCollapsed(
    `%c[Cacao] Tree validation: ${issues.length} issue${issues.length > 1 ? 's' : ''} found`,
    'color: #f59e0b; font-weight: bold'
  );
  for (const issue of issues) {
    console.warn(issue);
  }
  console.groupEnd();
}

function walkTree(components, parentType, issues) {
  if (!Array.isArray(components)) return;

  // Collect child types for the parent
  const childTypes = components.map(c => c?.type).filter(Boolean);

  // Check parent's expectedChildren
  if (parentType && contracts[parentType]?.expectedChildren) {
    for (const expected of contracts[parentType].expectedChildren) {
      if (!childTypes.includes(expected)) {
        issues.push(
          `${parentType} expects a <${expected}> child but none was found. ` +
          `Children present: [${childTypes.join(', ') || 'none'}]`
        );
      }
    }
  }

  // Check parent's allowedChildren
  if (parentType && contracts[parentType]?.allowedChildren) {
    const allowed = contracts[parentType].allowedChildren;
    for (const childType of childTypes) {
      if (!allowed.includes(childType)) {
        issues.push(
          `${parentType} does not expect <${childType}> as a child. ` +
          `Allowed: [${allowed.join(', ')}]`
        );
      }
    }
  }

  // Check each child
  for (const comp of components) {
    if (!comp?.type) continue;

    // Check requiredParent
    const contract = contracts[comp.type];
    if (contract?.requiredParent) {
      if (!parentType || !contract.requiredParent.includes(parentType)) {
        issues.push(
          `<${comp.type}> must be a child of [${contract.requiredParent.join(', ')}] ` +
          `but found inside ${parentType ? `<${parentType}>` : 'root'}`
        );
      }
    }

    // Recurse into children
    if (comp.children) {
      walkTree(comp.children, comp.type, issues);
    }
  }
}
