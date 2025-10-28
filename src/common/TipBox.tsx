import React, { ReactNode } from 'react';
import { FaLightbulb } from 'react-icons/fa';

interface TipBoxProps {
  children: ReactNode;
  title?: string;
}

export const TipBox: React.FC<TipBoxProps> = ({ children, title = 'Tip' }) => {
  return (
    <div className="tips-box" style={{ borderLeftColor: 'var(--solid-success)', backgroundColor: 'var(--solid-success-bg)' }}>
      <h4 style={{ color: 'var(--solid-success)' }} className="card-headear-wrapper flex items-center">
        <FaLightbulb size={18} style={{ marginRight: "8px" }} />
        {title}
      </h4>
      <div className="mt-2">{children}</div>
    </div>
  );
};

