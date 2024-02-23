import { useState } from "react";
import { Button } from "../components/button/Button";
import Input from "../components/input/Input";
import BookingCard from "../components/booking/Booking";
import Dashboard from "./dashboard/Dashboard";
import filter from "./dashboard/icons/icon7.png";
import { FaSearch } from "react-icons/fa";

function Test() {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");

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

export default Test;
