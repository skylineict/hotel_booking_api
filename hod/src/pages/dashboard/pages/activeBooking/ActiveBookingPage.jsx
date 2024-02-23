import Dashboard from "../../Dashboard";
import "./ActiveBookingPage.css";
import filter from "../../icons/icon7.png";
import { FaSearch } from "react-icons/fa";
import BookingCard from "../../../../components/booking/Booking";


function ActiveBookingPage() {
  return (
    <Dashboard>
       <div className="search-container">
        <div className="search-input">
          <div className="search-icon">
            <span>
              <FaSearch />
            </span>
          </div>
          <input placeholder="Search" type="text" />

          <div className="filter-icon">
            <img src={filter} alt="" />
          </div>
        </div>
      </div>

      <div className="cards-container-title">
        <h1>Active Booking</h1>
      </div>

      <div className="active-cards-container">

        <BookingCard />
        <BookingCard />
        <BookingCard />
        <BookingCard />
        <BookingCard />
        <BookingCard />

      </div>
    </Dashboard>
  );
}

export default ActiveBookingPage;
