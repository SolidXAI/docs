import { themes as prismThemes } from 'prism-react-renderer';
import type { Config } from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)
import dotenv from 'dotenv';
dotenv.config();

const typesenseCollectionName = process.env.NEXT_PUBLIC_TYPESENSE_COLLECTION_NAME;
const typesenseHost = process.env.NEXT_PUBLIC_TYPESENSE_HOST;
const typesensePort = process.env.NEXT_PUBLIC_TYPESENSE_PORT;
const typesenseProtocol = process.env.NEXT_PUBLIC_TYPESENSE_PROTOCOL;
const typesenseApiKey = process.env.NEXT_PUBLIC_TYPESENSE_API_KEY;

const hasTypesenseConfig = Boolean(
  typesenseCollectionName &&
    typesenseHost &&
    typesensePort &&
    typesenseProtocol &&
    typesenseApiKey
);

const config: Config = {
  title: 'SolidX Docs',
  tagline: 'Enterprise-focussed low-code development platform',
  favicon: 'img/tab-logo.svg',

  // Set the production url of your site here
  url: 'https://docs.solidstarters.com',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'LogicLoop', // Usually your GitHub org/user name.
  projectName: 'solid-starters-docs', // Usually your repo name.

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  //  ADDED THIS
  // themes: ['docusaurus-theme-search-typesense'],

  
  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
        },
        blog: {
          showReadingTime: true,
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
          // Useful options to enforce blogging best practices
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },
      sitemap: {
        changefreq: 'weekly',
        priority: 0.5,
        filename: 'sitemap.xml',
        ignorePatterns: ['/tags/**'],
      },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {

    ...(hasTypesenseConfig
      ? {
          typesense: {
            typesenseCollectionName,
            typesenseServerConfig: {
              nodes: [
                {
                  host: typesenseHost,
                  port: Number(typesensePort),
                  protocol: typesenseProtocol,
                },
              ],
              // IMPORTANT: USE SEARCH-ONLY KEY HERE
              apiKey: typesenseApiKey,
            },
            searchParameters: {},
          },
        }
      : {}),

    colorMode: {
      defaultMode: 'light',
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },

    image: 'img/docusaurus-social-card.jpg',

    navbar: {
      title: '',
      logo: {
        alt: 'SolidX Alt Logo',
        src: 'img/NavbarLogo.svg',
      },
      items: [
        {
          to: '/docs/quick-start',
          label: 'Quick Start',
          position: 'left',
        },
        {
          type: 'custom-megaMenu',
          position: 'left',
          label: 'Tutorial',
          activeBasePath: '/docs/tutorial',
          description:
            'Learn SolidX by building a real application end to end, from setup through customization and implementation.',
          cta: {
            label: 'Open Tutorial Hub',
            to: '/docs/tutorial/',
          },
          sections: [
            {
              title: 'Start Here',
              items: [
                {
                  label: 'Tutorial Home',
                  to: '/docs/tutorial/',
                  description: 'Entry point into the guided learning path.',
                },
                {
                  label: 'SolidX Setup',
                  to: '/docs/tutorial/school-fees-portal/solidx_setup',
                  description: 'Set up the project and platform prerequisites.',
                },
                {
                  label: 'Product Overview',
                  to: '/docs/tutorial/school-fees-portal/fees_portal_product_overview',
                  description: 'Understand the School Fees Portal example domain.',
                },
              ],
            },
            {
              title: 'Core Concepts',
              items: [
                {
                  label: 'Field Types',
                  to: '/docs/tutorial/school-fees-portal/common/field-types',
                  description: 'See how domain fields are modelled in practice.',
                },
                {
                  label: 'Code Generation',
                  to: '/docs/tutorial/school-fees-portal/common/code-generation',
                  description: 'Understand the codegen workflow used in the tutorial.',
                },
                {
                  label: 'View Customizations',
                  to: '/docs/tutorial/school-fees-portal/common/applying-view-customizations',
                  description: 'Apply UI changes on top of generated views.',
                },
              ],
            },
            {
              title: 'Implementation',
              items: [
                {
                  label: 'Institute Onboarding',
                  to: '/docs/tutorial/school-fees-portal/end-to-end-implementation/institute_onboarding',
                  description: 'Walk through onboarding the institute flow.',
                },
                {
                  label: 'Activate Institute',
                  to: '/docs/tutorial/school-fees-portal/end-to-end-implementation/activate_institute',
                  description: 'Implement the activation flow and related behavior.',
                },
                {
                  label: 'Making Payment',
                  to: '/docs/tutorial/school-fees-portal/end-to-end-implementation/making_payment',
                  description: 'Follow the user-side payment journey.',
                },
              ],
            },
          ],
        },
        {
          type: 'custom-megaMenu',
          position: 'left',
          label: 'Reference',
          activeBasePath: '/docs/developer-docs',
          description:
            'Developer documentation for building full-stack SolidX applications with metadata, code generation, testing, APIs, and deployment.',
          cta: {
            label: 'Open Reference',
            to: '/docs/developer-docs/',
          },
          sections: [
            {
              title: 'Getting Started',
              items: [
                {
                  label: 'Quick Start',
                  to: '/docs/quick-start',
                  description: 'Get a SolidX project running in under 10 minutes.',
                },
                {
                  label: 'Overview',
                  to: '/docs/developer-docs/',
                  description: 'Orientation into the developer reference area.',
                },
                {
                  label: 'Prerequisites',
                  to: '/docs/developer-docs/prerequisites',
                  description: 'Prepare the local environment and toolchain.',
                },
                {
                  label: 'Installation',
                  to: '/docs/developer-docs/installation',
                  description: 'Bootstrap a new SolidX project.',
                },
                {
                  label: 'Project Structure',
                  to: '/docs/developer-docs/project-structure',
                  description: 'Understand the solid-api and solid-ui layout.',
                },
                {
                  label: 'solidctl Reference',
                  to: '/docs/developer-docs/solidctl-commands',
                  description: 'Use the CLI to build, seed, generate, and test.',
                },
              ],
            },
            {
              title: 'Core Systems',
              items: [
                {
                  label: 'Testing',
                  to: '/docs/developer-docs/testing/',
                  description: 'Metadata-driven API and UI testing support.',
                },
                {
                  label: 'Metadata Schema',
                  to: '/docs/developer-docs/metadata_schema/',
                  description: 'Define models, fields, views, roles, and more.',
                },
                {
                  label: 'REST APIs',
                  to: '/docs/developer-docs/rest-apis/',
                  description: 'Understand the generated API surface and behavior.',
                },
                {
                  label: 'Code Generation',
                  to: '/docs/developer-docs/extending/code-generation/',
                  description: 'See how metadata affects generated backend structure.',
                },
              ],
            },
            {
              title: 'Customization & Deployment',
              items: [
                {
                  label: 'Extending SolidX',
                  to: '/docs/developer-docs/extending/',
                  description: 'Customize backend, frontend, and built-in providers.',
                },
                {
                  label: 'UI Testing',
                  to: '/docs/developer-docs/testing/ui-testing',
                  description: 'Playwright-backed E2E testing patterns.',
                },
                {
                  label: 'API Testing',
                  to: '/docs/developer-docs/testing/api-testing',
                  description: 'Test APIs using the SolidX testing engine.',
                },
                {
                  label: 'Going Live',
                  to: '/docs/developer-docs/going-live/',
                  description: 'Deploy to VM, Docker, or ECS.',
                },
              ],
            },
          ],
        },
        {
          type: 'custom-megaMenu',
          position: 'left',
          label: 'Recipes',
          activeBasePath: '/docs/recipes',
          description:
            'Practical patterns and implementation snippets for common platform tasks.',
          cta: {
            label: 'Open Recipes',
            to: '/docs/recipes/',
          },
          sections: [
            {
              title: 'Core Patterns',
              items: [
                {
                  label: 'Filtering',
                  to: '/docs/recipes/filtering',
                  description: 'Apply filter patterns across generated APIs and UI.',
                },
                {
                  label: 'Handlers',
                  to: '/docs/recipes/handlers',
                  description: 'Implement common event and action handlers.',
                },
                {
                  label: 'Workflow Status',
                  to: '/docs/recipes/workflow-status',
                  description: 'Model and use workflow-driven status transitions.',
                },
                {
                  label: 'Computed Fields',
                  to: '/docs/recipes/computed-fields',
                  description: 'Use computed behavior in a practical way.',
                },
              ],
            },
            {
              title: 'Platform Recipes',
              items: [
                {
                  label: 'Email',
                  to: '/docs/recipes/email',
                  description: 'Integrate email behavior and templating.',
                },
                {
                  label: 'Queue',
                  to: '/docs/recipes/queue',
                  description: 'Work with queue-backed platform workflows.',
                },
                {
                  label: 'Media Providers',
                  to: '/docs/recipes/media-providers',
                  description: 'Configure and extend media storage behavior.',
                },
              ],
            },
            {
              title: 'Data & Access',
              items: [
                {
                  label: 'Additional Datasources',
                  to: '/docs/recipes/additional-datasources',
                  description: 'Use more than one datasource in a project.',
                },
                {
                  label: 'Soft Delete',
                  to: '/docs/recipes/soft-delete',
                  description: 'Work with archived or recoverable records.',
                },
                {
                  label: 'Extending Users',
                  to: '/docs/recipes/extending-users',
                  description: 'Add custom behavior around the user model.',
                },
              ],
            },
          ],
        },
        {
          type: 'custom-megaMenu',
          position: 'left',
          label: 'Admin',
          activeBasePath: '/docs/admin-docs',
          description:
            'Use the admin manual to model business domains, manage layouts, configure access, and run the platform.',
          cta: {
            label: 'Open Admin Manual',
            to: '/docs/admin-docs/',
          },
          sections: [
            {
              title: 'Module Builder',
              items: [
                {
                  label: 'Overview',
                  to: '/docs/admin-docs/module-builder/',
                  description: 'The conceptual center of metadata-driven app building.',
                },
                {
                  label: 'Module Management',
                  to: '/docs/admin-docs/module-builder/module-management',
                  description: 'Create and organize business domains.',
                },
                {
                  label: 'Model Management',
                  to: '/docs/admin-docs/module-builder/model-management',
                  description: 'Define the records and relationships in each module.',
                },
                {
                  label: 'Field Management',
                  to: '/docs/admin-docs/module-builder/field-management',
                  description: 'Configure field types and platform semantics.',
                },
              ],
            },
            {
              title: 'Layouts',
              items: [
                {
                  label: 'Layouts Overview',
                  to: '/docs/admin-docs/layouts/',
                  description: 'Understand how generated screens are structured.',
                },
                {
                  label: 'List View',
                  to: '/docs/admin-docs/layouts/list-view',
                  description: 'Configure many-record browsing experiences.',
                },
                {
                  label: 'Form View',
                  to: '/docs/admin-docs/layouts/form-view',
                  description: 'Shape single-record editing experiences.',
                },
                {
                  label: 'Kanban View',
                  to: '/docs/admin-docs/layouts/kanban-view',
                  description: 'Configure workflow-style board layouts.',
                },
              ],
            },
            {
              title: 'Access & Operations',
              items: [
                {
                  label: 'IAM',
                  to: '/docs/admin-docs/iam/',
                  description: 'Manage users, roles, permissions, and record rules.',
                },
                {
                  label: 'Notifications',
                  to: '/docs/admin-docs/notifications/',
                  description: 'Configure email and SMS template behavior.',
                },
                {
                  label: 'Media Library',
                  to: '/docs/admin-docs/media-library/',
                  description: 'Handle uploaded media and storage providers.',
                },
                {
                  label: 'Settings',
                  to: '/docs/admin-docs/settings/',
                  description: 'Manage platform-level operational settings.',
                },
              ],
            },
          ],
        },
        // {
        //   to: '/blog',
        //   label: ' Blog',
        //   position: 'left',
        //   className: 'custom-center-item',
        // },

        // {
        //   href: 'https://github.com/facebook/docusaurus',
        //   label: 'GitHub',
        //   position: 'right',
        // },

        //  ADDED SEARCH BAR HERE
        // {
        //   type: 'search',
        //   position: 'right',
        // },
      ],
    },

    footer: {
      style: 'dark',
      links: [],
      copyright: `Copyright © ${new Date().getFullYear()} SolidX. All rights reserved.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.vsDark,
      additionalLanguages: ['typescript', 'tsx', 'bash', 'json', 'http', 'diff'],
      magicComments: [
        {
          className: 'theme-code-block-highlighted-line',
          line: 'highlight-next-line',
          block: {start: 'highlight-start', end: 'highlight-end'},
        },
      ],
    },


  } satisfies Preset.ThemeConfig,

  themes: hasTypesenseConfig ? ['docusaurus-theme-search-typesense'] : [],


};

export default config;
