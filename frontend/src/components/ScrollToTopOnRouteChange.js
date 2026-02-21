import { Component } from 'react';
import { withRouter } from '../utils/withRouter';

class ScrollToTopOnRouteChange extends Component {
  componentDidUpdate(prevProps) {
    if (this.props.location !== prevProps.location) {
      // Scroll to top when route changes
      window.scrollTo(0, 0);
    }
  }

  render() {
    return this.props.children;
  }
}

export default withRouter(ScrollToTopOnRouteChange);
