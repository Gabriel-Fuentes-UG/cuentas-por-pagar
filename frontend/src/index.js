import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import App from "./App";

// Use legacy rendering mode to avoid React 18 concurrent rendering issues with Radix UI portals
ReactDOM.render(<App />, document.getElementById("root"));
