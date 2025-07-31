import { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [prediction, setPrediction] = useState("");
  const [report, setReport] = useState("");
  const [loading, setLoading] = useState(false);

  const handleDrop = (e) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && droppedFile.type.startsWith("image/")) {
      setFile(droppedFile);
      setPrediction("");
      setReport("");
    }
  };

  const handlePredict = async () => {
    if (!file) return;
    setLoading(true);
    setPrediction("");
    setReport("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://127.0.0.1:8000/predict", formData);
      setPrediction(res.data.predicted_class);
      setReport(res.data.diagnosis_report);
    } catch {
      setPrediction("Prediction failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="bg-white shadow-2xl rounded-2xl p-6 max-w-md w-full text-center">
        <h1 className="text-2xl font-bold mb-6 text-gray-800">
          Eye Disease Classifier
        </h1>

        <div
          className="border-4 border-dashed border-blue-300 p-6 rounded-lg bg-blue-50 hover:bg-blue-100 cursor-pointer transition"
          onDrop={handleDrop}
          onDragOver={(e) => e.preventDefault()}
          onClick={() => document.getElementById("fileInput").click()}
        >
          {file ? (
            <img
              src={URL.createObjectURL(file)}
              alt="preview"
              className="max-h-48 mx-auto mb-2 rounded-lg"
            />
          ) : (
            <p className="text-blue-700">Click or Drag an Image File Here</p>
          )}
          <input
            id="fileInput"
            type="file"
            accept="image/*"
            hidden
            onChange={(e) => {
              setFile(e.target.files[0]);
              setPrediction("");
              setReport("");
            }}
          />
        </div>

        <button
          onClick={handlePredict}
          disabled={!file || loading}
          className="mt-6 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg w-full disabled:bg-blue-300"
        >
          {loading ? "Predicting..." : "Predict"}
        </button>

        {prediction && (
          <div className="mt-4 text-lg font-medium text-green-700">
            Prediction: <span className="font-bold">{prediction}</span>
          </div>
        )}

        {report && (
          <div className="mt-2 text-sm text-gray-700 text-left bg-gray-100 p-3 rounded-lg">
            <strong>Diagnosis Report:</strong>
            <p className="mt-1">{report}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
