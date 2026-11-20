import { createMDX } from 'fumadocs-mdx/next';

/** @type {import('next').NextConfig} */
const config = {
  reactStrictMode: true,
  async redirects() {
    return [
      {
        source: '/docs/solidx',
        destination: '/docs/solidx/quick-start',
        permanent: false,
      },
      {
        source: '/docs/test-hub',
        destination: '/docs/test-hub/getting-started/quickstart',
        permanent: false,
      },
      ...['quick-start', 'developer-docs', 'recipes', 'tutorial', 'admin-docs', 'product-modules'].flatMap((section) => [
        {
          source: `/docs/${section}`,
          destination: `/docs/solidx/${section}`,
          permanent: true,
        },
        {
          source: `/docs/${section}/:path*`,
          destination: `/docs/solidx/${section}/:path*`,
          permanent: true,
        },
      ]),
    ];
  },
};

const withMDX = createMDX();

export default withMDX(config);
