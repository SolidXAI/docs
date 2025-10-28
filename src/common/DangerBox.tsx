import React, { ReactNode } from 'react';
import { MdError } from 'react-icons/md';

interface DangerBoxProps {
  children: ReactNode;
  title?: string;
}

export const DangerBox: React.FC<DangerBoxProps> = ({ children, title = 'Danger' }) => {
  return (
    <div className="tips-box error-box">
      <h4 className="card-headear-wrapper flex items-center">
        <MdError size={20} style={{ marginRight: "8px" }} />
        {title}
      </h4>
      <div className="mt-2">{children}</div>
    </div>
  );
};

