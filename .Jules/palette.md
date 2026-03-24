## 2024-05-24 - Dynamic ARIA Labeling with Existing Tooltips
**Learning:** Found a common pattern where icon-only buttons (`IconButton.vue`) use a `tooltip` prop for visual users, but lack screen reader context.
**Action:** Reused the existing visual `tooltip` prop to dynamically bind to `aria-label`, ensuring visual and auditory accessibility are inherently linked and easily maintained by developers.

## 2024-05-24 - Dynamic ARIA Labeling with Existing Translations
**Learning:** When adding ARIA labels, ensure you fall back to English defaults using `languages?.KEY || 'Fallback'` when binding to the reactive language dictionaries.
**Action:** Use this pattern to make sure UI does not break if a translation key is missing.
