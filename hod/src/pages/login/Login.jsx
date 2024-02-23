import "../signup/Signup.css";
import { FaChevronLeft } from "react-icons/fa";
import Input from "../../components/input/Input";
import { useState, useRef, useEffect } from "react";
import { Button, StaticButton } from "../../components/button/Button";
import { Link } from "react-router-dom";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setpassword] = useState("");
  const [firstStep, setFirstStep] = useState(true);
  const [secondStep, setSecondStep] = useState(false);
  const [firstCode, setFirstCode] = useState("");
  const [secondCode, setSecondCode] = useState("");
  const [thirdCode, setThirdCode] = useState("");
  const [fourthCode, setFourthCode] = useState("");
  const [countdown, setCountdown] = useState(60);
  const [countdownReachedZero, setCountdownReachedZero] = useState(false);
  const minutes = Math.floor(countdown / 60);
  const seconds = countdown % 60;
  const firstCodeRef = useRef();
  const secondCodeRef = useRef();
  const thirdCodeRef = useRef();
  const fourthCodeRef = useRef();

  const handleLoginClick = async () => {
    // console.log("Sign Up Button Was Clicked")

    setFirstStep(false);
    setSecondStep(true);
  };

  const backToFirstStage = () => {
    setSecondStep(false);
    setFirstStep(true);
  };

  const handleCodeInput = (value, index) => {
    if (index === 1) {
      if (value === "") {
        setFirstCode(value);
        return;
      }
      const splitedValue = value.split("");
      if (value.length > 1) {
        setFirstCode(splitedValue[0] || firstCode);
        setSecondCode(splitedValue[1] || secondCode);
        setThirdCode(splitedValue[2] || thirdCode);
        setFourthCode(splitedValue[3] || fourthCode);
        return;
      }

      setFirstCode(value);
      secondCodeRef.current.focus();
    } else if (index === 2) {
      if (value === "") {
        setSecondCode(value);
        firstCodeRef.current.focus();
        return;
      }

      const splitedValue = value.split("");

      if (value.length > 1) {
        setFirstCode(splitedValue[0] || firstCode);
        setSecondCode(splitedValue[1] || secondCode);
        setThirdCode(splitedValue[2] || thirdCode);
        setFourthCode(splitedValue[3] || fourthCode);
        return;
      }

      setSecondCode(value);
      thirdCodeRef.current.focus();
    } else if (index === 3) {
      if (value === "") {
        setThirdCode(value);
        secondCodeRef.current.focus();
        return;
      }
      const splitedValue = value.split("");

      if (value.length > 1) {
        setFirstCode(splitedValue[0] || firstCode);
        setSecondCode(splitedValue[1] || secondCode);
        setThirdCode(splitedValue[2] || thirdCode);
        setFourthCode(splitedValue[3] || fourthCode);
        return;
      }

      setThirdCode(value);
      fourthCodeRef.current.focus();
    } else if (index === 4) {
      if (value === "") {
        setFourthCode(value);
        thirdCodeRef.current.focus();
        return;
      }

      const splitedValue = value.split("");

      if (value.length > 1) {
        setFirstCode(splitedValue[0] || firstCode);
        setSecondCode(splitedValue[1] || secondCode);
        setThirdCode(splitedValue[2] || thirdCode);
        setFourthCode(splitedValue[3] || fourthCode);
        return;
      }

      setFourthCode(value);
    }
  };

  const decrementCountdown = () => {
    if (countdown <= 0) {
      if (!countdownReachedZero) {
        console.log("Countdown reached zero!");
        setCountdownReachedZero(true);
      }
    } else {
      setCountdown(
        (prevCountdown) => prevCountdown > 0 && secondStep && prevCountdown - 1
      );
    }
  };

  useEffect(() => {
    const timer = setInterval(decrementCountdown, 1000);

    return () => clearInterval(timer);
  }, [secondStep]);

  return (
    <section className="signup-container">
      <div className="signup-container-inner">
        {firstStep && (
          //==== FIRST STEP (INPUTS SECTION) Starts =====//

          <>
            <div className="container-top">
              <div className="container-top-left">
                <span>
                  <FaChevronLeft />
                </span>
              </div>

              <div className="container-top-right">
                <h3>Login to Your Account</h3>
              </div>
            </div>

            <div className="signup-form-container">
              <Input
                title={"Email"}
                placeholder={"Enter Your Email"}
                type={"email"}
                value={email}
                changeValue={setEmail}
                id={"email"}
              />

              <Input
                title={"Password"}
                placeholder={"Enter Your password"}
                type={"password"}
                value={password}
                changeValue={setpassword}
                id={"password"}
              />
            </div>

            <div className="signup-btn">
              <StaticButton text={"Login"} onclick={handleLoginClick} />
            </div>

            <div className="already-have-account">
              <p>New Here ?</p>
              <Link to={"/join"}>Create Account</Link>
            </div>
          </>

          //==== FIRST STEP (INPUTS SECTION) Ends Here =====//
        )}
        ;
        {secondStep && (
          // SECOND STEP (PHONE NO VERIFICATION) Starts Here //

          <>
            <div className="container-top">
              <div className="container-top-left">
                <span onClick={backToFirstStage}>
                  <FaChevronLeft />
                </span>
              </div>

              <div className="container-top-right">
                <h3>Verify Your Number</h3>
              </div>
            </div>

            <div className="phone-ver-message">
              <p>Enter the 4- digit code we sent via text to</p>

              <div className="number-change_btn">
                <p>+234816653375</p>
                <span>Change</span>
              </div>
            </div>

            <div className="verification-codes-input">
              <div className="single-ver-code">
                <input
                  ref={firstCodeRef}
                  value={firstCode}
                  onChange={(e) => handleCodeInput(e.target.value, 1)}
                  type="text"
                />
              </div>

              <div className="single-ver-code">
                <input
                  ref={secondCodeRef}
                  value={secondCode}
                  onChange={(e) => handleCodeInput(e.target.value, 2)}
                  type="text"
                />
              </div>

              <div className="single-ver-code">
                <input
                  ref={thirdCodeRef}
                  value={thirdCode}
                  onChange={(e) => handleCodeInput(e.target.value, 3)}
                  type="text"
                />
              </div>

              <div className="single-ver-code">
                <input
                  ref={fourthCodeRef}
                  value={fourthCode}
                  onChange={(e) => handleCodeInput(e.target.value, 4)}
                  type="text"
                />
              </div>
            </div>

            <div className="text-arrival-message">
              <p>
                The Text should arrive within{" "}
                {minutes.toString().padStart(2, "0")}:
                {seconds.toString().padStart(2, "0")} secs
              </p>
            </div>

            <div className="resend-btn">
              <p>I didn’t receive the OTP? </p>
              <span className={countdownReachedZero ? "" : "cant-resend"}>
                Resend OTP
              </span>
            </div>

            <div className="continue-ver-btn">
              <StaticButton text={"Continue"} />
            </div>
          </>

          // SECOND STEP (PHONE NO VERIFICATION) Ends Here //
        )}
      </div>
    </section>
  );
}

export default Login;
