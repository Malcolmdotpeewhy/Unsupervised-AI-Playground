## 2024-05-24 - Dynamic ARIA Labeling with Existing Tooltips
**Learning:** Found a common pattern where icon-only buttons (`IconButton.vue`) use a `tooltip` prop for visual users, but lack screen reader context.
**Action:** Reused the existing visual `tooltip` prop to dynamically bind to `aria-label`, ensuring visual and auditory accessibility are inherently linked and easily maintained by developers.
## 2024-05-24 - Missing `aria-label`s on icon-only buttons
**Learning:** Icon-only buttons (like settings, window controls, prompt area interactions) often use `title` for hover tooltips but miss `aria-label`s, causing poor screen reader accessibility. This includes dynamically injected tools and custom UI component wrappers like `<Button>`.
**Action:** When adding icon-only buttons, map the visual `title` or tooltip string directly to `aria-label`. Verify custom UI buttons like `<Button>` receive standard accessibility attributes.
