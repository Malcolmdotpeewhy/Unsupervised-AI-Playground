## 2024-05-24 - Dynamic ARIA Labeling with Existing Tooltips
**Learning:** Found a common pattern where icon-only buttons (`IconButton.vue`) use a `tooltip` prop for visual users, but lack screen reader context.
**Action:** Reused the existing visual `tooltip` prop to dynamically bind to `aria-label`, ensuring visual and auditory accessibility are inherently linked and easily maintained by developers.
## 2024-05-18 - Accessibility on Toggle Buttons
**Learning:** When adding focus states and accessibility labels to dynamic state toggles (like expanding/collapsing a sidebar panel), ensure `aria-label` correctly reflects the action depending on current state, using existing `focus-visible:ring-2` class utilities for visible focus indicators without writing custom CSS.
**Action:** Use conditional statements for dynamically changing `aria-label` text (e.g., `isHistoryVisible ? 'Close History' : 'Show History'`) and verify translations provide proper English fallbacks.
