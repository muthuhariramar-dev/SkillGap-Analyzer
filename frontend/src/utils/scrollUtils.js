// Scroll prevention utility
export const preventUnwantedScroll = () => {
  // Prevent scroll jump on page load
  if (window.location.hash) {
    window.scrollTo(0, 0);
  }

  // Prevent scroll jump when clicking buttons
  const handleButtonClick = (e) => {
    // Prevent default scroll behavior for buttons that don't need it
    if (e.target.tagName === 'BUTTON' || e.target.type === 'submit') {
      // Don't prevent default for buttons that should navigate
      if (!e.target.closest('a') && !e.target.closest('form')) {
        e.preventDefault();
      }
    }
  };

  // Prevent scroll jump on hash changes
  const handleHashChange = () => {
    window.scrollTo(0, 0);
  };

  // Add event listeners
  document.addEventListener('click', handleButtonClick);
  window.addEventListener('hashchange', handleHashChange);

  // Ensure page starts at top
  window.scrollTo(0, 0);

  // Cleanup function
  return () => {
    document.removeEventListener('click', handleButtonClick);
    window.removeEventListener('hashchange', handleHashChange);
  };
};

// Utility function to scroll to top
export const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
};

// Utility function to prevent scroll jump
export const preventScrollJump = () => {
  // Store current scroll position
  const scrollY = window.scrollY;

  // Restore scroll position after next frame
  requestAnimationFrame(() => {
    window.scrollTo(0, scrollY);
  });
};

// Simple scroll prevention without event listeners
export const initializeScrollPrevention = () => {
  // Just ensure page starts at top
  window.scrollTo(0, 0);
  
  // Add a simple click handler to prevent unwanted scrolling
  const handleClick = (e) => {
    // Only prevent default for buttons that don't need navigation
    const target = e.target;
    if (target.tagName === 'BUTTON' && 
        !target.closest('a') && 
        !target.closest('form') && 
        !target.onclick) {
      e.preventDefault();
    }
  };
  
  // Add the click listener with error handling
  try {
    document.addEventListener('click', handleClick, { passive: false });
  } catch (error) {
    console.warn('Scroll prevention click listener error:', error);
  }
  
  // Prevent scroll jump on hash changes
  try {
    window.addEventListener('hashchange', () => {
      window.scrollTo(0, 0);
    });
  } catch (error) {
    console.warn('Hash change listener error:', error);
  }
};
