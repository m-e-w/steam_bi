import React from "react";
import SteamIDForm from "../components/SteamIDForm";
import SupersetDashboard from "../components/SupersetDashboard";

const Home = () => {

    return (
        <div>
            <h1>Steam-Bi</h1>
            <SteamIDForm></SteamIDForm>
            <SupersetDashboard></SupersetDashboard>
        </div>

    )
};

export default Home;