## 2024-05-24 - Dynamic ARIA Labeling with Existing Tooltips
**Learning:** Found a common pattern where icon-only buttons (`IconButton.vue`) use a `tooltip` prop for visual users, but lack screen reader context.
**Action:** Reused the existing visual `tooltip` prop to dynamically bind to `aria-label`, ensuring visual and auditory accessibility are inherently linked and easily maintained by developers.
## 2024-05-15 - Dynamic State-Based ARIA Labels for Icon Toggles
**Learning:** When using icon-only toggle buttons (like an expand/collapse panel button) in Vue, static `aria-label` attributes are insufficient. Screen readers will not announce the changed state when the visual icon updates. Using a dynamic `aria-label` bound to the component's state (e.g. `:aria-label="isOpen ? 'Close' : 'Open'"`) ensures the accessibility tree stays perfectly synchronized with the visual state without needing additional DOM elements.
**Action:** Always bind both `:aria-label` and `:title` to the reactive toggle state for icon-only buttons that change function upon clicking. Provide localized strings for both states.
