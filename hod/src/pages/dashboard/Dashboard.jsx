import "./Dashboard.css";
import MainDashboard from "./components/main/MainDashboard";
import Sidebar from "./components/sidebar/Sidebar";

function Dashboard({ children }) {
  return (
    <>
      <Sidebar />

      <MainDashboard>{children}</MainDashboard>
    </>
  );
}

export default Dashboard;
