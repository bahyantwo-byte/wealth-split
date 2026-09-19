"""
Generates QuickSpend.shortcut XML plist.
Flow:
  0. Text action (holds user's sync key — Import Question fills this on install)
  1. Ask for Input (amount)
  2. HTTP POST to Supabase with {user_id, amount, type}
  3. Show Notification

Usage: python3 generate_shortcut.py <supabase_url> <anon_key> <output_xml_path>
CI then runs: plutil -convert binary1 -o QuickSpend.shortcut output.xml
"""
import sys
import uuid

supabase_url = sys.argv[1].rstrip('/')
anon_key = sys.argv[2]
output_path = sys.argv[3]

text_uuid = str(uuid.uuid4()).upper()   # Text action (holds sync key)
ask_uuid  = str(uuid.uuid4()).upper()   # Ask for Input (amount)
http_uuid = str(uuid.uuid4()).upper()   # HTTP POST

ATTACH = '￼'  # U+FFFC — Shortcuts' placeholder for action output tokens

xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
\t<key>WFWorkflowActions</key>
\t<array>

\t\t<!-- Action 0: Text (sync key — filled by Import Question) -->
\t\t<dict>
\t\t\t<key>WFWorkflowActionIdentifier</key>
\t\t\t<string>is.workflow.actions.gettext</string>
\t\t\t<key>WFWorkflowActionParameters</key>
\t\t\t<dict>
\t\t\t\t<key>UUID</key>
\t\t\t\t<string>{text_uuid}</string>
\t\t\t\t<key>WFTextActionText</key>
\t\t\t\t<dict>
\t\t\t\t\t<key>Value</key>
\t\t\t\t\t<dict>
\t\t\t\t\t\t<key>string</key>
\t\t\t\t\t\t<string></string>
\t\t\t\t\t</dict>
\t\t\t\t\t<key>WFSerializationType</key>
\t\t\t\t\t<string>WFTextTokenString</string>
\t\t\t\t</dict>
\t\t\t</dict>
\t\t</dict>

\t\t<!-- Action 1: Ask for Input (amount) -->
\t\t<dict>
\t\t\t<key>WFWorkflowActionIdentifier</key>
\t\t\t<string>is.workflow.actions.ask</string>
\t\t\t<key>WFWorkflowActionParameters</key>
\t\t\t<dict>
\t\t\t\t<key>UUID</key>
\t\t\t\t<string>{ask_uuid}</string>
\t\t\t\t<key>WFAskActionPrompt</key>
\t\t\t\t<string>Amount?</string>
\t\t\t\t<key>WFInputType</key>
\t\t\t\t<string>Text</string>
\t\t\t\t<key>WFAskActionDefaultAnswer</key>
\t\t\t\t<string></string>
\t\t\t</dict>
\t\t</dict>

