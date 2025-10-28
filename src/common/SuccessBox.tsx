import React, { ReactNode } from 'react';
import { FaCheckCircle } from 'react-icons/fa';

interface SuccessBoxProps {
  children: ReactNode;
  title?: string;
}

export const SuccessBox: React.FC<SuccessBoxProps> = ({ children, title = 'Success' }) => {
  return (
    <div className="tips-box info-box" style={{ borderLeftColor: 'var(--solid-success)', backgroundColor: 'var(--solid-success-bg)' }}>
      <h4 style={{ color: 'var(--solid-success)' }} className="card-headear-wrapper flex items-center">
        <FaCheckCircle size={18} style={{ marginRight: "8px" }} />
        {title}
      </h4>
      <div className="mt-2">{children}</div>
    </div>
  );
};

