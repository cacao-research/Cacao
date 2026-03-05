/**
 * Video - Embed YouTube, Vimeo, or direct video files
 */

const { createElement: h } = React;

function parseProvider(src) {
  if (!src) return { type: 'direct', id: null };

  // YouTube
  const ytMatch = src.match(/(?:youtube\.com\/(?:watch\?v=|embed\/)|youtu\.be\/)([\w-]+)/);
  if (ytMatch) return { type: 'youtube', id: ytMatch[1] };

  // Vimeo
  const vimeoMatch = src.match(/vimeo\.com\/(?:video\/)?([\d]+)/);
  if (vimeoMatch) return { type: 'vimeo', id: vimeoMatch[1] };

  return { type: 'direct', id: null };
}

export function Video({ props }) {
  const { src, title = '', width, height, aspect = '16/9', poster, autoplay = false, controls = true, loop = false, muted = false } = props;
  const { type, id } = parseProvider(src);

  const containerStyle = { aspectRatio: aspect };
  if (width) containerStyle.width = typeof width === 'number' ? width + 'px' : width;
  if (height) { containerStyle.height = typeof height === 'number' ? height + 'px' : height; containerStyle.aspectRatio = undefined; }

  if (type === 'youtube') {
    const params = new URLSearchParams();
    if (autoplay) params.set('autoplay', '1');
    if (loop) params.set('loop', '1');
    if (muted) params.set('mute', '1');
    const paramStr = params.toString();
    return h('div', { className: 'c-video', style: containerStyle },
      h('iframe', {
        src: 'https://www.youtube.com/embed/' + id + (paramStr ? '?' + paramStr : ''),
        title,
        frameBorder: '0',
        allow: 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture',
        allowFullScreen: true,
        className: 'c-video-iframe',
      })
    );
  }

  if (type === 'vimeo') {
    const params = new URLSearchParams();
    if (autoplay) params.set('autoplay', '1');
    if (loop) params.set('loop', '1');
    if (muted) params.set('muted', '1');
    const paramStr = params.toString();
    return h('div', { className: 'c-video', style: containerStyle },
      h('iframe', {
        src: 'https://player.vimeo.com/video/' + id + (paramStr ? '?' + paramStr : ''),
        title,
        frameBorder: '0',
        allow: 'autoplay; fullscreen; picture-in-picture',
        allowFullScreen: true,
        className: 'c-video-iframe',
      })
    );
  }

  // Direct video file
  return h('div', { className: 'c-video', style: containerStyle },
    h('video', {
      src,
      title,
      poster,
      controls,
      autoPlay: autoplay,
      loop,
      muted,
      className: 'c-video-player',
    })
  );
}
