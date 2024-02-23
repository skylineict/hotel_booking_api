import { FaSearch } from "react-icons/fa";
import "./BookingPage.css";
import Dashboard from "../../Dashboard";
import filter from "../../icons/icon7.png";
import { useState } from "react";
import BookingCard from "../../../../components/booking/Booking";

function BookingPage() {
  const [activeTab, setActiveTab] = useState("approved");

  const handleTabChange = (tab) => {
    setActiveTab(tab);
  };

  return (
    <Dashboard>
      <div className="page-tltle">
        <h1>Hotel Booking</h1>
      </div>

      <div className="booking-filter-tabs-container">
        <button
          className={activeTab === "approved" ? "acive-booking-filter" : ""}
          onClick={() => handleTabChange("approved")}
        >
          Approved
        </button>
        <button
          className={activeTab === "cancelled" ? "acive-booking-filter" : ""}
          onClick={() => handleTabChange("cancelled")}
        >
          Cancelled
        </button>
      </div>

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

      {/* Main Contents */}

      {activeTab === "approved" && (
        <div className="approvedBookings">
          <div className="bookings-wrap">
            <BookingCard status="approved-booking" />
            <BookingCard status="approved-booking" />
            <BookingCard status="approved-booking" />
            <BookingCard status="approved-booking" />
            <BookingCard status="approved-booking" />
            <BookingCard status="approved-booking" />
            <BookingCard status="approved-booking" />
            <BookingCard status="approved-booking" />
            <BookingCard status="approved-booking" />
            <BookingCard status="approved-booking" />
            <BookingCard status="approved-booking" />
            <BookingCard status="approved-booking" />
          </div>
        </div>
      )}
      {activeTab === "cancelled" && (
        <div className="approvedBookings">
          <div className="bookings-wrap">
            <BookingCard status="cancelled-booking" />
            <BookingCard status="cancelled-booking" />
            <BookingCard status="cancelled-booking" />
            <BookingCard status="cancelled-booking" />
            <BookingCard status="cancelled-booking" />
            <BookingCard status="cancelled-booking" />
            <BookingCard status="cancelled-booking" />
            <BookingCard status="cancelled-booking" />
            <BookingCard status="cancelled-booking" />
            <BookingCard status="cancelled-booking" />
            <BookingCard status="cancelled-booking" />
            <BookingCard status="cancelled-booking" />
          </div>
        </div>
      )}
    </Dashboard>
  );
}

export default BookingPage;
