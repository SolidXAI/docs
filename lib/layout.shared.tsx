import type { BaseLayoutProps } from 'fumadocs-ui/layouts/shared';

export function baseOptions(): BaseLayoutProps {
  return {
    nav: {
      title: (
        <img src="/img/NavbarLogo.svg" alt="SolidX" className="h-6" />
      ),
    },
    links: [
      { text: 'Quick Start', url: '/docs/quick-start' },
      { text: 'Tutorial', url: '/docs/tutorial', active: 'nested-url' },
      { text: 'Admin', url: '/docs/admin-docs', active: 'nested-url' },
      { text: 'Reference', url: '/docs/developer-docs', active: 'nested-url' },
      { text: 'Recipes', url: '/docs/recipes', active: 'nested-url' },
    ],
  };
}
