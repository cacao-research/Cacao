# DevTools - showcase demo (static handlers)
import cacao as c

c.config(title="DevTools", theme="dark", branding=True)

c.title("DevTools")
c.text("Browser-based developer utilities powered by Cacao static handlers", color="muted")
c.spacer()

# --- Encoders ---
with c.row():
    with c.col(span=6):
        with c.card("Base64 Encoder"):
            input_sig = c.signal("Hello, Cacao!", name="b64_input")
            output_sig = c.signal("", name="b64_output")
            c.input("Text to encode", value=input_sig)
            c.button("Encode", on_click="base64_encode", variant="primary")
            c.bind("base64_encode", input_sig)
            c.code("", language="text", id="b64_result")
            c.static_handler("base64_encode", """
                const text = args.value || '';
                const encoded = btoa(text);
                document.querySelector('[data-id="b64_result"] code').textContent = encoded;
            """)

    with c.col(span=6):
        with c.card("URL Encoder"):
            url_input = c.signal("hello world & foo=bar", name="url_input")
            c.input("Text to encode", value=url_input)
            c.button("Encode URL", on_click="url_encode", variant="primary")
            c.bind("url_encode", url_input)
            c.code("", language="text", id="url_result")
            c.static_handler("url_encode", """
                const text = args.value || '';
                const encoded = encodeURIComponent(text);
                document.querySelector('[data-id="url_result"] code').textContent = encoded;
            """)

c.spacer()

# --- Generators ---
with c.row():
    with c.col(span=4):
        with c.card("UUID Generator"):
            c.code("", language="text", id="uuid_result")
            c.button("Generate UUID", on_click="gen_uuid", variant="primary")
            c.static_handler("gen_uuid", """
                const uuid = crypto.randomUUID();
                document.querySelector('[data-id="uuid_result"] code').textContent = uuid;
            """)

    with c.col(span=4):
        with c.card("Password Generator"):
            c.code("", language="text", id="pwd_result")
            c.button("Generate Password", on_click="gen_pwd", variant="primary")
            c.static_handler("gen_pwd", """
                const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*';
                const arr = new Uint8Array(20);
                crypto.getRandomValues(arr);
                const pwd = Array.from(arr).map(b => chars[b % chars.length]).join('');
                document.querySelector('[data-id="pwd_result"] code').textContent = pwd;
            """)

    with c.col(span=4):
        with c.card("Timestamp"):
            c.code("", language="text", id="ts_result")
            c.button("Get Timestamp", on_click="gen_ts", variant="primary")
            c.static_handler("gen_ts", """
                const now = new Date();
                const ts = Math.floor(now.getTime() / 1000);
                const iso = now.toISOString();
                document.querySelector('[data-id="ts_result"] code').textContent =
                    `Unix: ${ts}\\nISO:  ${iso}`;
            """)

c.spacer()

# --- Hash ---
with c.card("SHA-256 Hash"):
    hash_input = c.signal("", name="hash_input")
    c.input("Text to hash", value=hash_input)
    c.button("Compute Hash", on_click="compute_hash", variant="primary")
    c.bind("compute_hash", hash_input)
    c.code("", language="text", id="hash_result")
    c.static_handler("compute_hash", """
        const text = args.value || '';
        const encoder = new TextEncoder();
        const data = encoder.encode(text);
        const hashBuffer = await crypto.subtle.digest('SHA-256', data);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
        document.querySelector('[data-id="hash_result"] code').textContent = hashHex;
    """)

c.spacer()

# --- JSON Formatter ---
with c.card("JSON Formatter"):
    json_input = c.signal('{"name":"cacao","version":"2.0","features":["charts","forms","static"]}', name="json_input")
    c.textarea("Paste JSON here", value=json_input, rows=3)
    c.button("Format JSON", on_click="format_json", variant="primary")
    c.bind("format_json", json_input)
    c.code("", language="json", id="json_result")
    c.static_handler("format_json", """
        try {
            const text = args.value || '';
            const parsed = JSON.parse(text);
            const formatted = JSON.stringify(parsed, null, 2);
            document.querySelector('[data-id="json_result"] code').textContent = formatted;
        } catch(e) {
            document.querySelector('[data-id="json_result"] code').textContent = 'Invalid JSON: ' + e.message;
        }
    """)
