/**
 * PanelManager - Manages z-index stacking for floating panels
 */

let _zCounter = 900;

const PanelManager = {
  bringToFront(panelElement) {
    if (!panelElement) return;
    _zCounter++;
    panelElement.style.setProperty('--panel-z', _zCounter);
    panelElement.style.zIndex = _zCounter;
  },

  reset() {
    _zCounter = 900;
  },
};

// Expose globally
window.CacaoPanelManager = PanelManager;

export { PanelManager };
