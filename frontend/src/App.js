import React, { useState } from "react";
import axios from "axios";
import './App.css'

function App() {
  const [image, setImage] = useState(null);
  const [results, setResults] = useState([]);

  const uploadImage = async () => {
    if (!image) {
      alert("Please select an image first");
      return;
    }

    const formData = new FormData();
    formData.append("image", image); // Must match Flask key

    try {
      const res = await axios.post("http://localhost:5001/detect", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setResults(res.data);
      console.log(res.data);
    } catch (err) {
      console.error(err);
      alert("Upload failed! Check console for details.");
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h2>License Plate Recognition</h2>

      <input type="file" onChange={(e) => setImage(e.target.files[0])} />
      <br /><br />
      <button onClick={uploadImage}>Detect</button>

      {results.length > 0 && (
        <div style={{ marginTop: "30px" }}>
          <h3>Results:</h3>
          {results.map((r, i) => (
            <div key={i}>
              <p><b>Plate:</b> {r.text}</p>
              <p><b>Colour:</b> {r.colour}</p>
              <p><b>Type:</b> {r.vehicle_type}</p>
              <p><b>Confidence:</b> {r.confidence}</p>
              <hr />
            </div>
          ))}
        </div>
      )}

      <a
        href="http://localhost:5001/download_csv" // Fixed port
        target="_blank"
        rel="noopener noreferrer"
      >
        <button>Download CSV</button>
      </a>
    </div>
  );
}

export default App;