\t\t<!-- Action 2: HTTP POST to Supabase -->
\t\t<dict>
\t\t\t<key>WFWorkflowActionIdentifier</key>
\t\t\t<string>is.workflow.actions.downloadurl</string>
\t\t\t<key>WFWorkflowActionParameters</key>
\t\t\t<dict>
\t\t\t\t<key>UUID</key>
\t\t\t\t<string>{http_uuid}</string>
\t\t\t\t<key>WFURL</key>
\t\t\t\t<string>{supabase_url}/rest/v1/pending_entries</string>
\t\t\t\t<key>WFHTTPMethod</key>
\t\t\t\t<string>POST</string>
\t\t\t\t<key>WFHTTPHeaders</key>
\t\t\t\t<dict>
\t\t\t\t\t<key>Value</key>
\t\t\t\t\t<dict>
\t\t\t\t\t\t<key>WFDictionaryFieldValues</key>
\t\t\t\t\t\t<array>
\t\t\t\t\t\t\t<dict>
\t\t\t\t\t\t\t\t<key>WFItemType</key><integer>0</integer>
\t\t\t\t\t\t\t\t<key>WFKey</key>
\t\t\t\t\t\t\t\t<dict>
\t\t\t\t\t\t\t\t\t<key>Value</key><dict><key>string</key><string>apikey</string></dict>
\t\t\t\t\t\t\t\t\t<key>WFSerializationType</key><string>WFTextTokenString</string>
\t\t\t\t\t\t\t\t</dict>
\t\t\t\t\t\t\t\t<key>WFValue</key>
\t\t\t\t\t\t\t\t<dict>
\t\t\t\t\t\t\t\t\t<key>Value</key><dict><key>string</key><string>{anon_key}</string></dict>
\t\t\t\t\t\t\t\t\t<key>WFSerializationType</key><string>WFTextTokenString</string>
\t\t\t\t\t\t\t\t</dict>
\t\t\t\t\t\t\t</dict>
\t\t\t\t\t\t\t<dict>
\t\t\t\t\t\t\t\t<key>WFItemType</key><integer>0</integer>
\t\t\t\t\t\t\t\t<key>WFKey</key>
\t\t\t\t\t\t\t\t<dict>
\t\t\t\t\t\t\t\t\t<key>Value</key><dict><key>string</key><string>Authorization</string></dict>
\t\t\t\t\t\t\t\t\t<key>WFSerializationType</key><string>WFTextTokenString</string>
\t\t\t\t\t\t\t\t</dict>
\t\t\t\t\t\t\t\t<key>WFValue</key>
\t\t\t\t\t\t\t\t<dict>
\t\t\t\t\t\t\t\t\t<key>Value</key><dict><key>string</key><string>Bearer {anon_key}</string></dict>
\t\t\t\t\t\t\t\t\t<key>WFSerializationType</key><string>WFTextTokenString</string>
\t\t\t\t\t\t\t\t</dict>
\t\t\t\t\t\t\t</dict>
\t\t\t\t\t\t\t<dict>
\t\t\t\t\t\t\t\t<key>WFItemType</key><integer>0</integer>
\t\t\t\t\t\t\t\t<key>WFKey</key>
\t\t\t\t\t\t\t\t<dict>
\t\t\t\t\t\t\t\t\t<key>Value</key><dict><key>string</key><string>Content-Type</string></dict>
\t\t\t\t\t\t\t\t\t<key>WFSerializationType</key><string>WFTextTokenString</string>
\t\t\t\t\t\t\t\t</dict>
\t\t\t\t\t\t\t\t<key>WFValue</key>
\t\t\t\t\t\t\t\t<dict>
\t\t\t\t\t\t\t\t\t<key>Value</key><dict><key>string</key><string>application/json</string></dict>
\t\t\t\t\t\t\t\t\t<key>WFSerializationType</key><string>WFTextTokenString</string>
\t\t\t\t\t\t\t\t</dict>
\t\t\t\t\t\t\t</dict>
\t\t\t\t\t\t\t<dict>
\t\t\t\t\t\t\t\t<key>WFItemType</key><integer>0</integer>
\t\t\t\t\t\t\t\t<key>WFKey</key>
\t\t\t\t\t\t\t\t<dict>
\t\t\t\t\t\t\t\t\t<key>Value</key><dict><key>string</key><string>Prefer</string></dict>
\t\t\t\t\t\t\t\t\t<key>WFSerializationType</key><string>WFTextTokenString</string>
\t\t\t\t\t\t\t\t</dict>
\t\t\t\t\t\t\t\t<key>WFValue</key>
\t\t\t\t\t\t\t\t<dict>
\t\t\t\t\t\t\t\t\t<key>Value</key><dict><key>string</key><string>return=minimal</string></dict>
\t\t\t\t\t\t\t\t\t<key>WFSerializationType</key><string>WFTextTokenString</string>
\t\t\t\t\t\t\t\t</dict>
\t\t\t\t\t\t\t</dict>
\t\t\t\t\t\t</array>
\t\t\t\t\t</dict>
\t\t\t\t\t<key>WFSerializationType</key>
\t\t\t\t\t<string>WFDictionaryFieldValues</string>
\t\t\t\t</dict>
\t\t\t\t<key>WFHTTPBodyType</key>
\t\t\t\t<string>JSON</string>
\t\t\t\t<key>WFHTTPBodyJSON</key>
\t\t\t\t<dict>
\t\t\t\t\t<key>Value</key>
\t\t\t\t\t<dict>
\t\t\t\t\t\t<key>WFDictionaryFieldValues</key>
\t\t\t\t\t\t<array>
\t\t\t\t\t\t\t<!-- amount field — references Ask action output -->
\t\t\t\t\t\t\t<dict>
\t\t\t\t\t\t\t\t<key>WFItemType</key><integer>0</integer>
\t\t\t\t\t\t\t\t<key>WFKey</key>
\t\t\t\t\t\t\t\t<dict>
\t\t\t\t\t\t\t\t\t<key>Value</key><dict><key>string</key><string>amount</string></dict>
\t\t\t\t\t\t\t\t\t<key>WFSerializationType</key><string>WFTextTokenString</string>
\t\t\t\t\t\t\t\t</dict>
\t\t\t\t\t\t\t\t<key>WFValue</key>
\t\t\t\t\t\t\t\t<dict>
\t\t\t\t\t\t\t\t\t<key>Value</key>
\t\t\t\t\t\t\t\t\t<dict>
\t\t\t\t\t\t\t\t\t\t<key>attachmentsByRange</key>
\t\t\t\t\t\t\t\t\t\t<dict>
\t\t\t\t\t\t\t\t\t\t\t<key>{{0, 1}}</key>
\t\t\t\t\t\t\t\t\t\t\t<dict>
\t\t\t\t\t\t\t\t\t\t\t\t<key>OutputUUID</key><string>{ask_uuid}</string>
\t\t\t\t\t\t\t\t\t\t\t\t<key>Type</key><string>ActionOutput</string>
\t\t\t\t\t\t\t\t\t\t\t</dict>
\t\t\t\t\t\t\t\t\t\t</dict>
\t\t\t\t\t\t\t\t\t\t<key>string</key><string>{ATTACH}</string>
\t\t\t\t\t\t\t\t\t</dict>
\t\t\t\t\t\t\t\t\t<key>WFSerializationType</key><string>WFTextTokenString</string>
\t\t\t\t\t\t\t\t</dict>
\t\t\t\t\t\t\t</dict>
\t\t\t\t\t\t\t<!-- type field — hardcoded "expense" -->
\t\t\t\t\t\t\t<dict>
\t\t\t\t\t\t\t\t<key>WFItemType</key><integer>0</integer>
\t\t\t\t\t\t\t\t<key>WFKey</key>
\t\t\t\t\t\t\t\t<dict>
\t\t\t\t\t\t\t\t\t<key>Value</key><dict><key>string</key><string>type</string></dict>
\t\t\t\t\t\t\t\t\t<key>WFSerializationType</key><string>WFTextTokenString</string>
\t\t\t\t\t\t\t\t</dict>
\t\t\t\t\t\t\t\t<key>WFValue</key>
\t\t\t\t\t\t\t\t<dict>
\t\t\t\t\t\t\t\t\t<key>Value</key><dict><key>string</key><string>expense</string></dict>
\t\t\t\t\t\t\t\t\t<key>WFSerializationType</key><string>WFTextTokenString</string>
\t\t\t\t\t\t\t\t</dict>
\t\t\t\t\t\t\t</dict>
\t\t\t\t\t\t\t<!-- user_id field — references Text action output (sync key) -->
\t\t\t\t\t\t\t<dict>
\t\t\t\t\t\t\t\t<key>WFItemType</key><integer>0</integer>
\t\t\t\t\t\t\t\t<key>WFKey</key>
\t\t\t\t\t\t\t\t<dict>
\t\t\t\t\t\t\t\t\t<key>Value</key><dict><key>string</key><string>user_id</string></dict>
\t\t\t\t\t\t\t\t\t<key>WFSerializationType</key><string>WFTextTokenString</string>
\t\t\t\t\t\t\t\t</dict>
\t\t\t\t\t\t\t\t<key>WFValue</key>
\t\t\t\t\t\t\t\t<dict>
\t\t\t\t\t\t\t\t\t<key>Value</key>
\t\t\t\t\t\t\t\t\t<dict>
\t\t\t\t\t\t\t\t\t\t<key>attachmentsByRange</key>
\t\t\t\t\t\t\t\t\t\t<dict>
\t\t\t\t\t\t\t\t\t\t\t<key>{{0, 1}}</key>
\t\t\t\t\t\t\t\t\t\t\t<dict>
\t\t\t\t\t\t\t\t\t\t\t\t<key>OutputUUID</key><string>{text_uuid}</string>
\t\t\t\t\t\t\t\t\t\t\t\t<key>Type</key><string>ActionOutput</string>
\t\t\t\t\t\t\t\t\t\t\t</dict>
\t\t\t\t\t\t\t\t\t\t</dict>
\t\t\t\t\t\t\t\t\t\t<key>string</key><string>{ATTACH}</string>
\t\t\t\t\t\t\t\t\t</dict>
\t\t\t\t\t\t\t\t\t<key>WFSerializationType</key><string>WFTextTokenString</string>
\t\t\t\t\t\t\t\t</dict>
\t\t\t\t\t\t\t</dict>
\t\t\t\t\t\t</array>
\t\t\t\t\t</dict>
\t\t\t\t\t<key>WFSerializationType</key>
\t\t\t\t\t<string>WFDictionaryFieldValues</string>
\t\t\t\t</dict>
\t\t\t</dict>
\t\t</dict>

