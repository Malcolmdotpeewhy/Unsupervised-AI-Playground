## 2024-05-24 - Vue Inline Arrays Cause Render Thrashing
**Learning:** In Vue, using inline array literals like `['chat', 'imageGen', 'video']` inside a `v-for` loop or within computed properties causes Vue to allocate a new array reference on every single render cycle or property evaluation. This triggers unnecessary DOM updates and child component re-renders.
**Action:** Always extract static array literals into constants in the `<script setup>` block, preserving reference identity across renders.
