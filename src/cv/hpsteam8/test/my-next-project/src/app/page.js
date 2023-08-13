import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/").then((response) => {
      setMessage(response.data);
    });
  }, []);

  return <div className="App">{message}</div>;
}

export default App;