\t\t<!-- Action 3: Show Notification -->
\t\t<dict>
\t\t\t<key>WFWorkflowActionIdentifier</key>
\t\t\t<string>is.workflow.actions.notification</string>
\t\t\t<key>WFWorkflowActionParameters</key>
\t\t\t<dict>
\t\t\t\t<key>WFNotificationActionTitle</key>
\t\t\t\t<string>Wealth Split</string>
\t\t\t\t<key>WFNotificationActionBody</key>
\t\t\t\t<string>&#x1F4B8; Logged!</string>
\t\t\t\t<key>WFNotificationActionSound</key>
\t\t\t\t<false/>
\t\t\t</dict>
\t\t</dict>

\t</array>

\t<key>WFWorkflowClientVersion</key>
\t<string>1240.0.4</string>
\t<key>WFWorkflowHasOutputFallback</key>
\t<false/>
\t<key>WFWorkflowIcon</key>
\t<dict>
\t\t<key>WFWorkflowIconGlyphNumber</key>
\t\t<integer>59511</integer>
\t\t<key>WFWorkflowIconColor</key>
\t\t<integer>-12306255</integer>
\t</dict>

\t<!-- Import Question: asks for sync key when shortcut is first added -->
\t<key>WFWorkflowImportQuestions</key>
\t<array>
\t\t<dict>
\t\t\t<key>ActionIndex</key>
\t\t\t<integer>0</integer>
\t\t\t<key>Category</key>
\t\t\t<string>Parameter</string>
\t\t\t<key>DefaultValue</key>
\t\t\t<string></string>
\t\t\t<key>ParameterKey</key>
\t\t\t<string>WFTextActionText</string>
\t\t\t<key>Text</key>
\t\t\t<string>Paste your Wealth Split sync key (found in app → profile → Quick Entry)</string>
\t\t</dict>
\t</array>

\t<key>WFWorkflowInputContentItemClasses</key>
\t<array/>
\t<key>WFWorkflowMinimumClientVersion</key>
\t<integer>411</integer>
\t<key>WFWorkflowMinimumClientVersionString</key>
\t<string>411</string>
\t<key>WFWorkflowName</key>
\t<string>Quick Spend</string>
\t<key>WFWorkflowOutputContentItemClasses</key>
\t<array/>
\t<key>WFWorkflowTypes</key>
\t<array/>
</dict>
</plist>
'''

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(xml)
print(f'Generated: {output_path}')
