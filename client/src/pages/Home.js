import React from "react";
import SteamIDForm from "../components/SteamIDForm";
import { SupersetExampleDashboard } from "../hooks/SupersetEmbedhook";

const Home = () => {

    return (
        <div>
            <h1>Steam-Bi</h1>
            <SteamIDForm></SteamIDForm>
            <SupersetExampleDashboard></SupersetExampleDashboard>
        </div>

    )
};

export default Home;