## 2024-03-22 - Missing focus states on generic icon buttons
**Learning:** Generic reusable icon buttons without text often lack focus states. While focus is important everywhere, it is critical on reusable wrapper components because any missing accessibility on the wrapper multiplies across all usages.
**Action:** When auditing custom base components like IconButton.vue, always ensure they inherit focus visible classes (focus-visible:ring-1 focus-visible:ring-ring focus-visible:outline-none or similar from the design system).
