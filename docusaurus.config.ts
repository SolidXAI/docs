import { themes as prismThemes } from 'prism-react-renderer';
import type { Config } from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)
import dotenv from 'dotenv';
dotenv.config();

const config: Config = {
  title: 'SolidX Docs',
  tagline: 'Enterprise-focussed low-code development platform',
  favicon: 'img/tab-logo.png',

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

    //  ADDED TYPESENSE CONFIG
    typesense: {
      typesenseCollectionName: process.env.NEXT_PUBLIC_TYPESENSE_COLLECTION_NAME,

      typesenseServerConfig: {
        nodes: [
          {
            host: process.env.NEXT_PUBLIC_TYPESENSE_HOST,
            port: Number(process.env.NEXT_PUBLIC_TYPESENSE_PORT),
            protocol: process.env.NEXT_PUBLIC_TYPESENSE_PROTOCOL,
          },
        ],
      
        // IMPORTANT: USE SEARCH-ONLY KEY HERE
        apiKey: process.env.NEXT_PUBLIC_TYPESENSE_API_KEY,
      },
      
      searchParameters: {},
    },

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
        src: 'img/NavbarLogo.png',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: ' Tutorial',
          className: 'custom-center-item',
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
      logo: {
        src: 'img/NavbarLogo.png',
        className: 'footer-bottom-icon'
      },

      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Tutorial',
              to: 'docs/admin-docs/',
            },
          ],
        },
        // {
        //   title: 'Community',
        //   items: [
        //     {
        //       label: 'Stack Overflow',
        //       href: 'https://stackoverflow.com/questions/tagged/docusaurus',
        //     },
        //     {
        //       label: 'Discord',
        //       href: 'https://discordapp.com/invite/docusaurus',
        //     },
        //     {
        //       label: 'X',
        //       href: 'https://x.com/docusaurus',
        //     },
        //   ],
        // },
        // {
        //   title: 'More',
        //   items: [
        //     {
        //       label: 'Blog',
        //       to: '/blog',
        //       className: "myfooterdataClass"
        //     },
        //     {
        //       label: 'GitHub',
        //       href: 'https://github.com/facebook/docusaurus',
        //     },
        //   ],
        // },
      ],
      // copyright: `Copyright © ${new Date().getFullYear()} SolidX, LogicLoop Ventures LLP.`,
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

  themes: ['docusaurus-theme-search-typesense'],

  // plugins: [
  //   [
  //     'docusaurus-biel',
  //     {
  //       project: 'yrjmteh4r5',
  //       headerTitle: 'Biel.ai chatbot',
  //       version: 'latest',
  //       bielButtonText: 'ASK AI',
  //       buttonPosition: 'center-right',
  //       modalPosition: 'sidebar-right',
  //       buttonStyle: 'dark',
  //       enable: true,
  //     },
  //   ],
  // ],
};

export default config;
