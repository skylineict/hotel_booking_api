import "./App.css";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Test from "./pages/TestPage";
import Signup from "./pages/signup/Signup";
import Login from "./pages/login/Login";
import Onboard from "./pages/Onboard/Onboard";
import BookingPage from "./pages/dashboard/pages/booking/BookingPage";
import ActiveBookingPage from "./pages/dashboard/pages/activeBooking/ActiveBookingPage";
import WalletPage from "./pages/dashboard/pages/walletPage/WalletPage";
import SettingsPage from "./pages/dashboard/pages/settings/SettingsPage";

function App() {
  const router = createBrowserRouter([
    {
      path: "/",
      element: <Test />,
    },
    {
      path: "/join",
      element: <Signup />,
    },
    {
      path: "/login",
      element: <Login />,
    },
    {
      path: "/onboard",
      element: <Onboard />,
    },
    {
      path: "/booking",
      element: <BookingPage />,
    },
    {
      path: "/active_booking",
      element: <ActiveBookingPage />,
    },
    {
      path: "/wallet",
      element: <WalletPage />,
    },
    {
      path: "/settings",
      element: <SettingsPage />,
    },
    {
      path: "*",
      element: <h1>Not Found Bro!</h1>,
    },
  ]);

  return (
    <>
      <RouterProvider router={router} />
    </>
  );
}

export default App;
