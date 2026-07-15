import type { BaseLayoutProps } from 'fumadocs-ui/layouts/shared';

export function baseOptions(): BaseLayoutProps {
  return {
    nav: {
      title: (
        <>
          <img
            src="/img/solidx-logo-dark.png"
            alt="SolidX"
            className="h-6 dark:hidden"
          />
          <img
            src="/img/solidx-logo-light.png"
            alt="SolidX"
            className="hidden h-6 dark:block"
          />
        </>
      ),
    },
    links: [],
  };
}
