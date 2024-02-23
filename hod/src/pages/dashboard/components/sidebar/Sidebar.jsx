import "./Sidebar.css";

import icon1 from "../../icons/icon1.png";
import icon2 from "../../icons/icon2.png";
import icon3 from "../../icons/icon3.png";
import icon4 from "../../icons/icon2.png";
import icon5 from "../../icons/icon4.png";
import icon6 from "../../icons/icon5.png";
import icon7 from "../../icons/icon6.png";
import { NavLink } from "react-router-dom";

function Sidebar() {
  return (
    <div className="dashboard-sidebar">
      <div className="sidebar-buttons-wrapper">
        <div className="sidebar-button">
          <div className="s-button-i">
            <img src={icon1} alt="" />
          </div>
        </div>
        <NavLink to={"/booking"}>
          <div className="sidebar-button">
            <div className="s-button-i">
              <img src={icon2} alt="" />
            </div>
            <div className="s-button-t">
              <p>Booking</p>
            </div>
          </div>
        </NavLink>
        <NavLink to={"/wallet"}>
          <div className="sidebar-button">
            <div className="s-button-i">
              <img src={icon3} alt="" />
            </div>
            <div className="s-button-t">
              <p>Wallet</p>
            </div>
          </div>
        </NavLink>
        <NavLink to={"/active_booking"}>
          <div className="sidebar-button">
            <div className="s-button-i">
              <img src={icon4} alt="" />
            </div>
            <div className="s-button-t">
              <p>
                Active <br /> Booking
              </p>
            </div>
          </div>
        </NavLink>
        <NavLink to={"/settings"}>
          <div className="sidebar-button">
            <div className="s-button-i">
              <img src={icon5} alt="" />
            </div>
            <div className="s-button-t">
              <p>Settings</p>
            </div>
          </div>
        </NavLink>
        <NavLink to={"/upload_hotel"}>
          <div className="sidebar-button">
            <div className="s-button-i">
              <img src={icon6} alt="" />
            </div>

            <div className="s-button-t">
              <p>Upload Hotel</p>
            </div>
          </div>
        </NavLink>
        <div className="sidebar-button">
          <div className="s-button-i">
            <img src={icon7} alt="" />
          </div>

          <div className="s-button-t">
            <p style={{color:"red"}}>Logout</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Sidebar;
