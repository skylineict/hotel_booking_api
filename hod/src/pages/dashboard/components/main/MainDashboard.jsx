import "./MainDashboard.css";
function MainDashboard({children}) {
  return (

    <section className="dashboard-contents" >
        {children}
    </section>

  );
}

export default MainDashboard;
