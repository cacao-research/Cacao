/**
 * DocumentUpload - Upload documents and extract structured data
 *
 * Supports PDF, DOCX, CSV, XLSX, Markdown, TXT, HTML via Prompture ingestion.
 *
 * Props:
 *   schema            - JSON Schema for extraction (optional)
 *   provider          - LLM provider for extraction
 *   model             - Model name for extraction
 *   title             - Component title
 *   accept            - Accepted file types
 *   show_preview      - Show parsed text preview
 *   extract_on_upload - Auto-extract on upload
 *   doc_signal        - Signal to store document data
 */

const { createElement: h, useState, useRef, useCallback } = React;
import { cacaoWs } from '../core/websocket.js';

export function DocumentUpload({ props }) {
  const {
    schema,
    provider = 'openai',
    model = 'gpt-4o',
    title = 'Document Upload',
    accept = '.pdf,.docx,.csv,.xlsx,.md,.txt,.html',
    show_preview = true,
    extract_on_upload = false,
  } = props;

  const [docText, setDocText] = useState('');
  const [extracted, setExtracted] = useState(null);
  const [metadata, setMetadata] = useState(null);
  const [loading, setLoading] = useState(false);
  const [extracting, setExtracting] = useState(false);
  const [error, setError] = useState(null);
  const [fileName, setFileName] = useState('');
  const fileInputRef = useRef(null);
  const docId = useRef(`doc_${Date.now()}_${Math.random().toString(36).slice(2)}`);

  const handleFileChange = useCallback(async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setFileName(file.name);
    setLoading(true);
    setError(null);
    setDocText('');
    setExtracted(null);

    // Read file as base64 and send to server for parsing
    const reader = new FileReader();
    reader.onload = () => {
      const handler = (msg) => {
        if (msg.type === 'document:result' && msg.id === docId.current) {
          setDocText(msg.text || '');
          setMetadata(msg.metadata);
          if (msg.extracted) setExtracted(msg.extracted);
          setLoading(false);
          cacaoWs.removeListener(handler);
        } else if (msg.type === 'document:error' && msg.id === docId.current) {
          setError(msg.error);
          setLoading(false);
          cacaoWs.removeListener(handler);
        }
      };
      cacaoWs.addListener(handler);

      cacaoWs.send({
        type: 'document:upload',
        id: docId.current,
        file_path: file.name,
        file_data: reader.result.split(',')[1], // base64 data
        schema: extract_on_upload ? schema : null,
        model: `${provider}/${model}`,
      });
    };
    reader.readAsDataURL(file);
  }, [schema, provider, model, extract_on_upload]);

  const handleExtract = useCallback(() => {
    if (!docText || extracting || !schema) return;

    setExtracting(true);
    setError(null);

    const handler = (msg) => {
      if (msg.type === 'extract:result' && msg.id === docId.current) {
        setExtracted(msg.result);
        setExtracting(false);
        cacaoWs.removeListener(handler);
      } else if (msg.type === 'extract:error' && msg.id === docId.current) {
        setError(msg.error);
        setExtracting(false);
        cacaoWs.removeListener(handler);
      }
    };
    cacaoWs.addListener(handler);

    cacaoWs.send({
      type: 'extract:submit',
      id: docId.current,
      text: docText,
      schema: schema,
      model: `${provider}/${model}`,
    });
  }, [docText, extracting, schema, provider, model]);

  return h('div', { className: 'cacao-document-upload' },
    h('div', { className: 'cacao-document-header' },
      h('h3', null, title),
    ),

    // File input area
    h('div', {
      className: `cacao-document-dropzone ${loading ? 'loading' : ''}`,
      onClick: () => fileInputRef.current?.click(),
    },
      h('input', {
        ref: fileInputRef,
        type: 'file',
        accept: accept,
        onChange: handleFileChange,
        style: { display: 'none' },
      }),
      loading
        ? h('div', { className: 'cacao-document-loading' }, 'Parsing document...')
        : fileName
          ? h('div', { className: 'cacao-document-filename' },
              h('span', null, '📄 '),
              h('strong', null, fileName),
              metadata && h('span', { className: 'cacao-document-meta' },
                ` (${(metadata.length || 0).toLocaleString()} chars)`,
              ),
            )
          : h('div', { className: 'cacao-document-placeholder' },
              h('div', null, '📁'),
              h('div', null, 'Click to upload or drag & drop'),
              h('small', null, accept.split(',').join(', ')),
            ),
    ),

    error && h('div', { className: 'cacao-alert cacao-alert-error' }, error),

    // Preview
    show_preview && docText && h('div', { className: 'cacao-document-preview' },
      h('details', { open: !extracted },
        h('summary', null, 'Parsed Text Preview'),
        h('pre', { className: 'cacao-document-text' }, docText.slice(0, 5000)),
        docText.length > 5000 && h('small', null, `... ${docText.length - 5000} more characters`),
      ),
    ),

    // Extract button (when schema is set but extract_on_upload is off)
    schema && docText && !extract_on_upload && !extracted && h('button', {
      className: 'cacao-btn cacao-btn-primary',
      onClick: handleExtract,
      disabled: extracting,
    }, extracting ? 'Extracting...' : 'Extract Data'),

    // Extracted data
    extracted && h('div', { className: 'cacao-document-extracted' },
      h('h4', null, 'Extracted Data'),
      h('pre', { className: 'cacao-extract-result' }, JSON.stringify(extracted, null, 2)),
    ),
  );
}
