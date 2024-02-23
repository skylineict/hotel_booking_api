import "./Onboard.css";
import { FaChevronLeft } from "react-icons/fa";
import Input from "../../components/input/Input";
import { useState, useRef, useEffect } from "react";
import { Button, StaticButton } from "../../components/button/Button";
import { Link } from "react-router-dom";
import Modal from "../../components/Modal/Modal";
import Select from "react-select";

function Onboard() {
  const [hotelName, setHotelName] = useState("");
  const [location, setLocation] = useState("");
  const [country, setCountry] = useState("");
  const [hotelId, setHotelId] = useState("");
  const [hotelStatus, setHotelStatus] = useState("");
  const [isSearchable, setIsSearchable] = useState(true);
  const [options, setOptions] = useState([]);
  const [selectedCountry, setSelectedCountry] = useState(null);

  const handleCountryChange = (selectedOption) => {
    setSelectedCountry(selectedOption);

    console.log(selectedOption);
  };

  const customStyles = {
    control: (provided, state) => ({
      ...provided,
      backgroundColor: "transparent", // Change background color
      border: state.isFocused ? "2px solid #0083FD" : "2px solid #0083FD", // Example border color change when focused
      borderRadius: "8px",
      padding: "10px",
    }),
    option: (provided, state) => ({
      ...provided,
      color: state.isSelected ? "white" : "white", // Change text color based on whether it's selected or not
      backgroundColor: "var(--body-color)", // Change background color based on whether it's selected or not
    }),
    singleValue: (provided, state) => ({
      ...provided,
      color: state.isSelected ? "white" : "white", // Change text color of the selected item
    }),
    input: (provided) => ({
      ...provided,
      color: "white", // Change search text color
    }),
  };

  const hotelStatusOptions = [
    { value: "unregistered", label: "Unregistered" },
    { value: "registered", label: "Registered" },
  ];

  useEffect(() => {
    const fetchCountries = async () => {
      try {
        const response = await fetch("https://restcountries.com/v3.1/all");
        const data = await response.json();
        const countries = data.map((country) => ({
          value: country.name.common,
          label: country.name.common,
        }));
        setOptions(countries);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchCountries();
  }, []);

  return (
    <section className="signup-container">
      <div className="signup-container-inner">
        <div className="container-top">
          <div className="container-top-left">
            <span>
              <FaChevronLeft />
            </span>
          </div>

          <div className="container-top-right"></div>
        </div>

        <div className="onboard-title">
          <h3>
            Hello, Golden Hotel !! <br />
            Tell us about your Hotel
          </h3>
        </div>

        <div className="signup-form-container">
          <Input
            title={"Hotel Name"}
            placeholder={"Enter Hotel Name"}
            type={"text"}
            value={hotelName}
            changeValue={setHotelName}
            id={"hotel_name"}
          />

          <Input
            title={"Location"}
            placeholder={"Verify Address Here"}
            type={"text"}
            value={location}
            changeValue={setLocation}
            id={"location"}
          />

          <div className="i-g">
            <label htmlFor="">Select Country</label>
          </div>

          <Select
            className="basic-single"
            classNamePrefix="select"
            defaultValue={options[0]}
            isSearchable={isSearchable}
            name="color"
            options={options}
            styles={customStyles}
            onChange={handleCountryChange}
          />

          <Input
            title={"Hotel ID"}
            placeholder={"Upload your personal info here(NIN & PASSPORT)"}
            type={"text"}
            value={hotelId}
            changeValue={setHotelId}
            id={"hotel_id"}
          />

          <div className="i-g">
            <label htmlFor="">Hotel Registration Status</label>
          </div>

          <Select
            className="basic-single"
            classNamePrefix="select"
            defaultValue={hotelStatusOptions[0]}
            isSearchable={false}
            name="color"
            options={hotelStatusOptions}
            styles={customStyles}
            onChange={setHotelStatus}
          />
        </div>

        <div className="signup-btn">
          <StaticButton text={"Continue"} onclick={""} />
        </div>
      </div>
    </section>
  );
}

export default Onboard;
