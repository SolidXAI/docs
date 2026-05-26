import type { BaseLayoutProps } from 'fumadocs-ui/layouts/shared';

export function baseOptions(): BaseLayoutProps {
  return {
    nav: {
      title: (
        <img src="/img/NavbarLogo.svg" alt="SolidX" className="h-6" />
      ),
    },
    links: [],
  };
}
