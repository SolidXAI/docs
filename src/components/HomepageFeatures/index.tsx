import type { ReactNode } from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';


type FeatureItem = {
  title: string;
  description: ReactNode;
  Svg?: React.ComponentType<React.ComponentProps<'svg'>>;
  moreInfo?: string,
  to?: string,

};

const FeatureList: FeatureItem[] = [
  {
    title: 'Easy to Use',
    Svg: require('@site/static/img/undraw_docusaurus_mountain.svg').default,
    description: (
      <>
        Docusaurus was designed from the ground up to be easily installed and
        used to get your website up and running quickly.
      </>
    ),
    moreInfo: 'ReadMore',
    to: 'docs/user-docs/',

  },
  {
    title: 'Focus on What Matters',
    Svg: require('@site/static/img/undraw_docusaurus_tree.svg').default,
    description: (
      <>
        Docusaurus lets you focus on your docs, and we&apos;ll do the chores. Go
        ahead and move your docs into the <code >docs</code> directory.
      </>
    ),
    moreInfo: 'ReadMore',
    to: 'docs/user-docs/',
  },
  
 
];

function Feature({ title, description, moreInfo, to, Svg }: FeatureItem) {
  return (
    <div className={clsx(`col col--5 ${styles.homeCards}`)}>
      <div className="text--start padding-horiz--md">
      <img src="/img/CardIcon2.png" alt="" width={50} height={50} />
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
        <Svg className={styles.featureSvg} role="img" />
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
