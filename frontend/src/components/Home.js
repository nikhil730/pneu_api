import React, { useState } from "react";

const Home = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [result, setResult] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    const previewURL = URL.createObjectURL(event.target.files[0]);
    setImagePreview(previewURL);
  };

  const handlePredict = async () => {
    if (!selectedFile) {
      alert("Please select an image first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch(
        "https://pnuemonia-det-api.onrender.com/predict",
        {
          method: "POST",
          body: formData,
        }
      );
      const result = await response.json();
      console.log(result);

      setResult(result);
    } catch (error) {
      console.error("Error during prediction:", error);
    }
  };

  return (
    <div>
      <h1>Image Upload and Prediction</h1>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      {imagePreview && (
        <img
          src={imagePreview}
          alt="Selected"
          style={{ maxWidth: "100%", maxHeight: "300px" }}
        />
      )}
      <button onClick={handlePredict}>Predict</button>
      {result && <p>Prediction result: {result}</p>}
    </div>
  );
};

export default Home;
