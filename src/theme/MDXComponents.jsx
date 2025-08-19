import React from 'react';
import MDXComponents from '@theme-original/MDXComponents';
import Zoom from 'react-medium-image-zoom';
import 'react-medium-image-zoom/dist/styles.css';

export default {
  ...MDXComponents,
  img: (props) => (
    <Zoom>
      <img {...props} style={{ cursor: 'zoom-in' }} />
    </Zoom>
  ),
};
