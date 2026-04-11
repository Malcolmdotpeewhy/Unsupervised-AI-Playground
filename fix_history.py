import sys
content = open('WebUI/src/components/HistoryChat.vue').read()
# Replace the end </div> with </HistoryChatItem>
content = content.replace("      <ThumbnailPreviewStrip :items=\"conversationImages[key] || []\" />\n    </div>", "      <ThumbnailPreviewStrip :items=\"conversationImages[key] || []\" />\n    </HistoryChatItem>")
open('WebUI/src/components/HistoryChat.vue', 'w').write(content)
