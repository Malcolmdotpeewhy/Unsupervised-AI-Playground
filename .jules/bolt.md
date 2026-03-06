## 2024-05-17 - Memoization for Markdown Parsing in v-for Loops
**Learning:** The Vue.js frontend is highly sensitive to function calls inside `v-for` loops, especially `v-html` template interpolations. Calling expensive operations like markdown parsing (`parse`) directly in the template causes severe render thrashing.
**Action:** Always use memoization (e.g., Map-based LRU caching) for expensive operations. Crucially, when streaming LLM text, bypass the cache during active streaming and only cache the final text to prevent rapid cache evictions.
