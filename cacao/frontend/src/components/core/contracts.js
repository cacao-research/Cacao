/**
 * Component contracts — defines expected parent-child relationships.
 *
 * Each key is a component type. The contract describes:
 *   - expectedChildren: child types this component needs to function correctly
 *   - allowedChildren: if set, only these child types are valid (optional)
 *   - requiredParent: this component must be a child of one of these types
 */
export const contracts = {
  AppShell: {
    expectedChildren: ['NavSidebar'],
  },
  NavSidebar: {
    expectedChildren: ['NavGroup'],
    requiredParent: ['AppShell'],
  },
  ShellContent: {
    requiredParent: ['AppShell'],
  },
  NavGroup: {
    expectedChildren: ['NavItem'],
    requiredParent: ['NavSidebar'],
  },
  NavItem: {
    requiredParent: ['NavGroup'],
  },
};
