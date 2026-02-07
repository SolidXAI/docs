
import type { ReactNode } from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from '../HomepageFeatures/styles.module.css';
import React from 'react';


type FeatureItem = {
  title: string;
  description: ReactNode;
  // Svg?: React.ComponentType<React.ComponentProps<'svg'>>;
  imgs?: string
  moreInfo?: string,
  to?: string,

};

const TutorialList: FeatureItem[] = [
  {
    title: 'School Fess Portal',
    imgs: require('@site/static/img/homeImg1.png').default,
    description: (
      <>
        A complete guide for administrators and business users to create School Fees Portal application in SolidX. <br></br>Learn how to set up modules, setup core business entities or models, manage users, and tailor the platform to fit your organizational needs - without writing code.
      </>
    ),
    moreInfo: 'ReadMore',
    to: 'school-fees-portal/',
  },
  {
    title: 'Library Management',
    imgs: require('@site/static/img/homeImg1.png').default,
    description: (
      <>
        A complete guide for administrators and business users to create a Library Management System in SolidX. <br></br>Learn how to set up modules, setup core business entities or models, manage users, and tailor the platform to fit your organizational needs - without writing code.
        </>
    ),
    moreInfo: 'ReadMore',
    to: 'school-fees-portal/',
  },
];

function TutorialCard({ title, description, moreInfo, to, imgs }: FeatureItem) {
  return (
    <div className={clsx(`col col-5 ${styles.homeCards}`)}>
      <div className="text--start padding-horiz--md">
        <Heading as="h1">{title}</Heading>
        <p>{description}</p>

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

export default function TutorialCards(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className={`row ${styles.homeCardMain} `}>
          {TutorialList.map((props, idx) => (
            <TutorialCard key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
