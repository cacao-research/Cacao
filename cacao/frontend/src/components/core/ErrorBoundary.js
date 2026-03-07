/**
 * Error Boundary for Cacao components.
 * Catches render errors in individual components and displays a visual
 * indicator instead of crashing the entire app.
 */

const { createElement: h, Component } = React;

export class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { error };
  }

  componentDidCatch(error, errorInfo) {
    this.setState({ errorInfo });
    console.error(`[Cacao] Component error in <${this.props.componentType || 'Unknown'}>:`, error, errorInfo);
  }

  render() {
    if (this.state.error) {
      const { componentType } = this.props;
      const isDebug = window.__CACAO_DEBUG__;
      const errorMessage = this.state.error.message || String(this.state.error);

      return h('div', { className: 'cacao-error-boundary' },
        h('div', { className: 'cacao-error-boundary__header' },
          h('span', { className: 'cacao-error-boundary__icon' }, '\u26A0'),
          h('span', { className: 'cacao-error-boundary__title' },
            `Error in <${componentType || 'Component'}>`
          ),
        ),
        isDebug && h('div', { className: 'cacao-error-boundary__details' },
          h('code', null, errorMessage),
          this.state.errorInfo && h('pre', { className: 'cacao-error-boundary__stack' },
            this.state.errorInfo.componentStack
          ),
        ),
        h('button', {
          className: 'cacao-error-boundary__retry',
          onClick: () => this.setState({ error: null, errorInfo: null }),
        }, 'Retry'),
      );
    }

    return this.props.children;
  }
}
