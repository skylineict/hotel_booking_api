import Dashboard from "../../Dashboard";
import "./WalletPage.css";
import image from "../../icons/Group 302.png";
import rightArrow from "../../icons/ion_chevron-back-sharp.png";
import hidden from "../../icons/Component 15.png";
import open from "../../icons/Component 15 (1).png";
import settingsIcon from "../../icons/ic_baseline-settings.png";
import { useState } from "react";

function WalletPage() {
  const [balanceHidden, setBalanceHidden] = useState(false);

  const handleBalanceHiddenStaus = () => {
    setBalanceHidden(!balanceHidden);
  };

  return (
    <Dashboard>
      <div className="logged_in_hotel">
        <div className="logged_left">
          <img src={image} alt="" />
        </div>
        <div className="logged-right">
          <h3>Golden Hotel</h3>
          <p>RC-75874</p>
        </div>
      </div>

      <div className="wallet-balance-container">
        <div className="wallet-card">
          <div className="wallet-card-top">
            <div className="wallet-top-left">
              <p>Available Balance</p>
            </div>
            <div className="wallet-top-right">
              <p>Transaction History</p>
              <img src={rightArrow} alt="" />
            </div>
          </div>

          <div className="wallet-card-center">
            <h3>{balanceHidden ? "***********" : "N29,000.00"}</h3>
            <img
              onClick={handleBalanceHiddenStaus}
              src={balanceHidden ? hidden : open}
              alt=""
            />
          </div>

          <div className="wallet-card-bottom">
            <div className="w-c-b-b">
              <img src={settingsIcon} alt="" />
              <p>Settings</p>
            </div>
            <div className="w-c-b-b">
              <img src={settingsIcon} alt="" />
              <p>Withdraw</p>
            </div>
          </div>
        </div>
      </div>
    </Dashboard>
  );
}

export default WalletPage;
