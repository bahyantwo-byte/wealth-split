import sys

path = 'ios/App/App/AppDelegate.swift'
with open(path) as f:
    content = f.read()

# The line Capacitor generates for URL handling
OLD = '        return ApplicationDelegateProxy.shared.application(app, open: url, options: options)'

# Replacement: forward to Capacitor AND inject directly into WKWebView as a backup
NEW = '''        let handled = ApplicationDelegateProxy.shared.application(app, open: url, options: options)
        if let jsonData = try? JSONEncoder().encode(url.absoluteString),
           let jsonStr = String(data: jsonData, encoding: .utf8) {
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) {
                func findBridge(_ vc: UIViewController) -> CAPBridgeViewController? {
                    if let cap = vc as? CAPBridgeViewController { return cap }
                    for child in vc.children { if let found = findBridge(child) { return found } }
                    return nil
                }
                if let root = self.window?.rootViewController,
                   let cap = findBridge(root) {
                    let js = "window.handleAppUrl && window.handleAppUrl(" + jsonStr + ")"
                    cap.webView?.evaluateJavaScript(js, completionHandler: nil)
                }
            }
        }
        return handled'''

if OLD in content:
    patched = content.replace(OLD, NEW)
    with open(path, 'w') as f:
        f.write(patched)
    print('SUCCESS: AppDelegate patched for direct URL injection')
else:
    print('WARNING: Expected pattern not found in AppDelegate.swift')
    print('--- Current content ---')
    print(content)
    sys.exit(0)  # Don't fail build, Capacitor plugin may still handle it
