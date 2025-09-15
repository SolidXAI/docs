import React from 'react';
import { FaPencilAlt } from 'react-icons/fa';

interface TipsBoxProps {
  children: React.ReactNode;
}

export const NoteBoxs: React.FC<TipsBoxProps> = ({ children }) => {
  return (
    <div className="tips-box note-box">
      <h4>
        <FaPencilAlt color="#8c6dbe" style={{ marginRight: '0.5em' }}   size={13}/>
        Note
      </h4>
      <ul>
        {React.Children.map(children, (child) => (
          <li>{child}</li>
        ))}
      </ul>
    </div>
  );
};
