import "./Booking.css";
import image from "../../../public/testpng.png";

function BookingCard({ status }) {
  return (
    <>
      <div className="booking-card">
        <div className="booking-card-top">
          <button className="active_boocking_button">Client Details</button>
          <button>Hotel Information</button>
          <button>Location</button>
          <button>Client Information</button>
        </div>

        <div className="booking-card-center">
          <div className="booking-card-center-left">
            <div className="client-image">
              <img src={image} alt="" />
            </div>
            <div className="client-details">
              <h3>Emmanuel</h3>
              <p>Client</p>
            </div>
          </div>

          <div className="booking-card-center-right">
            <div className={status}>
              {status === "approved-booking" ? (
                <p>In Progress</p>
              ) : (
                <p>Canceled & Refunded</p>
              )}
            </div>
          </div>
        </div>

        <div className="booking-card-bottom">
          <div className="booking-detail">
            <p>Booking ID</p>
            <h3>#6467347383</h3>
          </div>
          <div className="booking-detail">
            <p>Hotel</p>
            <h3>2-bed Room</h3>
          </div>
          <div className="booking-detail">
            <p>Price</p>
            <h3>N 50,000</h3>
          </div>
          <div className="booking-detail">
            <p>Duration</p>
            <h3>2 nights</h3>
          </div>
        </div>
      </div>
    </>
  );
}

export default BookingCard;
