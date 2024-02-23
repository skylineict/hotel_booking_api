import Dashboard from "../../Dashboard";
import "./SettingsPage.css";
import hotelIage from "../../icons/Group 302.png";
import editButton from "../../icons/bxs_message-square-edit.png";
import editProfileIcon from "../../icons/Vector (4).png";
import playButton from "../../icons/Frame 308.png";
import walletIcon from "../../icons/iconoir_wallet.png";
import notificatioIcon from "../../icons/ri_notification-4-line.png";

function SettingsPage() {
  return (
    <Dashboard>
      <div className="settings-page-container">
        <div className="settings-page-inner">
          <div className="settings-page-top">
            <div className="edit-button">
              <img src={editButton} alt="" />
            </div>
            <div className="hotel-profile-image">
              <img src={hotelIage} alt="" />
            </div>
            <h3>Golden Hotel</h3>
            <p>goldenhotel@gmail.com</p>
          </div>
          <div className="settings-page-buttons">
            <div className="settings-button">
              <div className="setting-button-left">
                <div className="s-b-i">
                  <img src={editProfileIcon} alt="" />
                </div>

                <div className="s-b-t">
                  <p>Edit Profile</p>
                </div>
              </div>

              <div className="s-b-c">
                <img src={playButton} alt="" />
              </div>
            </div>
            <div className="settings-button">
              <div className="setting-button-left">
                <div className="s-b-i">
                  <img src={walletIcon} alt="" />
                </div>

                <div className="s-b-t">
                  <p>Wallet</p>
                </div>
              </div>

              <div className="s-b-c">
                <img src={playButton} alt="" />
              </div>
            </div>
            <div className="settings-button">
              <div className="setting-button-left">
                <div className="s-b-i">
                  <img src={notificatioIcon} alt="" />
                </div>

                <div className="s-b-t">
                  <p>Notifications</p>
                </div>
              </div>

              <div className="s-b-c">
              <label className="switch">
                    <input type="checkbox" />
                    <span className="slider round"></span>
                    </label>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Dashboard>
  );
}

export default SettingsPage;
