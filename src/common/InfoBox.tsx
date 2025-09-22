// components/TipBox.tsx
import { HiOutlineInformationCircle } from "react-icons/hi2";
import { ReactNode } from "react";

interface InfoBoxProps {
  children: ReactNode;
}

export const InfoBox: React.FC<InfoBoxProps> = ({ children }) => {
  return (
    <div className="tips-box info-box">
      <h4 className="card-headear-wrapper flex items-center">
        <HiOutlineInformationCircle size={20} style={{ marginRight: "8px" }} />
        Info
      </h4>
      <div className="mt-2">{children}</div>
    </div>
  );
};
