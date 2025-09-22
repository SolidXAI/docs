// components/TipBox.tsx
import { MdWarningAmber } from "react-icons/md";
import { ReactNode } from "react";

interface WarningBoxProps {
  children: ReactNode;
}

export const WarningBox: React.FC<WarningBoxProps> = ({ children }) => {
  return (
    <div className="tips-box warning-box">
      <h4 className="card-headear-wrapper flex items-center">
        <MdWarningAmber size={20} style={{ marginRight: "8px" }} />
        Warning
      </h4>
      <div className="mt-2">{children}</div>
    </div>
  );
};
