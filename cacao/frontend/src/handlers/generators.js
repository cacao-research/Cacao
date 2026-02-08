/**
 * Generator Handlers
 */

export const generators = {
  // UUID
  gen_uuid: (signals) => {
    const uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
      const r = Math.random() * 16 | 0;
      const v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
    signals.set('uuid_result', uuid);
  },

  // Password
  gen_password: (signals) => {
    const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*';
    const length = signals.get('pwd_length') || 16;
    let password = '';
    const array = new Uint32Array(length);
    crypto.getRandomValues(array);
    for (let i = 0; i < length; i++) {
      password += chars[array[i] % chars.length];
    }
    signals.set('password', password);
  },

  set_pwd_length: (signals, data) => {
    signals.set('pwd_length', parseInt(data.value) || 16);
  },

  // Lorem Ipsum
  gen_lorem: (signals) => {
    const LOREM_WORDS = [
      'lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur', 'adipiscing',
      'elit', 'sed', 'do', 'eiusmod', 'tempor', 'incididunt', 'ut', 'labore',
      'et', 'dolore', 'magna', 'aliqua', 'enim', 'ad', 'minim', 'veniam',
    ];

    const genSentence = () => {
      const length = 8 + Math.floor(Math.random() * 9);
      const words = [];
      for (let i = 0; i < length; i++) {
        words.push(LOREM_WORDS[Math.floor(Math.random() * LOREM_WORDS.length)]);
      }
      words[0] = words[0].charAt(0).toUpperCase() + words[0].slice(1);
      return words.join(' ') + '.';
    };

    const genParagraph = () => {
      const count = 4 + Math.floor(Math.random() * 5);
      const sentences = [];
      for (let i = 0; i < count; i++) {
        sentences.push(genSentence());
      }
      return sentences.join(' ');
    };

    const paraCount = signals.get('lorem_para') || 3;
    const paragraphs = [];
    for (let i = 0; i < paraCount; i++) {
      paragraphs.push(genParagraph());
    }
    signals.set('lorem_out', paragraphs.join('\n\n'));
  },

  set_lorem_para: (signals, data) => {
    signals.set('lorem_para', parseInt(data.value) || 3);
  },
};
