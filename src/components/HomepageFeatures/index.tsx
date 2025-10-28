import type { ReactNode } from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';


type FeatureItem = {
  title: string;
  description: ReactNode;
  // Svg?: React.ComponentType<React.ComponentProps<'svg'>>;
  imgs?:string
  moreInfo?: string,
  to?: string,

};

const FeatureList: FeatureItem[] = [
  {
    title: 'Admin Documentation',
    imgs: require('@site/static/img/homeImage-11.png').default,
    description: (
      <>
        A complete guide for administrators and business users to install, configure, and manage applications in SolidX. Learn how to set up modules, setup core business entities or models, manage users, and tailor the platform to fit your organizational needs—without writing code.
      </>
    ),
    moreInfo: 'Get Started',
    to: 'docs/admin-docs/',
  },
  {
    title: 'Developer Documentation',
    imgs: require('@site/static/img/homeImage-22.png').default,
    description: (
      <>
        Dive into SolidX's low-code engine and learn how to extend, customize, and integrate enterprise applications using APIs, code hooks, and reusable components. Ideal for developers looking to build advanced logic and automation on top of the platform.
      </>
    ),
    moreInfo: 'Explore Docs',
    to: 'docs/developer-docs/',
  },
];

function Feature({ title, description, moreInfo, to, imgs }: FeatureItem) {
  return (
    <div className={clsx(`col col--5 ${styles.homeCards}`)}>
      <div className="text--start padding-horiz--md">
        <img src="/img/CardIcon2.png" alt="" width={50} height={50} style={{ marginBottom: '1rem' }} />
        <Heading as="h2" style={{ fontSize: '1.75rem', marginBottom: '1rem' }}>{title}</Heading>
        <p style={{ fontSize: '1rem', lineHeight: '1.7', marginBottom: '1.5rem' }}>{description}</p>

        <a href={to} className={styles.moreInfoLink}>
          {moreInfo}
          <svg
            className={styles.arrowIcon}
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M5 12H19M19 12L13 6M19 12L13 18"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </a>
      </div>
      <div className="text--start">
        <img src={imgs} className={styles.featureSvg} role="img" alt={`${title} illustration`} />
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className={`row ${styles.homeCardMain} `}>
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
