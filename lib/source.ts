import { docs } from 'collections/index';
import { loader } from 'fumadocs-core/source';

const mdxSource = docs.toFumadocsSource();

// fumadocs-mdx types `files` as VirtualFile[] but at runtime it's a lazy () => VirtualFile[]
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const files = typeof mdxSource.files === 'function' ? (mdxSource.files as any)() : mdxSource.files;

export const source = loader({
  baseUrl: '/docs',
  source: {
    files,
  },
});
