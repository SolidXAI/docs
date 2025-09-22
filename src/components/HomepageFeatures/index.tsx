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
    title: 'Admin Docs',
    imgs: require('@site/static/img/homeImg1.png').default,
    description: (
      <>
        A complete guide for administrators and business users to install, configure, and manage applications in SolidX. <br></br>Learn how to set up modules, setup core business entities or models, manage users, and tailor the platform to fit your organizational needs—without writing code.
      </>
    ),
    moreInfo: 'ReadMore',
    to: 'docs/admin-docs/',
  },
  // {
  //   title: 'Guided Tutorial',
  //   imgs: require('@site/static/img/homeImg1.png').default,
  //   description: (
  //     <>
  //       Dive into SolidX’s low-code engine and learn how to extend, customize, and integrate enterprise applications using APIs, code hooks, and reusable components. <br></br>Ideal for developers looking to build advanced logic and automation on top of the platform.
  //     </>
  //   ),
  //   moreInfo: 'ReadMore',
  //   to: 'docs/admin-docs/',
  // },
  {
    title: 'Developer Docs',
    imgs: require('@site/static/img/homeImg1.png').default,
    description: (
      <>
        Dive into SolidX’s low-code engine and learn how to extend, customize, and integrate enterprise applications using APIs, code hooks, and reusable components. <br></br>Ideal for developers looking to build advanced logic and automation on top of the platform.
      </>
    ),
    moreInfo: 'ReadMore',
    to: 'docs/developer-docs/',
  },
];

function Feature({ title, description, moreInfo, to, imgs }: FeatureItem) {
  return (
    <div className={clsx(`col col--5 ${styles.homeCards}`)}>
      <div className="text--start padding-horiz--md">
        <img src="/img/CardIcon2.png" alt="" width={50} height={50} />
        <Heading as="h1">{title}</Heading>
        <p className=''>{description}</p>

        <a href={to} className={styles.moreInfoLink}>
          {moreInfo}
          <svg
            className={styles.arrowIcon}
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M5 12H19M19 12L13 6M19 12L13 18"
              stroke="#a77aff"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </a>

      </div>
      <div className="text--start">
        <img src={imgs} className={styles.featureSvg} role="img" />
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
