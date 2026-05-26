import { docs } from 'collections/index';
import { loader } from 'fumadocs-core/source';
import * as LucideIcons from 'lucide-react';
import { createElement, type ReactElement } from 'react';

const mdxSource = docs.toFumadocsSource();

// fumadocs-mdx types `files` as VirtualFile[] but at runtime it's a lazy () => VirtualFile[]
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const files = typeof mdxSource.files === 'function' ? (mdxSource.files as any)() : mdxSource.files;

function resolveIcon(name: string | undefined): ReactElement | undefined {
  if (!name) return undefined;
  const pascal = name
    .split('-')
    .map((s) => s.charAt(0).toUpperCase() + s.slice(1))
    .join('');
  const Icon = (LucideIcons as Record<string, unknown>)[pascal] as
    | React.ComponentType<{ className?: string }>
    | undefined;
  if (!Icon) return undefined;
  return createElement(Icon, { className: 'size-4' });
}

export const source = loader({
  baseUrl: '/docs',
  source: {
    files,
  },
  icon: resolveIcon,
});
